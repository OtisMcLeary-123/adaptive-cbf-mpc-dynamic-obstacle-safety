# Block B Experiment Protocol

## Purpose

Block B establishes non-LLM adaptive safety baselines for the paper.

The experiments must use the same point-mass scenario family as Block A so later language-interface repos can compare against both fixed CBF and adaptive non-LLM safety controllers.

## Experiment Order

```text
E5 -> E6
```

## Required Outputs

Each experiment should write:

```text
results/exp_<id>/summary.json
results/exp_<id>/trace.csv
results/exp_<id>/trajectory.png
results/exp_<id>/distance_to_obstacle.png
docs/exp_<id>_report.md
```

## Comparison Rules

- E5 compares obstacle prediction assumptions with matched seeds and fixed gamma.
- E6 compares fixed gamma with rule-based adaptive gamma using matched seeds.
- Do not introduce language feedback or LLM calls in Block B.
- Log `gamma_used`, `prediction_mode`, and `sensor_delay_steps` in trace outputs.

## Acceptance Criteria

- E5 produces a static/stale/velocity-prediction comparison.
- E6 produces a fixed-vs-adaptive gamma comparison.
- Both experiments produce trajectory and distance-to-obstacle plots.
