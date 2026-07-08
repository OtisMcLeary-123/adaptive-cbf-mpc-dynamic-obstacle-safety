# Scripts

Entrypoints:

```text
run_e5_dynamic_obstacle_prediction.py
run_e6_rule_adaptive_gamma.py
run_extended_suite.py
build_tables_figures.py
reproduce_all.sh
run_block_b_smoke.sh
```

Smoke example:

```bash
bash scripts/run_block_b_smoke.sh
```

Paper reproduction:

```bash
bash scripts/reproduce_all.sh
```

Individual E6 commands:

```bash
python3 scripts/run_e6_rule_adaptive_gamma.py --seeds 50 --fixed-gammas 0.15 0.08 0.04 --backend random_shooting
python3 scripts/run_e6_rule_adaptive_gamma.py --seeds 20 --fixed-gammas 0.15 0.08 0.04 --backend casadi --casadi-horizon 8
```

`build_tables_figures.py` reads generated `results/**/summary.json` files and writes GitHub-renderable outputs under `docs/tables/`, `docs/figures/extended/`, and `docs/paper_section_results.md`.
