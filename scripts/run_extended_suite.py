#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from block_b.runner import run_e5_prediction_comparison, run_e6_adaptive_gamma


BASE_SCENARIO = ROOT / "configs/scenario_point_mass_2d.json"
SCENARIO_DIR = ROOT / "configs/scenarios"


def slug(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]+", "_", value).strip("_").lower()


def scenario_paths() -> list[Path]:
    return [BASE_SCENARIO] + sorted(SCENARIO_DIR.glob("*.json"))


def scenario_id(path: Path) -> str:
    return json.loads(path.read_text())["scenario_id"]


def run_base(seeds: int, backend: str, casadi_horizon: int) -> None:
    run_e5_prediction_comparison(
        BASE_SCENARIO,
        ROOT / "results/paper_main/e5_prediction_50_seed",
        seeds=seeds,
        gamma=0.08,
        sensor_delay_steps=3,
        backend=backend,
        casadi_horizon=casadi_horizon,
    )
    run_e6_adaptive_gamma(
        BASE_SCENARIO,
        ROOT / "results/paper_main/e6_adaptive_50_seed",
        seeds=seeds,
        fixed_gammas=[0.15, 0.08, 0.04],
        backend=backend,
        casadi_horizon=casadi_horizon,
    )


def run_scenarios(seeds: int, backend: str, casadi_horizon: int) -> None:
    for scenario in scenario_paths():
        sid = scenario_id(scenario)
        out = ROOT / "results/extended/scenarios" / slug(f"{sid}_{backend}")
        run_e6_adaptive_gamma(
            scenario,
            out,
            seeds=seeds,
            fixed_gammas=[0.15, 0.08, 0.04],
            backend=backend,
            casadi_horizon=casadi_horizon,
        )


def run_backend(seeds: int, casadi_horizon: int) -> None:
    for backend in ["random_shooting", "casadi"]:
        run_e6_adaptive_gamma(
            BASE_SCENARIO,
            ROOT / "results/extended/backend_comparison" / backend,
            seeds=seeds,
            fixed_gammas=[0.15, 0.08, 0.04],
            backend=backend,
            casadi_horizon=casadi_horizon,
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run extended Block B benchmark suites.")
    parser.add_argument("--suite", choices=["base", "scenarios", "backend", "all"], default="all")
    parser.add_argument("--seeds", type=int, default=50)
    parser.add_argument("--backend-seeds", type=int, default=20)
    parser.add_argument("--backend", choices=["random_shooting", "casadi"], default="random_shooting")
    parser.add_argument("--casadi-horizon", type=int, default=8)
    args = parser.parse_args()

    if args.suite in {"base", "all"}:
        run_base(args.seeds, args.backend, args.casadi_horizon)
    if args.suite in {"scenarios", "all"}:
        run_scenarios(args.seeds, args.backend, args.casadi_horizon)
    if args.suite in {"backend", "all"}:
        run_backend(args.backend_seeds, args.casadi_horizon)


if __name__ == "__main__":
    main()
