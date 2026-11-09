# EFERT | Network Intelligence Dashboard

**MGT-353 Supply Chain Analytics | Illustrative educational optimisation model**

> **Illustrative model built from public information and synthetic data. Not company data.**

This repository contains a hypothetical Sindh/Punjab fertiliser distribution-network optimisation case calibrated to publicly available information about Engro Fertilizers Limited (EFERT). **It is not EFERT’s verified current network**, and the model does not establish actual or realised EFERT savings.

## View the dashboard

Download `dashboard/EFERT_Network_Intelligence_Dashboard.html` and double-click it. It is self-contained and works offline; no server or dependencies required. Interactive filters show the embedded Python-generated result snapshot; the dashboard does not re-run the solver.

## Repository contents

| Folder | Contents |
|---|---|
| `data/` | Populated provisional Excel data pack, original workbook template and 10 CSV datasets |
| `src/` | Phase 3 data generator and Phase 4 annual optimisation, sensitivity, test scripts and requirements |
| `results/` | Solver summaries, monthly costs, modelled flows, scenarios, audit and thresholds |
| `notebooks/` | Google Colab V3 notebook |
| `dashboard/` | Standalone six-page interactive HTML dashboard and frozen data snapshot |
| `assets/` | Preview images and inline network-map PNG |
| `docs/` | Source documentation, logs, QA notes and modelling instructions |

## Model overview

- Two illustrative Daharki production nodes, six candidate distribution centres and twelve regional demand zones.
- Synthetic monthly demand history; 2025 annual planning horizon.
- Fixed-opening mixed-integer network optimisation with plant-to-DC and DC-to-zone flows.
- Six stress scenarios, five-factor sensitivity and conditional network switching thresholds.
- Audit outputs and independent LP checks for feasible DC combinations.

**Displayed illustrative annual results:** six-DC counterfactual baseline approximately PKR 6.261bn; optimised five-DC network approximately PKR 6.238bn; modelled savings approximately PKR 22.96m (0.37%). These are rounded display values. Use `results/summary.json` for precise numerical results.

## Reproduce the analysis

Install packages in `src/requirements.txt`, then run `src/run_phase4.py`, `src/switching_thresholds.py` and `src/test_phase4.py` from a working directory with the expected `data/` inputs. The scripts were preserved from the validated Phase 4 package; their relative-path expectations may require running from the repository root. Alternatively, open the V3 notebook in Google Colab and follow its instructions. See `docs/phase4_README.md` and `docs/Colab_V3_README.md`.

## Evidence and limitations

All quantitative inputs should be interpreted using their `[REAL]`, `[DERIVED]`, `[ASSUMED]` or `[SYNTHETIC]` provenance tags. Data provenance counts are **not** verified-company-data percentages. Road distances are approximations, freight costs are assumed rather than current carrier quotes, candidate DC locations are illustrative, and the inventory reserve is static rather than a dynamic physical stock-flow model. The baseline is a hypothetical six-DC counterfactual, not an observed EFERT network. Infeasible scenarios have no artificial zero cost. The source materials and audit records should be checked before any academic or business reuse.

## Submission note

This repository is a technical project archive. The student's independently prepared verification log and personal limitations/recommendation reflection, where required by the course, are not included or authored by AI. Instructor acceptance of the synthetic inventory substitute and any Power BI-specific delivery requirement should be confirmed separately.
