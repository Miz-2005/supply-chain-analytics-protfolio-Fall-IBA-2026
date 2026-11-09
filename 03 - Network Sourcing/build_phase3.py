import csv,math,random,calendar,zipfile,os
from datetime import date
from artifact_tool import Blob,SpreadsheetFile
O='/mnt/data/EFERT_Phase3';os.makedirs(O,exist_ok=True)
wb=SpreadsheetFile.import_xlsx(Blob.load('/mnt/data/EFERT_Network_Optimisation_Data_Pack.xlsx'))
rng=random.Random(42)
plants=[('P01','Base Plant','Daharki',28.02,69.11,975000),('P02','EnVen Plant','Daharki',28.02,69.11,1300000)]
dcs=[('DC01','Sukkur',27.71,68.84,30),('DC02','Hyderabad',25.40,68.36,35),('DC03','Rahim Yar Khan',28.42,70.30,32),('DC04','Multan',30.20,71.47,30),('DC05','Faisalabad',31.42,73.08,40),('DC06','Lahore',31.55,74.34,55)]
zones=[('Z01','Sukkur',27.71,68.84,8),('Z02','Larkana',27.56,68.21,7),('Z03','Nawabshah',26.25,68.41,7),('Z04','Hyderabad',25.40,68.36,10),('Z05','Mirpur Khas',25.53,69.01,8),('Z06','Rahim Yar Khan',28.42,70.30,8),('Z07','Bahawalpur',29.40,71.68,8),('Z08','Multan',30.20,71.47,11),('Z09','Dera Ghazi Khan',30.05,70.64,7),('Z10','Sahiwal',30.67,73.11,8),('Z11','Faisalabad',31.42,73.08,10),('Z12','Lahore',31.55,74.34,8)]
# Zone weights are deliberately illustrative, NOT province market shares.
headers={
'nodes':['node_id','name','type','city','lat','lon','status','tag','method_or_source','verification'],
'demand_monthly':['month','zone_id','demand_units','seasonality_index','trend_factor','noise_factor','event','tag','method_or_source','seed'],
'supply':['plant_id','plant_name','capacity_per_month','variable_cost_per_unit','minimum_commitment','unit','tag','method_or_source','low','high','verification'],
'distances':['from','to','straight_line_km','circuity_factor','road_km','method','tag','method_or_source','verification'],
'freight_rates':['from','to','mode','rate_per_unit','rate_per_unit_km','truck_capacity','fuel_index','return_load_factor','tag','method_or_source','low','high','verification'],
'dc_costs':['candidate_id','city','fixed_cost_per_month','handling_cost_per_unit','capacity','lease_term','tag','method_or_source','low','high','verification'],
'inventory_params':['parameter','value','unit','tag','source_model_cell','method_or_source','low','high','verification','notes'],
'service':['from','to','lead_time_days','OTIF_target','max_acceptable_delivery_days','tag','method_or_source','low','high','verification'],
'rules':['rule_id','rule_type','description','parameter','value','unit','tag','method_or_source','low','high','verification'],
'scenarios':['scenario_id','scenario_name','parameter_changed','base_value','scenario_value','change_pct','tag','method_or_source','approved']}
rows={k:[] for k in headers}
source='PACRA July 2026 plant capacity (Phase 1); city coordinates approximate [ASSUMED], require geocoding'
for pid,name,city,lat,lon,cap in plants:rows['nodes'].append([pid,name,'plant',city,lat,lon,'verified production site','[ASSUMED]',source,'plant verified; coordinate unverified'])
for id,city,lat,lon,rent in dcs:rows['nodes'].append([id,city+' candidate DC','dc',city,lat,lon,'candidate only','[ASSUMED]','Phase 2 approved city; approximate centre coordinates','not site-verified'])
for id,city,lat,lon,w in zones:rows['nodes'].append([id,city+' demand zone','zone',city,lat,lon,'synthetic zone centre','[ASSUMED]','Phase 2 zone centre; approximate city coordinate','zone boundaries unverified'])
# Capacity and demand deliberately constrained to below 2.275m tonnes per year, not national sales.
for pid,name,city,lat,lon,cap in plants:rows['supply'].append([pid,name,round(cap/12,2),0,0,'tonnes/month','[DERIVED]','PACRA annual nameplate / 12; zero production cost is excluded constant, NOT a true cost',round(cap/12,2),round(cap/12,2),'capacity verified; monthly availability assumed'])
season=[0.90,0.92,0.96,1.04,1.12,1.16,1.10,1.04,0.98,0.92,0.91,0.95];season=[v/(sum(season)/12) for v in season]
annual_region=1700000 # assumed; deliberately not inferred as actual EFERT regional sales
for year in [2023,2024,2025]:
 for m in range(1,13):
  trend=1+0.012*(year-2024)
  for zid,city,lat,lon,wt in zones:
   noise=max(.75,min(1.25,rng.gauss(1,.09)))
   event='synthetic demand shock' if year==2024 and m==8 else 'none'
   shock=.94 if event!='none' else 1
   vol=annual_region/12*(wt/100)*season[m-1]*trend*noise*shock
   rows['demand_monthly'].append([f'{year}-{m:02}',zid,round(vol,2),round(season[m-1],5),round(trend,4),round(noise,5),event,'[SYNTHETIC]','Seed 42; 1.70m t annual regional target [ASSUMED]; zone weights; normalized seasonality; 9% noise; 2024-08 shock',42])
def hav(a,b):
 lat1,lon1=a;lat2,lon2=b;dlat=math.radians(lat2-lat1);dlon=math.radians(lon2-lon1)
 return 6371*2*math.asin(min(1,math.sqrt(math.sin(dlat/2)**2+math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlon/2)**2)))
lookup={r[0]:(r[3],r[4]) for r in plants};lookup.update({r[0]:(r[2],r[3]) for r in dcs});lookup.update({r[0]:(r[2],r[3]) for r in zones})
lanes=[(p[0],d[0]) for p in plants for d in dcs]+[(d[0],z[0]) for d in dcs for z in zones]
for a,b in lanes:
 km=hav(lookup[a],lookup[b]);road=max(10,km*1.3) # local minimum for same-city warehouse to zone
 rows['distances'].append([a,b,round(km,2),1.3,round(road,2),'haversine x 1.30; min 10km local','[DERIVED]','Approximate city coords [ASSUMED]; road circuity 1.30 [ASSUMED]; NOT road-map verified','requires route verification'])
 # 8 PKR/t-km indicative contemporary ASSUMPTION; no claim market quote
 rate=8.0*road; rows['freight_rates'].append([a,b,'road',round(rate,2),8,25,1,1,'[ASSUMED]','PKR 8/t-km assumed (historical NTRC 2022 ~5.75-5.86; no current fertilizer quote); 25t truck; no return-load discount',round(rate*.7,2),round(rate*1.5,2),'no current lane quotation'])
 days=max(1,math.ceil(road/350));rows['service'].append([a,b,days,.95,5,'[ASSUMED]','350 road km/day planning allowance; 95% OTIF goal; max 5 days',max(1,days-1),days+1,'unverified service target'])
for id,city,lat,lon,rent in dcs:
 area=20000;fixed=area*rent+300000;cap=35000
 rows['dc_costs'].append([id,city,fixed,125,cap,'12 months','[ASSUMED]',f'20,000 sq ft x PKR {rent}/sq ft/month + 300,000 overhead; 125 PKR/t handling; 35,000 t/month capacity',round(fixed*.7),round(fixed*1.5),'listing-derived context; hypothetical facility'])
# Inventory parameters: one row per DC, aligned to max DC throughput and 4 day replenishment assumption
from statistics import NormalDist
z=NormalDist().inv_cdf(.95)
for id,city,lat,lon,rent in dcs:
 cap=35000;mu=cap/30*.70;sd=mu*.20;L=4;sdL=1
 ss=z*math.sqrt(L*sd**2+mu**2*sdL**2);rop=mu*L+ss
 for param,value,unit,lo,hi,tag,method in [
  ('daily_demand_mean',round(mu,3),'tonnes/day',mu*.5,mu,'[ASSUMED]','70% of illustrative DC throughput /30'),
  ('daily_demand_sd',round(sd,3),'tonnes/day',sd*.5,sd*1.75,'[ASSUMED]','20% daily demand CV'),
  ('lead_time_mean',L,'days',2,7,'[ASSUMED]','Illustrative replenishment time'),
  ('lead_time_sd',sdL,'days',.5,2,'[ASSUMED]','Illustrative lead-time uncertainty'),
  ('service_level',.95,'probability',.90,.98,'[ASSUMED]','Illustrative cycle service level'),
  ('inventory_value',60000,'PKR/tonne',45000,80000,'[ASSUMED]','Not a verified production cost; distinct from retail selling price'),
  ('holding_rate_annual',.20,'fraction/year',.12,.30,'[ASSUMED]','Illustrative carrying-cost rate'),
  ('safety_stock',round(ss,2),'tonnes',None,None,'[DERIVED]','z95 * sqrt(L * daily_sd^2 + daily_mean^2 * lead_sd^2)'),
  ('reorder_point',round(rop,2),'tonnes',None,None,'[DERIVED]','daily_mean * L + safety_stock'),
  ('holding_cost_per_tonne_month',1000,'PKR/tonne/month',None,None,'[DERIVED]','60000 * .20 / 12')]:
  rows['inventory_params'].append([id+'.'+param,value,unit,tag,'provisional synthetic inventory model',method,lo,hi,'provisional; instructor approval required','Illustrative DC parameters, not EFERT data'])
rows['rules']=[['R01','max_open_dcs','No more than 6 candidate DCs','max_open',6,'DCs','[ASSUMED]','Phase 2 candidate count',3,6,'proposed'],['R02','demand_satisfaction','All monthly demand must be served','demand_coverage',1,'fraction','[ASSUMED]','Model design requirement',1,1,'proposed'],['R03','no_forced_contracts','No invented take-or-pay commitments','minimum_contract',0,'tonnes','[ASSUMED]','No EFERT contractual evidence',0,0,'proposed'],['R04','capacity_limit','Each candidate DC capped monthly','dc_capacity',35000,'tonnes/month','[ASSUMED]','Illustrative 35kt per DC',25000,45000,'proposed']]
rows['scenarios']=[['S00','Base case','baseline',1,1,0,'[ASSUMED]','Base model', 'no'],['S01','Fuel shock','freight_multiplier',1,1.3,30,'[ASSUMED]','Sensitivity, not forecast','no'],['S02','Demand growth','demand_multiplier',1,1.15,15,'[ASSUMED]','Sensitivity','no'],['S03','Demand contraction','demand_multiplier',1,.85,-15,'[ASSUMED]','Sensitivity','no'],['S04','Single plant outage','P01_capacity_multiplier',1,0,-100,'[ASSUMED]','One-plant outage; feasibility may fail','no'],['S05','Service tightening','max_delivery_days',5,3,-40,'[ASSUMED]','Service constraint stress','no'],['S06','Warehouse inflation','dc_fixed_cost_multiplier',1,1.25,25,'[ASSUMED]','Facility cost stress','no']]
# Writes CSVs and workbook
sheet_names=['02_Nodes','03_Demand_Monthly','04_Supply','05_Distances','06_Freight_Rates','07_DC_Costs','08_Inventory_Params','09_Service','10_Rules','11_Scenarios']
for (name,records),sheet_name in zip(rows.items(),sheet_names):
 with open(f'{O}/{name}.csv','w',newline='',encoding='utf-8') as f:
  w=csv.writer(f);w.writerow(headers[name]);w.writerows(records)
 s=wb.worksheets.get_item(sheet_name);n=len(records);s.get_range_by_indexes(4,0,n,len(headers[name])).values=records
 if name=='inventory_params':s.get_range('A2').values=[['PROVISIONAL synthetic inventory model authorised by user; NOT a linked prior milestone. Instructor compliance risk.']]
 if name=='demand_monthly':s.get_range('A2').values=[['36 months x 12 zones; synthetic seed 42; regional volume is assumed, not EFERT sales.']]
# sanity checks
sums={}
for row in rows['demand_monthly']:sums[row[0]]=sums.get(row[0],0)+row[2]
max_month=max(sums.values());total_dc=6*35000;plantcap=sum(p[-1] for p in plants)/12
checks=[['Node count','2 plants + 6 DC + 12 zones',len(rows['nodes']),'PASS','Nodes dataset','', 'PASS'],['Monthly history','36 distinct months',len(sums),'PASS','2023-2025','', 'PASS'],['Monthly demand <= total DC capacity',f'<= {total_dc:,.0f} t',round(max_month,1),'PASS' if max_month<=total_dc else 'FAIL','6 DC x 35,000 tonnes','Reduce demand or increase capacities','PASS' if max_month<=total_dc else 'FAIL'],['Monthly demand <= total plant capacity',f'<= {plantcap:,.0f} t',round(max_month,1),'PASS' if max_month<=plantcap else 'FAIL','2.275m annual /12','Adjust regional allocation','PASS' if max_month<=plantcap else 'FAIL'],['Demand region vs EFERT national sales','Assumed 1.7m < 2.314m national sales',annual_region,'PASS','Provisional volume only','Obtain regional market share','PASS'],['Road routes verified','All lanes map checked',0,'FAIL','Haversine proxy only','Map verify routes','FAIL'],['Inventory milestone linkage','Linked prior inventory model',0,'FAIL','User-approved synthetic substitute','Instructor sign-off needed','FAIL'],['Current freight quotations','Verified current lane quotations',0,'FAIL','Historical NTRC proxy','Obtain current quotes','FAIL'],['Exact coordinates verified','All 20 coordinates geocoded',0,'FAIL','Approximate city coordinates','Geocode','FAIL']]
s=wb.worksheets.get_item('14_Realism_Checks');s.get_range_by_indexes(4,0,len(checks),7).values=checks
assumptions=[['A01','Annual regional Engro Urea demand',1700000,1300000,2000000,'tonnes/year','Illustrative subset of national sales; not measured','2025 EFERT sales 2.314m national', 'high','provisional','demand_monthly'],['A02','Road circuity',1.3,1.15,1.5,'ratio','Approximate road path versus straight line','No lane map validation','high','provisional','distances'],['A03','Freight unit rate',8,5.5,12,'PKR/tonne-km','Historical NTRC 2022 rate, updated by assumption not verified quote','NTRC trucking study 2022','high','provisional','freight_rates'],['A04','DC monthly throughput',18000,25000,45000,'tonnes','Illustrative storage/turnover','No EFERT DC information','high','provisional','dc_costs'],['A05','Warehouse space',20000,12000,30000,'sq ft','Illustrative rented facility','Market rental listings in Phase 1','high','provisional','dc_costs'],['A06','Inventory unit value',60000,45000,80000,'PKR/tonne','Illustrative cost basis not retail price','No EFERT inventory unit cost','high','provisional','inventory_params'],['A07','Holding rate',.20,.12,.30,'annual fraction','Inventory model substitute','No prior inventory milestone','high','provisional','inventory_params'],['A08','Daily service distance',350,250,450,'km/day','Truck transit allowance','No lane service commitments','medium','provisional','service'],['A09','Zone weights',100,100,100,'percent total','Twelve illustrative shares sum 100%; not district data','Phase 2 proposed zone structure','high','provisional','demand_monthly']]
wb.worksheets.get_item('12_Assumptions').get_range_by_indexes(4,0,len(assumptions),11).values=assumptions
# README disclaimer
wb.worksheets.get_item('00_README').get_range('A2').values=[['Illustrative model built from public information and synthetic data. Not company data. Phase 3 PROVISIONAL; see failed verification checks.']]
out='/mnt/data/EFERT_Phase3_Data_Pack_Provisional.xlsx';SpreadsheetFile.export_xlsx(wb).save(out)
with zipfile.ZipFile('/mnt/data/EFERT_Phase3_CSVs.zip','w',zipfile.ZIP_DEFLATED) as z:
 for name in rows:z.write(f'{O}/{name}.csv',arcname=name+'.csv')
print('OUTPUT',out,'rows',[(k,len(v)) for k,v in rows.items()],'max_month',max_month,'plant_cap',plantcap,'DC_cap',total_dc,'checks',[(x[0],x[-1]) for x in checks])
