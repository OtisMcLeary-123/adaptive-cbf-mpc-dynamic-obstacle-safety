#!/usr/bin/env bash
set -euo pipefail

# Main 50-seed Block B paper runs.
python3 scripts/run_extended_suite.py --suite base --seeds 50

# Base + hard scenario E6 comparison, 50 matched seeds each.
python3 scripts/run_extended_suite.py --suite scenarios --seeds 50

# Backend comparison with CasADi/IPOPT synced from Block A.
python3 scripts/run_extended_suite.py --suite backend --backend-seeds 20 --casadi-horizon 8

# Tables, selected figures, and paper-style report section.
python3 scripts/build_tables_figures.py
