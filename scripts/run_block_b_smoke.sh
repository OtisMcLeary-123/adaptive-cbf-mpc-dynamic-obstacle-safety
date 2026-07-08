#!/usr/bin/env bash
set -euo pipefail

python3 scripts/run_e5_dynamic_obstacle_prediction.py --seeds 3 --gamma 0.08 --sensor-delay-steps 3
python3 scripts/run_e6_rule_adaptive_gamma.py --seeds 3 --fixed-gamma 0.15
