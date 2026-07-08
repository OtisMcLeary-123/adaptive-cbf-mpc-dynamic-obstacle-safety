# Block B Experiment Protocol

## Purpose

Block B establishes non-LLM adaptive safety baselines for the paper.

The experiments must use the same point-mass scenario family as Block A so later language-interface repos can compare against both fixed CBF and adaptive non-LLM safety controllers.

## Experiment Order

```text
E5 -> E6
```

## Scenario Set

The E6 scenario suite includes the base dynamic obstacle task plus `aggressive_crossing_v1`, `fast_crossing_v1`, `late_crossing_v1`, `head_on_v1`, and `noisy_prediction_v1`.

## Required Outputs

Each experiment writes the standardized output layout:

```text
results/<experiment_name>/
  config.yaml
  metrics_summary.csv
  per_seed_metrics.csv
  trajectories/
    seed_000_<method>.csv
  figures/
    seed_000_overlay.png
    seed_000_clearance_curve.png
    clearance_boxplot.png
    solve_time_boxplot.png
  logs/
    run.log
  report.md
```

`per_seed_metrics.csv` must keep this schema stable for downstream LaMPC/LLM blocks:

```text
experiment,scenario,controller,backend,seed,gamma,success,collision,min_clearance,path_length,completion_time,mean_solve_time,p95_solve_time,solver_failures,infeasible_rate,fallback_rate,collision_after_fallback,control_failure
```

## Comparison Rules

- E5 compares obstacle prediction assumptions with matched seeds and fixed gamma.
- E6 compares fixed gamma values `0.15`, `0.08`, and `0.04` with rule-based adaptive gamma using matched seeds.
- Backend comparison runs E6 with both `random_shooting` and `casadi` backends.
- Solver failure must be reported separately from control failure.
- Report `infeasible_rate`, `fallback_rate`, and `collision_after_fallback_rate` when the backend exposes these events.
- Do not introduce language feedback or LLM calls in Block B.
- Log `gamma_used`, `prediction_mode`, `sensor_delay_steps`, `backend`, `infeasible`, `fallback_used`, and `solver_status` in trace outputs.

## Acceptance Criteria

- E5 produces a static/stale/velocity-prediction comparison.
- E6 produces fixed `0.15`/`0.08`/`0.04` vs adaptive gamma comparison.
- E6 paper-main runs use 50 seeds.
- CasADi/IPOPT backend comparison uses at least 20 matched seeds.
- Per-scenario and paired-delta tables are generated under `docs/tables/`.
- Both experiments produce overlay trajectory, clearance curve, clearance boxplot, and solve-time boxplot figures.
