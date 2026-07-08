# Source

This directory contains the shared Block B implementation.

Modules:

```text
artifacts.py
controllers.py
dynamics.py
metrics.py
plots.py
runner.py
scenario.py
```

The implementation supports two MPC backends:

| Backend | Implementation | Notes |
|---|---|---|
| `random_shooting` | deterministic NumPy random-shooting MPC | Fast backend for 50-seed sweeps. |
| `casadi` | CasADi/IPOPT nonlinear program | Solver comparison backend synced from Block A. |

Block B extends the Block A controller with:

- obstacle prediction modes: `static`, `stale_velocity`, `true_velocity`
- rule-based adaptive CBF gamma from clearance and time-to-collision
- standardized artifacts: `config.yaml`, `metrics_summary.csv`, `per_seed_metrics.csv`, trajectory CSVs, figures, logs, and per-run report
- explicit separation of solver failure, infeasibility, fallback, control failure, and collision metrics
