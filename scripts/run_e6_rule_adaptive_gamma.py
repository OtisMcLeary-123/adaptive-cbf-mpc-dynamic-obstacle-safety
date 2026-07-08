#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from block_b.runner import run_e6_adaptive_gamma


def main() -> None:
    parser = argparse.ArgumentParser(description="Run E6 fixed vs rule-adaptive CBF gamma comparison.")
    parser.add_argument("--scenario", default=ROOT / "configs/scenario_point_mass_2d.json")
    parser.add_argument("--output", default=ROOT / "results/exp_e6")
    parser.add_argument("--seeds", type=int, default=10)
    parser.add_argument("--fixed-gamma", type=float, default=None, help="Backward-compatible single fixed gamma.")
    parser.add_argument("--fixed-gammas", type=float, nargs="+", default=[0.15, 0.08, 0.04])
    parser.add_argument("--backend", choices=["random_shooting", "casadi"], default="random_shooting")
    parser.add_argument("--casadi-horizon", type=int, default=8)
    args = parser.parse_args()
    fixed_gammas = [args.fixed_gamma] if args.fixed_gamma is not None else args.fixed_gammas
    run_e6_adaptive_gamma(
        args.scenario,
        args.output,
        seeds=args.seeds,
        fixed_gammas=fixed_gammas,
        backend=args.backend,
        casadi_horizon=args.casadi_horizon,
    )
    print(f"Wrote E6 results to {args.output}")


if __name__ == "__main__":
    main()
