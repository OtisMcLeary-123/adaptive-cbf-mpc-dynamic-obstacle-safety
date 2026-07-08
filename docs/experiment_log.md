# Experiment Log

## 2026-07-08

- Created Block B as a standalone Git repository scaffold.
- Scope: E5 dynamic obstacle prediction and E6 rule-based adaptive gamma.
- Added local paper corpus manifest for references [5], [9], [10], [11].
- Implemented E5 and E6 with deterministic NumPy random-shooting MPC.
- Ran 10-seed dev benchmark and saved report in `docs/exp_e5_e6_dev_report.md`.
- Added standardized result artifacts for downstream LaMPC/LLM blocks.
- Added E6 fixed gamma baselines `0.15`, `0.08`, and `0.04` plus rule-adaptive CBF.
- Added `aggressive_crossing_v1` hard scenario for stronger safety-margin separation.
- Synced CasADi/IPOPT MPC-CBF backend from Block A into Block B.
- Ran paper-scale E5/E6 50-seed random-shooting suites and 20-seed backend comparison.
- Generated `docs/tables/summary_metrics.md`, `docs/tables/scenario_comparison.md`, `docs/tables/paired_delta.md`, and `docs/paper_section_results.md`.
