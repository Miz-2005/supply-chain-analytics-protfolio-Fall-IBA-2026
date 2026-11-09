# EFERT Phase 4: Reproducible Python network optimisation

## Run

Requires Python 3.10+, `numpy`, `scipy` (tested SciPy 1.17), and the Python standard library.

```bash
pip install -r requirements.txt
python run_phase4.py
python switching_thresholds.py
python test_phase4.py
```

The scripts use `data/` as input and write CSV and JSON to `results/`. Run from any working directory. All files needed are included. No proprietary solver or EFERT company access required.

## Mathematical model

**Decision:** `y_c` is binary and stays constant for the 12-month planning year; `x_{m,p,c,z}` is a nonnegative flow along a plant-DC-zone path. A path is available only if the two leg lead times together meet the service limit. The model requires all monthly zone demand to be delivered, respects plant monthly nameplate capacity, and caps each DC's monthly throughput if opened.

**Objective:** sum of trunk freight, secondary freight and DC handling for all monthly path flows, plus 12 months of fixed facility cost and 12 months of the **provisional static safety-stock holding reserve** for every open DC. Production cost is excluded from both alternatives because the source workbook records zero as an excluded constant, not a verified real cost. Stock-flow balances and physical inventory storage capacity are **not** modelled. A warehouse's monthly throughput limit is not its storage-space limit. The reserve is not recalculated as flow changes. This is a simplified inventory-cost link, not full integrated inventory optimisation.

**Baseline:** all six candidate DCs leased throughout the year, with a service- and capacity-feasible LP flow assignment. This is a hypothetical *six-DC lease counterfactual*, not a documented EFERT as-is network, and not a strict single-source nearest-DC rule. Because the LP minimises the same variable freight/handling costs, it is an optimistic baseline given all six facilities, not a manually forced inefficient routing plan. The 0.367% modelled saving must be described only against this counterfactual. A verified real baseline is unavailable.

**Independent validation:** enumerate all 63 nonempty combinations of six DCs; fix the binary variables to each combination; solve a linear program with SciPy `linprog` HiGHS (distinct API/algorithm from `milp`); compare minimum feasible LP objective to MILP objective. Also check all 12 months × 12 zones for exact demand balance, plant and DC capacities, feasible service paths, nonnegative flows, binary opening decisions, and objective component reconciliation. `test_phase4.py` checks outputs, monthly costs, scenarios and sensitivity coverage.

## Output files

- `summary.json`: headline KPIs, assumptions and audit counts
- `annual_optimal_path_flows.csv`: plant-to-DC-to-zone monthly flows for dashboard map
- `annual_optimal_leg_flows.csv`: aggregated trunk and outbound monthly lanes
- `monthly_cost_breakdown.csv`: monthly freight, handling, fixed, inventory and totals
- `annual_scenarios.csv`: all seven rows (base + six required stresses), including infeasibility
- `five_assumption_sensitivity.csv`: 25 annual re-optimisations across five assumptions
- `switching_thresholds.csv`: approximate bisection thresholds for network changes and feasibility
- `independent_subset_validation.csv`: all feasible DC subsets and objective values
- `numerical_audit.csv`: every optimal and baseline numerical validation

## Critical limitations

1. All network cost, warehouse and service parameters are synthetic or assumed. This is **not EFERT company data**.
2. The 2025 planning year is one year of a 36-month synthetic history; it is not a 36-month optimisation.
3. Inventory safety stock is provisional, not approved as a substitute for the instructor's prior inventory model.
4. Source coordinates and freight costs are approximate, not verified truck-lane distances or quotes.
5. There is no model of direct plant-to-zone delivery, rail, actual customer contracts, dynamic safety-stock response or site-wide Daharki outages.
6. The fixed opening commitment is shared across 12 months; changing the DC network between years is outside scope.
7. Demand spike and Base Plant outage are infeasible in the current model; no emergency supply or lost-sales penalty is included. Never chart infeasible as zero cost.
8. Switching thresholds are numerical approximations within the tested ranges, not company forecasts.
9. Source-verified plant annual nameplate capacity divided by 12 is an assumed monthly availability profile, not measured production.
10. **Dashboard is not included:** Phase 5 is locked until user approval.

Mandatory banner for all Phase 5 pages: `Illustrative model built from public information and synthetic data. Not company data.`
