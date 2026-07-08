# E6 Paired Delta Table

Deltas are matched by seed and computed as `Rule adaptive CBF - fixed baseline`.

| Suite | Scenario | Backend | Baseline | Seeds | Δsuccess | Δcollision | Δclearance | Δpath length | Δsolve time |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| extended/backend_comparison/casadi | point_mass_2d_dynamic_obstacle_v1 | casadi | Fixed CBF gamma=0.15 | 20 | 0.000 ± 0.000 | 0.000 ± 0.000 | 0.211 ± 0.020 | 0.207 ± 0.013 | 2.740 ± 0.927 |
| extended/backend_comparison/casadi | point_mass_2d_dynamic_obstacle_v1 | casadi | Fixed CBF gamma=0.08 | 20 | 0.000 ± 0.000 | 0.000 ± 0.000 | -0.152 ± 0.021 | -0.098 ± 0.010 | 2.910 ± 0.105 |
| extended/backend_comparison/casadi | point_mass_2d_dynamic_obstacle_v1 | casadi | Fixed CBF gamma=0.04 | 20 | 0.000 ± 0.000 | 0.000 ± 0.000 | -0.609 ± 0.017 | -0.687 ± 0.031 | 2.949 ± 0.093 |
| extended/backend_comparison/random_shooting | point_mass_2d_dynamic_obstacle_v1 | random_shooting | Fixed CBF gamma=0.15 | 20 | 0.000 ± 0.246 | 0.000 ± 0.000 | 0.365 ± 0.032 | 0.382 ± 0.422 | 0.006 ± 0.011 |
| extended/backend_comparison/random_shooting | point_mass_2d_dynamic_obstacle_v1 | random_shooting | Fixed CBF gamma=0.08 | 20 | 0.000 ± 0.201 | 0.000 ± 0.000 | 0.029 ± 0.018 | -0.022 ± 0.380 | 0.004 ± 0.009 |
| extended/backend_comparison/random_shooting | point_mass_2d_dynamic_obstacle_v1 | random_shooting | Fixed CBF gamma=0.04 | 20 | -0.050 ± 0.224 | 0.000 ± 0.000 | -0.190 ± 0.021 | -0.511 ± 0.383 | 0.017 ± 0.012 |
| extended/scenarios/aggressive_crossing_v1_random_shooting | aggressive_crossing_v1 | random_shooting | Fixed CBF gamma=0.15 | 50 | 0.000 ± 0.000 | 0.000 ± 0.000 | 0.167 ± 0.040 | 0.348 ± 0.064 | 0.002 ± 0.007 |
| extended/scenarios/aggressive_crossing_v1_random_shooting | aggressive_crossing_v1 | random_shooting | Fixed CBF gamma=0.08 | 50 | 0.000 ± 0.000 | 0.000 ± 0.000 | 0.059 ± 0.008 | 0.069 ± 0.012 | 0.004 ± 0.004 |
| extended/scenarios/aggressive_crossing_v1_random_shooting | aggressive_crossing_v1 | random_shooting | Fixed CBF gamma=0.04 | 50 | 0.000 ± 0.000 | 0.000 ± 0.000 | -0.007 ± 0.010 | 0.012 ± 0.030 | 0.004 ± 0.003 |
| extended/scenarios/fast_crossing_v1_random_shooting | fast_crossing_v1 | random_shooting | Fixed CBF gamma=0.15 | 50 | 0.000 ± 0.000 | 0.000 ± 0.000 | 0.088 ± 0.029 | 0.175 ± 0.035 | 0.007 ± 0.004 |
| extended/scenarios/fast_crossing_v1_random_shooting | fast_crossing_v1 | random_shooting | Fixed CBF gamma=0.08 | 50 | 0.000 ± 0.000 | 0.000 ± 0.000 | 0.030 ± 0.013 | 0.051 ± 0.013 | 0.002 ± 0.003 |
| extended/scenarios/fast_crossing_v1_random_shooting | fast_crossing_v1 | random_shooting | Fixed CBF gamma=0.04 | 50 | 0.000 ± 0.000 | 0.000 ± 0.000 | -0.007 ± 0.010 | -0.003 ± 0.019 | 0.005 ± 0.004 |
| extended/scenarios/head_on_v1_random_shooting | head_on_v1 | random_shooting | Fixed CBF gamma=0.15 | 50 | 0.000 ± 0.000 | 0.000 ± 0.000 | 0.448 ± 0.018 | 0.489 ± 0.024 | -0.011 ± 0.009 |
| extended/scenarios/head_on_v1_random_shooting | head_on_v1 | random_shooting | Fixed CBF gamma=0.08 | 50 | 0.000 ± 0.000 | 0.000 ± 0.000 | 0.061 ± 0.011 | 0.052 ± 0.020 | -0.009 ± 0.005 |
| extended/scenarios/head_on_v1_random_shooting | head_on_v1 | random_shooting | Fixed CBF gamma=0.04 | 50 | 0.000 ± 0.000 | 0.000 ± 0.000 | -0.105 ± 0.012 | -0.059 ± 0.021 | -0.006 ± 0.006 |
| extended/scenarios/late_crossing_v1_random_shooting | late_crossing_v1 | random_shooting | Fixed CBF gamma=0.15 | 50 | 0.000 ± 0.000 | 0.000 ± 0.000 | 0.433 ± 0.013 | 0.666 ± 0.034 | 0.013 ± 0.005 |
| extended/scenarios/late_crossing_v1_random_shooting | late_crossing_v1 | random_shooting | Fixed CBF gamma=0.08 | 50 | 0.000 ± 0.000 | 0.000 ± 0.000 | 0.060 ± 0.009 | 0.055 ± 0.013 | 0.006 ± 0.003 |
| extended/scenarios/late_crossing_v1_random_shooting | late_crossing_v1 | random_shooting | Fixed CBF gamma=0.04 | 50 | 0.000 ± 0.000 | 0.000 ± 0.000 | -0.196 ± 0.018 | -0.382 ± 0.048 | 0.006 ± 0.003 |
| extended/scenarios/noisy_prediction_v1_random_shooting | noisy_prediction_v1 | random_shooting | Fixed CBF gamma=0.15 | 50 | 0.000 ± 0.000 | 0.000 ± 0.000 | 0.349 ± 0.032 | 0.424 ± 0.098 | -0.014 ± 0.010 |
| extended/scenarios/noisy_prediction_v1_random_shooting | noisy_prediction_v1 | random_shooting | Fixed CBF gamma=0.08 | 50 | 0.000 ± 0.000 | 0.000 ± 0.000 | 0.046 ± 0.011 | 0.038 ± 0.083 | -0.010 ± 0.008 |
| extended/scenarios/noisy_prediction_v1_random_shooting | noisy_prediction_v1 | random_shooting | Fixed CBF gamma=0.04 | 50 | 0.000 ± 0.000 | 0.000 ± 0.000 | -0.173 ± 0.036 | -0.208 ± 0.121 | -0.013 ± 0.007 |
| extended/scenarios/point_mass_2d_dynamic_obstacle_v1_random_shooting | point_mass_2d_dynamic_obstacle_v1 | random_shooting | Fixed CBF gamma=0.15 | 50 | -0.080 ± 0.146 | 0.000 ± 0.000 | 0.362 ± 0.016 | 0.540 ± 0.289 | -0.002 ± 0.005 |
| extended/scenarios/point_mass_2d_dynamic_obstacle_v1_random_shooting | point_mass_2d_dynamic_obstacle_v1 | random_shooting | Fixed CBF gamma=0.08 | 50 | -0.060 ± 0.118 | 0.000 ± 0.000 | 0.030 ± 0.010 | 0.170 ± 0.223 | -0.006 ± 0.006 |
| extended/scenarios/point_mass_2d_dynamic_obstacle_v1_random_shooting | point_mass_2d_dynamic_obstacle_v1 | random_shooting | Fixed CBF gamma=0.04 | 50 | -0.060 ± 0.142 | 0.000 ± 0.000 | -0.181 ± 0.014 | -0.253 ± 0.245 | 0.008 ± 0.005 |
| paper_main/e6_adaptive_50_seed | point_mass_2d_dynamic_obstacle_v1 | random_shooting | Fixed CBF gamma=0.15 | 50 | -0.080 ± 0.146 | 0.000 ± 0.000 | 0.362 ± 0.016 | 0.540 ± 0.289 | -0.016 ± 0.010 |
| paper_main/e6_adaptive_50_seed | point_mass_2d_dynamic_obstacle_v1 | random_shooting | Fixed CBF gamma=0.08 | 50 | -0.060 ± 0.118 | 0.000 ± 0.000 | 0.030 ± 0.010 | 0.170 ± 0.223 | -0.009 ± 0.008 |
| paper_main/e6_adaptive_50_seed | point_mass_2d_dynamic_obstacle_v1 | random_shooting | Fixed CBF gamma=0.04 | 50 | -0.060 ± 0.142 | 0.000 ± 0.000 | -0.181 ± 0.014 | -0.253 ± 0.245 | -0.005 ± 0.008 |
