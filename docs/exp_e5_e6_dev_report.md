# Block B Dev Report

## Run

Date: 2026-07-08

Commands:

```bash
python3 scripts/run_e5_dynamic_obstacle_prediction.py --seeds 10 --gamma 0.08 --sensor-delay-steps 3
python3 scripts/run_e6_rule_adaptive_gamma.py --seeds 10 --fixed-gamma 0.15
```

Solver implementation:

```text
numpy_random_shooting_mpc
```

## Results

| Experiment | Method | Success rate | Collision rate | Mean min clearance | Mean path length | Mean completion time | Mean solve time |
|---|---|---:|---:|---:|---:|---:|---:|
| E5 | CBF static obstacle in horizon | 0.9 | 0.0 | 0.529 m | 5.564 m | 5.97 s | 1.867 ms |
| E5 | CBF stale sensing, delay=3 | 0.8 | 0.0 | 0.781 m | 6.080 m | 6.46 s | 1.852 ms |
| E5 | CBF velocity prediction | 0.9 | 0.0 | 0.812 m | 5.779 m | 5.26 s | 1.829 ms |
| E6 | Fixed CBF gamma=0.15 | 0.9 | 0.0 | 0.485 m | 5.374 m | 4.85 s | 1.852 ms |
| E6 | Rule adaptive CBF | 0.8 | 0.0 | 0.856 m | 5.906 m | 6.13 s | 1.853 ms |

## Interpretation

- E5 shows velocity prediction improves clearance over static horizon modeling while preserving the same 0.9 success rate in this dev scenario.
- Stale sensing increases caution but reduces success to 0.8 and increases path length.
- E6 rule adaptation increases mean clearance from 0.485 m to 0.856 m, but also increases path length and reduces success from 0.9 to 0.8.
- This is a useful non-LLM safety comparator: it provides a cautious adaptive baseline that future language-guided methods must beat on both safety and task completion.

## Adaptive Gamma Usage

In the 10-seed E6 dev run, rule-adaptive CBF selected:

```text
gamma=0.08: 601 control steps
gamma=0.04: 12 control steps
gamma=0.02: 0 control steps
```

## Next

- Run 50 seeds for paper-level figures.
- Add a harder scenario if collision-rate separation is needed.
- Compare this Block B rule-adaptive baseline directly against Block C language interfaces.
