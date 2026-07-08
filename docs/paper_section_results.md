# Block B Results Section Draft

## Experimental Setup

Block B evaluates non-LLM adaptive CBF baselines on the same dynamic obstacle point-mass task as Block A. E5 compares obstacle prediction assumptions, and E6 compares fixed CBF gamma values against a rule-adaptive CBF controller.

## E6 Main Comparison

| Method | Runs | Success | Collision | Clearance | Solve time |
|---|---:|---:|---:|---:|---:|
| Fixed CBF gamma=0.15 | 50 | 0.880 | 0.000 | 0.491 | 1.830 |
| Fixed CBF gamma=0.08 | 50 | 0.860 | 0.000 | 0.823 | 1.824 |
| Fixed CBF gamma=0.04 | 50 | 0.860 | 0.000 | 1.033 | 1.827 |
| Rule adaptive CBF | 50 | 0.800 | 0.000 | 0.853 | 1.831 |

The paired-delta table reports matched-seed changes from each fixed gamma baseline to the rule-adaptive CBF controller.

## Tables

See `docs/tables/summary_metrics.md`, `docs/tables/scenario_comparison.md`, and `docs/tables/paired_delta.md`.

## Reproducibility

Run `scripts/reproduce_all.sh` to regenerate Block B paper outputs.
