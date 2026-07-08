# Source

This directory contains the shared Block B implementation.

Modules:

```text
dynamics.py
scenario.py
metrics.py
controllers.py
runner.py
plots.py
```

The current v1 implementation uses a deterministic NumPy random-shooting MPC controller for reproducible micro-experiments.

Block B extends the Block A controller with:

- obstacle prediction modes: `static`, `stale_velocity`, `true_velocity`
- rule-based adaptive CBF gamma from clearance and time-to-collision
