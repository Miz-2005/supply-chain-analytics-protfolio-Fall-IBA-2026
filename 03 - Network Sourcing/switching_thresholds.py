"""Approximate bisection thresholds; uses exactly the Phase 4 annual MILP."""
from run_phase4 import Model
from pathlib import Path
import csv,json
root=Path(__file__).resolve().parent
m=Model(root/'data');base=m.solve();baseopen=set(base['open_DCs'])

def bisect(key,lo,hi,pred,n=13):
 a,b=lo,hi
 for _ in range(n):
  mid=(a+b)/2;s=m.solve(**{key:mid})
  if pred(s):b=mid
  else:a=mid
 return (a+b)/2,m.solve(**{key:(a+b)/2})
# lower-demand threshold at which the five-DC selection flips to four; start at 70% (4) and 100% (5)
a,b=.7,1.
for _ in range(13):
 mid=(a+b)/2;s=m.solve(demand=mid)
 if s['status']=='OPTIMAL' and set(s['open_DCs'])==baseopen:b=mid
 else:a=mid
four_to_five=(a+b)/2
# reduced capacity threshold at which six becomes five; at 85% six, 100% five
a,b=.85,1.
for _ in range(13):
 mid=(a+b)/2;s=m.solve(capacity=mid)
 if s['status']=='OPTIMAL' and set(s['open_DCs'])==baseopen:b=mid
 else:a=mid
six_to_five=(a+b)/2
# maximal demand multiplier at which model is feasible
a,b=1.,1.15
for _ in range(13):
 mid=(a+b)/2;s=m.solve(demand=mid)
 if s['status']=='OPTIMAL':a=mid
 else:b=mid
max_demand=(a+b)/2
# minimum capacity multiplier for feasible model
a,b=.7,.85
for _ in range(13):
 mid=(a+b)/2;s=m.solve(capacity=mid)
 if s['status']=='OPTIMAL':b=mid
 else:a=mid
min_capacity=(a+b)/2
rows=[{'parameter':'demand','threshold_type':'4-to-5 DC selection transition (approx)','multiplier':four_to_five,'interpretation':'Below threshold fewer DCs can be cost-optimal'},{'parameter':'capacity','threshold_type':'6-to-5 DC selection transition (approx)','multiplier':six_to_five,'interpretation':'Lower DC capacity can force opening the sixth DC'},{'parameter':'demand','threshold_type':'maximum feasible demand (approx)','multiplier':max_demand,'interpretation':'Above threshold plant or DC capacity insufficient'},{'parameter':'capacity','threshold_type':'minimum feasible DC throughput multiplier (approx)','multiplier':min_capacity,'interpretation':'Below threshold combined DC throughput insufficient'}]
with (root/'results'/'switching_thresholds.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0])+['tag']);w.writeheader();w.writerows([{**r,'tag':'[DERIVED]'} for r in rows])
print(json.dumps(rows,indent=2))
