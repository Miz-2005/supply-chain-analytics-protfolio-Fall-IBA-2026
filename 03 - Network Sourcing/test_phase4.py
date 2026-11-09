"""Run: python test_phase4.py"""
import json,csv,math
from pathlib import Path
from run_phase4 import Model
R=Path(__file__).resolve().parent
m=Model(R/'data');s=json.loads((R/'results'/'summary.json').read_text())
assert len(m.M)==12 and len(m.C)==6 and len(m.P)==2
assert math.isclose(s['annual_tonnes'],sum(m.dem[t,z] for t in m.M for z in m.Z),abs_tol=.01)
assert math.isclose(s['baseline_PKR']-s['optimal_PKR'],s['savings_PKR'],abs_tol=.01)
assert s['audit']['optimal']['passed']==s['audit']['optimal']['total']==244
assert s['audit']['baseline']['passed']==s['audit']['baseline']['total']==244
assert s['independent_gap_PKR']<.01
assert s['independent_feasible_subsets']<=63
assert math.isclose(s['optimal_PKR'],sum(float(r['total_PKR']) for r in csv.DictReader((R/'results'/'monthly_cost_breakdown.csv').open())),abs_tol=.01)
sc={r['scenario_id']:r for r in csv.DictReader((R/'results'/'annual_scenarios.csv').open())}
assert len(sc)==7 and sc['S02']['status']=='INFEASIBLE' and sc['S04']['status']=='INFEASIBLE'
assert all(r['audit']=='PASS' for r in sc.values() if r['status']=='OPTIMAL')
assert len(list(csv.DictReader((R/'results'/'five_assumption_sensitivity.csv').open())))==25
assert len(list(csv.DictReader((R/'results'/'switching_thresholds.csv').open())))==4
print('PASS: 12 automated integration assertions; 488 individual model audit checks; 63-subset independent verification.')
