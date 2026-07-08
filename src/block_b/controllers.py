from __future__ import annotations

from dataclasses import dataclass
import time

import numpy as np

from .dynamics import clip_norm, nominal_pd_control, step_state
from .scenario import Scenario, obstacle_position


@dataclass(frozen=True)
class ControlResult:
    control: np.ndarray
    solve_time_ms: float
    solver_success: bool
    predicted_violation: float
    gamma_used: float | None


class SamplingMPCController:
    """Deterministic random-shooting MPC for lightweight baseline experiments."""

    def __init__(
        self,
        scenario: Scenario,
        method: str,
        seed: int,
        gamma: float | None = None,
        obstacle_enabled: bool = True,
        prediction_mode: str = "true_velocity",
        sensor_delay_steps: int = 0,
    ) -> None:
        if method not in {"smoke", "ed", "cbf", "adaptive_cbf"}:
            raise ValueError(f"Unsupported method: {method}")
        if prediction_mode not in {"true_velocity", "static", "stale_velocity"}:
            raise ValueError(f"Unsupported prediction mode: {prediction_mode}")
        self.scenario = scenario
        self.method = method
        self.seed = seed
        self.gamma = gamma
        self.obstacle_enabled = obstacle_enabled
        self.prediction_mode = prediction_mode
        self.sensor_delay_steps = sensor_delay_steps

    @property
    def safe_radius(self) -> float:
        return self.scenario.robot.radius + self.scenario.obstacle.radius

    def solve(self, state: np.ndarray, step: int) -> ControlResult:
        start = time.perf_counter()
        if self.method == "smoke" and not self.obstacle_enabled:
            control = nominal_pd_control(state, self.scenario)
            solve_time_ms = (time.perf_counter() - start) * 1000.0
            return ControlResult(
                control=control,
                solve_time_ms=solve_time_ms,
                solver_success=True,
                predicted_violation=0.0,
                gamma_used=None,
            )
        gamma_used = self._effective_gamma(state, step)
        controls = self._candidate_sequences(state, step)
        cost, violation = self._score_sequences(state, controls, step, gamma_used)
        best_idx = int(np.argmin(cost))
        solve_time_ms = (time.perf_counter() - start) * 1000.0
        return ControlResult(
            control=controls[best_idx, 0],
            solve_time_ms=solve_time_ms,
            solver_success=bool(violation[best_idx] <= 1e-7),
            predicted_violation=float(violation[best_idx]),
            gamma_used=gamma_used,
        )

    def _candidate_sequences(self, state: np.ndarray, step: int) -> np.ndarray:
        sim = self.scenario.simulation
        robot = self.scenario.robot
        rng = np.random.default_rng(self.seed * 10007 + step * 97 + 13)
        horizon = sim.horizon_steps
        n = sim.candidate_sequences
        nominal = nominal_pd_control(state, self.scenario)

        controls = rng.normal(loc=nominal, scale=0.95, size=(n, horizon, 2))
        decay = np.linspace(1.0, 0.45, horizon)[None, :, None]
        controls = nominal + (controls - nominal) * decay

        controls[0, :, :] = nominal
        lateral = self._lateral_direction(state, step)
        for idx, scale in enumerate([0.7, 1.1, -0.7, -1.1], start=1):
            if idx < n:
                controls[idx, :, :] = nominal + scale * lateral * robot.max_accel
        return clip_norm(controls, robot.max_accel)

    def _lateral_direction(self, state: np.ndarray, step: int) -> np.ndarray:
        pos = state[:2]
        obs = obstacle_position(self.scenario, step)
        to_target = self.scenario.robot.target - pos
        direction = np.array([-to_target[1], to_target[0]], dtype=float)
        if np.linalg.norm(direction) < 1e-9:
            direction = np.array([0.0, 1.0])
        direction = direction / np.linalg.norm(direction)
        if np.dot(obs - pos, direction) > 0:
            direction = -direction
        return direction

    def _score_sequences(
        self, state: np.ndarray, controls: np.ndarray, step: int, gamma_used: float | None
    ) -> tuple[np.ndarray, np.ndarray]:
        scenario = self.scenario
        target = scenario.robot.target
        states = np.repeat(state[None, :], controls.shape[0], axis=0)
        cost = np.zeros(controls.shape[0])
        violation_total = np.zeros(controls.shape[0])
        previous_h = self._barrier_value(states[:, :2], self._predicted_obstacle_position(step, 0))

        for horizon_idx in range(scenario.simulation.horizon_steps):
            u = controls[:, horizon_idx, :]
            states = step_state(states, u, scenario)
            pos = states[:, :2]
            vel = states[:, 2:]
            target_error = pos - target
            cost += 1.0 * np.sum(target_error * target_error, axis=1)
            cost += 0.05 * np.sum(vel * vel, axis=1)
            cost += 0.02 * np.sum(u * u, axis=1)

            if self.obstacle_enabled:
                obs = self._predicted_obstacle_position(step, horizon_idx + 1)
                h_value = self._barrier_value(pos, obs)
                if self.method == "ed":
                    violation = np.maximum(0.0, -h_value)
                elif self.method in {"cbf", "adaptive_cbf"}:
                    gamma = 1.0 if gamma_used is None else float(gamma_used)
                    cbf_rhs = (1.0 - gamma) * previous_h
                    violation = np.maximum(0.0, cbf_rhs - h_value)
                    violation += 5.0 * np.maximum(0.0, -h_value)
                    previous_h = h_value
                else:
                    violation = np.zeros_like(h_value)
                violation_total += violation
                cost += 9000.0 * violation * violation + 2000.0 * violation

        final_error = states[:, :2] - target
        cost += 12.0 * np.sum(final_error * final_error, axis=1)
        return cost, violation_total

    def _barrier_value(self, positions: np.ndarray, obstacle: np.ndarray) -> np.ndarray:
        delta = positions - obstacle
        return np.sum(delta * delta, axis=-1) - self.safe_radius * self.safe_radius

    def _effective_gamma(self, state: np.ndarray, step: int) -> float | None:
        if self.method == "adaptive_cbf":
            return self._rule_based_gamma(state, step)
        if self.method == "cbf":
            return 0.15 if self.gamma is None else float(self.gamma)
        return self.gamma

    def _rule_based_gamma(self, state: np.ndarray, step: int) -> float:
        pos = state[:2]
        vel = state[2:]
        obs = obstacle_position(self.scenario, step)
        rel = obs - pos
        distance = float(np.linalg.norm(rel))
        clearance = distance - self.safe_radius
        if distance < 1e-9:
            return 0.02

        rel_velocity = self.scenario.obstacle.velocity - vel
        closing_speed = -float(np.dot(rel_velocity, rel / distance))
        ttc = clearance / max(closing_speed, 1e-6) if closing_speed > 0.0 else np.inf

        if clearance < 0.35 or ttc < 1.0:
            return 0.02
        if clearance < 0.75 or ttc < 2.0:
            return 0.04
        return 0.08

    def _predicted_obstacle_position(self, current_step: int, horizon_offset: int) -> np.ndarray:
        if self.prediction_mode == "true_velocity":
            return obstacle_position(self.scenario, current_step + horizon_offset)

        sensed_step = max(0, current_step - self.sensor_delay_steps)
        sensed_position = obstacle_position(self.scenario, sensed_step)
        if self.prediction_mode == "static":
            return sensed_position
        return sensed_position + horizon_offset * self.scenario.simulation.dt * self.scenario.obstacle.velocity
