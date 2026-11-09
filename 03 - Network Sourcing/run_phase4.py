"""EFERT synthetic network: reproducible 12-month fixed-open MILP, LP baseline, scenario and audit.
Run: python run_phase4.py --input /path/to/EFERT_Phase3 --output /path/to/results
No actual EFERT freight, warehouse, or inventory data. SciPy HiGHS required.
"""
import argparse,csv,json,itertools,math
from pathlib import Path
from collections import defaultdict
import numpy as np
from scipy.optimize import milp,linprog,Bounds,LinearConstraint
from scipy.sparse import coo_matrix

PARSER=argparse.ArgumentParser();PARSER.add_argument('--input',default=str(Path(__file__).resolve().parent/'data'));PARSER.add_argument('--output',default=str(Path(__file__).resolve().parent/'results'))

def read(root,name):
 with open(root/(name+'.csv'),newline='') as f:return list(csv.DictReader(f))
def write(path,rows,columns):
 with open(path,'w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=columns);w.writeheader();w.writerows(rows)
def val(row,key):return float(row[key])

class Model:
 def __init__(self,root):
  self.root=root; self.plants=read(root,'supply');self.dcs=read(root,'dc_costs');self.demrows=read(root,'demand_monthly');self.rates=read(root,'freight_rates');self.service=read(root,'service');self.inv=read(root,'inventory_params');self.scenarios=read(root,'scenarios')
  self.P=[r['plant_id'] for r in self.plants];self.C=[r['candidate_id'] for r in self.dcs];self.Z=sorted({r['zone_id'] for r in self.demrows});self.M=sorted({r['month'] for r in self.demrows if r['month'].startswith('2025')})
  assert len(self.M)==12 and len(self.C)==6 and len(self.P)==2
  self.capP={r['plant_id']:val(r,'capacity_per_month') for r in self.plants};self.capC={r['candidate_id']:val(r,'capacity') for r in self.dcs};self.fixed={r['candidate_id']:val(r,'fixed_cost_per_month') for r in self.dcs};self.hand={r['candidate_id']:val(r,'handling_cost_per_unit') for r in self.dcs}
  self.dem={(r['month'],r['zone_id']):val(r,'demand_units') for r in self.demrows};self.rate={(r['from'],r['to']):val(r,'rate_per_unit') for r in self.rates};self.lead={(r['from'],r['to']):val(r,'lead_time_days') for r in self.service}
  pars={r['parameter']:val(r,'value') for r in self.inv};self.ss={c:pars[c+'.safety_stock'] for c in self.C};self.hold={c:pars[c+'.holding_cost_per_tonne_month'] for c in self.C}
  # Path variables guarantee BOTH legs belong to the same origin-to-destination service-compliant route.
  self.paths=[(p,c,z) for p in self.P for c in self.C for z in self.Z]
  self.xkeys=[(m,p,c,z) for m in self.M for p,c,z in self.paths];self.nx=len(self.xkeys);self.n=self.nx+len(self.C);self.yidx={c:self.nx+i for i,c in enumerate(self.C)}
  self.by_mz=defaultdict(list);self.by_mp=defaultdict(list);self.by_mc=defaultdict(list);self.by_c=defaultdict(list)
  for i,(m,p,c,z) in enumerate(self.xkeys):self.by_mz[m,z].append(i);self.by_mp[m,p].append(i);self.by_mc[m,c].append(i);self.by_c[c].append(i)
 def solve(self,freight=1,demand=1,plant=None,fixed=1,capacity=1,holding=1,days=5,method='milp',force_open=None,baseline=False):
  plant=plant or {};n=self.n;cost=np.zeros(n)
  for i,(m,p,c,z) in enumerate(self.xkeys):cost[i]=freight*(self.rate[p,c]+self.rate[c,z])+self.hand[c]
  for c in self.C:cost[self.yidx[c]]=12*(fixed*self.fixed[c]+holding*self.ss[c]*self.hold[c])
  upper=np.full(n,np.inf);upper[self.nx:]=1
  for i,(m,p,c,z) in enumerate(self.xkeys):
   if self.lead[p,c]+self.lead[c,z]>days:upper[i]=0
  if force_open is not None:
   for c in self.C:upper[self.yidx[c]]=1 if c in force_open else 0
  # Constraints: every month-zone met, each plant capacity, each DC throughput capacity conditional on opening.
  rows=[];cols=[];vals=[];lb=[];ub=[]
  def add(entries,low,high):
   k=len(lb)
   for j,v in entries:rows.append(k);cols.append(j);vals.append(v)
   lb.append(low);ub.append(high)
  for m in self.M:
   for z in self.Z:add([(i,1) for i in self.by_mz[m,z]],self.dem[m,z]*demand,self.dem[m,z]*demand)
   for p in self.P:add([(i,1) for i in self.by_mp[m,p]],-np.inf,self.capP[p]*plant.get(p,1))
   for c in self.C:add([(i,1) for i in self.by_mc[m,c]]+[(self.yidx[c],-self.capC[c]*capacity)],-np.inf,0)
  A=coo_matrix((vals,(rows,cols)),shape=(len(lb),n)).tocsr()
  if method=='milp':
   integ=np.zeros(n);integ[self.nx:]=1
   lower=np.zeros(n)
   if force_open is not None:
    for c in self.C:lower[self.yidx[c]]=1 if c in force_open else 0
   res=milp(cost,integrality=integ,bounds=Bounds(lower,upper),constraints=LinearConstraint(A,lb,ub),options={'time_limit':100,'mip_rel_gap':1e-8})
  else:
   if force_open is None:raise ValueError('LP needs fixed opening decisions')
   # Fix y=1 for all open and y=0 for others, even if no flow; annual lease commitment.
   bounds=[(0,None if np.isinf(u) else u) for u in upper[:self.nx]]+[(int(c in force_open),int(c in force_open)) for c in self.C]
   res=linprog(cost,A_ub=A[[i for i,l in enumerate(lb) if np.isneginf(l)]],b_ub=np.array(ub)[[i for i,l in enumerate(lb) if np.isneginf(l)]],A_eq=A[[i for i,l in enumerate(lb) if not np.isneginf(l)]],b_eq=np.array(ub)[[i for i,l in enumerate(lb) if not np.isneginf(l)]],bounds=bounds,method='highs')
  if res.x is None or not res.success:return {'status':'INFEASIBLE' if int(res.status)==2 else 'UNSOLVED','solver_message':str(res.message),'objective_PKR':None,'open_DCs':[],'raw':None}
  x=res.x;opened=[c for c in self.C if x[self.yidx[c]]>.5]
  var=float(np.dot(cost[:self.nx],x[:self.nx]));fac=sum(12*fixed*self.fixed[c] for c in opened);inventory=sum(12*holding*self.ss[c]*self.hold[c] for c in opened)
  result={'status':'OPTIMAL','solver_message':str(res.message),'objective_PKR':float(res.fun),'variable_PKR':var,'fixed_PKR':fac,'inventory_PKR':inventory,'open_DCs':opened,'demand_tonnes':sum(self.dem[m,z] for m in self.M for z in self.Z)*demand,'mip_gap':float(getattr(res,'mip_gap',0)) if method=='milp' else None,'raw':x}
  return result
 def audit(self,sol,demand=1,plant=None,capacity=1,days=5):
  if sol['raw'] is None:return {'status':'NOT_TESTABLE'}
  x=sol['raw'];plant=plant or {};checks=[]
  def check(name,error,tol=1e-5):checks.append({'check':name,'residual':float(error),'passed':bool(error<=tol)})
  check('Objective reconciliation PKR',abs(sol['objective_PKR']-sol['variable_PKR']-sol['fixed_PKR']-sol['inventory_PKR']),.1)
  for m in self.M:
   for z in self.Z:check('Demand '+m+' '+z,abs(sum(x[i] for i in self.by_mz[m,z])-self.dem[m,z]*demand),.01)
   for p in self.P:check('Plant capacity '+m+' '+p,max(0,sum(x[i] for i in self.by_mp[m,p])-self.capP[p]*plant.get(p,1)),.01)
   for c in self.C:check('DC throughput '+m+' '+c,max(0,sum(x[i] for i in self.by_mc[m,c])-self.capC[c]*capacity*x[self.yidx[c]]),.01)
  check('Path service feasibility',sum(x[i] for i,(m,p,c,z) in enumerate(self.xkeys) if self.lead[p,c]+self.lead[c,z]>days),.01)
  check('DC binary residual',max(abs(x[self.yidx[c]]-round(x[self.yidx[c]])) for c in self.C))
  check('No negative shipments',max(0,-float(min(x[:self.nx]))))
  return {'status':'PASS' if all(t['passed'] for t in checks) else 'FAIL','passed':sum(t['passed'] for t in checks),'total':len(checks),'checks':checks}

def main():
 a=PARSER.parse_args();root=Path(a.input);out=Path(a.output);out.mkdir(parents=True,exist_ok=True);model=Model(root)
 base=model.solve();assert base['status']=='OPTIMAL',base
 # As-is benchmark is an explicitly ASSUMED six-DC lease, with nearest-cost-feasible flow allocation.
 baseline=model.solve(method='lp',force_open=set(model.C));assert baseline['status']=='OPTIMAL'
 audit=model.audit(base);auditbase=model.audit(baseline);assert audit['status']==auditbase['status']=='PASS'
 # Independent exhaustive 63 subsets, each fixed-opening LP, independently confirms global optimum.
 winners=[]
 for k in range(1,1<<len(model.C)):
  selected={c for i,c in enumerate(model.C) if k&(1<<i)}
  s=model.solve(method='lp',force_open=selected)
  if s['status']=='OPTIMAL':winners.append((s['objective_PKR'],tuple(sorted(selected))))
 winners.sort();independent=winners[0];gap=abs(independent[0]-base['objective_PKR']);assert gap<.2,(gap,independent,base['objective_PKR'])
 # Scenario definitions come directly from the approved Phase 3 scenarios.csv.
 scen=[]
 for r in model.scenarios:
  sid=r['scenario_id'];opts={}
  if sid=='S01':opts['freight']=float(r['scenario_value'])
  if sid=='S02' or sid=='S03':opts['demand']=float(r['scenario_value'])
  if sid=='S04':opts['plant']={'P01':float(r['scenario_value'])}
  if sid=='S05':opts['days']=float(r['scenario_value'])
  if sid=='S06':opts['fixed']=float(r['scenario_value'])
  s=model.solve(**opts);chk=model.audit(s,demand=opts.get('demand',1),plant=opts.get('plant'),days=opts.get('days',5)) if s['status']=='OPTIMAL' else {'status':'NOT_APPLICABLE'}
  assert chk['status'] in ('PASS','NOT_APPLICABLE')
  scen.append({'scenario_id':sid,'scenario':r['scenario_name'],'status':s['status'],'cost_PKR':s['objective_PKR'],'demand_tonnes':sum(model.dem[m,z] for m in model.M for z in model.Z)*opts.get('demand',1),'selected_DCs':','.join(s['open_DCs']),'audit':chk['status'],'tag':'[DERIVED]','method_or_source':'12-month fixed-opening MILP; Phase 3 assumed scenarios'})
 # Sensitivities: 5 inputs, five levels each, true annual re-solves.
 sensitivity=[]
 for key in ['freight','fixed','capacity','demand','holding']:
  for mult in [.70,.85,1,1.15,1.30]:
   s=model.solve(**{key:mult});sensitivity.append({'parameter':key,'multiplier':mult,'status':s['status'],'annual_cost_PKR':s['objective_PKR'],'delta_PKR':s['objective_PKR']-base['objective_PKR'] if s['objective_PKR'] is not None else None,'selected_DCs':','.join(s['open_DCs']),'network_flip':s['status']=='OPTIMAL' and set(s['open_DCs'])!=set(base['open_DCs']),'tag':'[DERIVED]'})
 # Extract 12-month path flows; aggregated legs for network-map visualizations.
 pathrows=[];leg=defaultdict(float);monthly=defaultdict(lambda:defaultdict(float))
 for i,(m,p,c,z) in enumerate(model.xkeys):
  t=float(base['raw'][i]);
  if t<=.0001:continue
  pathrows.append({'month':m,'plant':p,'dc':c,'zone':z,'tonnes':round(t,6),'service_days':model.lead[p,c]+model.lead[c,z],'tag':'[DERIVED]','method_or_source':'Joint annual path MILP'})
  leg[m,p,c]+=t;leg[m,c,z]+=t;monthly[m]['freight_PKR']+=t*(model.rate[p,c]+model.rate[c,z]);monthly[m]['handling_PKR']+=t*model.hand[c];monthly[m]['tonnes']+=t
 for m in model.M:
  monthly[m]['fixed_PKR']=sum(model.fixed[c] for c in base['open_DCs']);monthly[m]['inventory_PKR']=sum(model.ss[c]*model.hold[c] for c in base['open_DCs']);monthly[m]['total_PKR']=sum(monthly[m][k] for k in ['freight_PKR','handling_PKR','fixed_PKR','inventory_PKR'])
 summary={'model':'Path-indexed 12-month fixed-open MILP','solver':'SciPy HiGHS milp','independent_method':'Exhaustive 63 subsets with independent fixed-open HiGHS LP','independent_feasible_subsets':len(winners),'independent_optimum_PKR':independent[0],'independent_open_DCs':list(independent[1]),'independent_gap_PKR':gap,'baseline_definition':'Illustrative as-is: all six candidate DCs leased for 12 months, with minimum freight-and-handling flow assignment subject to service/capacity; NOT actual EFERT as-is. This is a relaxed nearest-cost-feasible benchmark, not strict single-zone nearest assignment.','baseline_PKR':baseline['objective_PKR'],'optimal_PKR':base['objective_PKR'],'savings_PKR':baseline['objective_PKR']-base['objective_PKR'],'savings_pct':100*(baseline['objective_PKR']-base['objective_PKR'])/baseline['objective_PKR'],'annual_tonnes':base['demand_tonnes'],'open_DCs':base['open_DCs'],'cost_components_PKR':{k:base[k] for k in ['variable_PKR','fixed_PKR','inventory_PKR']},'audit':{'optimal':{'passed':audit['passed'],'total':audit['total']},'baseline':{'passed':auditbase['passed'],'total':auditbase['total']}},'inventory_method':'Provisional DC safety stock and monthly holding rate included as fixed reserve per opened DC. No physical inventory storage-capacity constraint because throughput capacity is not storage capacity; no dynamic stock-flow or reorder-point balance.','provenance':'[DERIVED] from Phase 3 synthetic and assumed inputs, not company operating results','limitations':['Synthetic inventory model requires instructor acceptance','Warehouse throughput capacity is not storage capacity','Freight routes are circuity estimates, not verified truck lanes','All six baseline DC leases are a counterfactual assumption, not observed EFERT current network','Production costs excluded equally from both alternatives','36 months of history; 12 months (2025) used for decision horizon']}
 write(out/'annual_optimal_path_flows.csv',pathrows,['month','plant','dc','zone','tonnes','service_days','tag','method_or_source'])
 write(out/'annual_optimal_leg_flows.csv',[{'month':m,'from':p,'to':c,'tonnes':round(t,6),'tag':'[DERIVED]'} for (m,p,c),t in leg.items()],['month','from','to','tonnes','tag'])
 write(out/'monthly_cost_breakdown.csv',[{'month':m,**{k:round(v,4) for k,v in monthly[m].items()},'tag':'[DERIVED]'} for m in model.M],['month','freight_PKR','handling_PKR','tonnes','fixed_PKR','inventory_PKR','total_PKR','tag'])
 write(out/'annual_scenarios.csv',scen,list(scen[0]))
 write(out/'five_assumption_sensitivity.csv',sensitivity,list(sensitivity[0]))
 write(out/'independent_subset_validation.csv',[{'cost_PKR':v,'open_DCs':','.join(s),'tag':'[DERIVED]'} for v,s in winners],['cost_PKR','open_DCs','tag'])
 write(out/'numerical_audit.csv',[{'solution':'optimal',**r} for r in audit['checks']]+[{'solution':'baseline',**r} for r in auditbase['checks']],['solution','check','residual','passed'])
 (out/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
