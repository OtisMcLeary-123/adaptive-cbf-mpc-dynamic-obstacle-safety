#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from block_b.runner import run_e5_prediction_comparison


def main() -> None:
    parser = argparse.ArgumentParser(description="Run E5 dynamic obstacle prediction comparison.")
    parser.add_argument("--scenario", default=ROOT / "configs/scenario_point_mass_2d.json")
    parser.add_argument("--output", default=ROOT / "results/exp_e5")
    parser.add_argument("--seeds", type=int, default=10)
    parser.add_argument("--gamma", type=float, default=0.08)
    parser.add_argument("--sensor-delay-steps", type=int, default=3)
    parser.add_argument("--backend", choices=["random_shooting", "casadi"], default="random_shooting")
    parser.add_argument("--casadi-horizon", type=int, default=8)
    args = parser.parse_args()
    run_e5_prediction_comparison(
        args.scenario,
        args.output,
        seeds=args.seeds,
        gamma=args.gamma,
        sensor_delay_steps=args.sensor_delay_steps,
        backend=args.backend,
        casadi_horizon=args.casadi_horizon,
    )
    print(f"Wrote E5 results to {args.output}")


if __name__ == "__main__":
    main()
