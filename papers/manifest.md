# Block B Paper Corpus Manifest

This directory stores the local reading corpus for Block B. PDF files are kept locally and ignored by Git to avoid redistributing papers on GitHub. This manifest records source links, local filenames, and how each paper supports the experiments.

Source reference list:

```text
/home/otismcleary/Documents/paper/Safety-Aware_Optimal_Control_With_Language-Guided_Online_Parameter_Adjustment_via_Large_Language_Models.pdf
```

## Downloaded PDFs

| Ref | Local file | Source URL | Used by | SHA-256 |
|---|---|---|---|---|
| [5] | `ref05_jian_2023_dynamic_cbf_mpc.pdf` | https://arxiv.org/pdf/2209.08539 | E5 | `f610d8234b6841569db0d6a654cbb3c4359a6fa5e1c044350722787cde3081b2` |
| [9] | `ref09_kim_2024_uncertainty_aware_online_cbf_adaptation.pdf` | https://arxiv.org/pdf/2409.14616 | E6 | `5c21961c0c571f039f36ff760e6a9bc29f8f93042ba9778030094cbdb9861cc0` |
| [10] | `ref10_zhang_2024_online_safety_critical_dynamic_obstacles.pdf` | https://arxiv.org/pdf/2402.16449 | E5, E6 | `1458e8a8b5879dbf37c6d831912d9c453b10f1026f5153b02adf60651d8c6c5e` |
| [11] | `ref11_parwana_2022_trust_based_rate_tunable_cbf.pdf` | https://arxiv.org/pdf/2204.04555 | E6 | `1a5d96ec2b9ca28ca7fb726d487b0df9bc47576dfbbbd49c47acecdad40f3f69` |

## Notes

- Do not commit PDF files unless the license explicitly allows redistribution and the repo policy is updated.
- Prefer arXiv, official conference proceedings, author pages, institutional repositories, and publisher open-access pages.
- Block B uses these papers to implement a non-LLM adaptive safety comparator before testing language-guided adaptation.
