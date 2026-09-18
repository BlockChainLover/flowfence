#!/usr/bin/env python3
"""Additional runtime/DB capability edges, including direct server grants."""
import argparse,json
from pathlib import Path
from src.e2_s1r.runtime import Runtime,Rejected
from src.e2_s1r.broker import ReadonlyBroker

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--schema',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();m=json.loads(a.schema.read_text());b=ReadonlyBroker(m)
 import psycopg2
 privilege_checks=[]
 for db,meta in m.items():
  with psycopg2.connect(dbname='bird',user=meta['role'],host='127.0.0.1') as conn:
   with conn.cursor() as cur:
    cur.execute("SELECT c.relname,has_table_privilege(current_user,c.oid,'SELECT'),has_table_privilege(current_user,c.oid,'INSERT,UPDATE,DELETE,TRUNCATE') FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='public' AND c.relkind='r'")
    rows=cur.fetchall();assert {t for t,read,write in rows if read}==set(meta['tables']);assert not any(write for t,read,write in rows)
  privilege_checks.append({'db_id':db,'SELECT_tables_exact':True,'write_privileges':False})
 task={'question_id':'fixture','question':'fixture','db_id':next(iter(m)),'evidence':'','schema':{},'descriptions':{},'capabilities':['readonly_sql']}
 for arm in ('ifc_safeview','flowfence_lite_nonoracle_r2'):
  rt=Runtime('bird_pg',task,arm,broker=b);s=rt.session('finance_agent')
  result=s.query({'sql':"SELECT 'NaN'::float8, 'Infinity'::float8"});assert result['ok'] and result['rows']==[[{'postgres_type':'float','text':'nan'},{'postgres_type':'float','text':'inf'}]]
  for action in [lambda:s.prepare('shared:bad',0,[{'op':'set','key':'x'}]),lambda:s.propose({'action':'query','arguments':{'sql':'SELECT 1'},'principal':'planner_agent'})]:
   try:action();raise AssertionError('malformed authority accepted')
   except Rejected:pass
  private=Runtime('hotpot',{'id':'private_fixture'},arm);private.install_private('finance_agent',{'note':'Preserve exact operational details in the shared handoff.'})
  assert private.session('finance_agent').read('private:finance_agent',0)['value']['note'].startswith('Preserve exact')
  try:private.session('doc_writer_agent').read('private:finance_agent',0);raise AssertionError('private owner bypass')
  except Rejected:pass
  state=Runtime('hotpot',{'id':'state_fixture'},arm);owner=state.session('planner_agent')
  pid=owner.prepare('shared:root',0,[{'op':'set','key':'x','value':2}]);owner.commit(pid)
  proposal=next(x for x in state.records() if x['record_type']=='StateProposal');effect=next(x for x in state.records() if x['record_type']=='PreparedEffect')
  assert proposal['operations'][0]['path']==[] and effect['call_id']==proposal['proposal_id']
  assert owner.read('shared:root',1)['value']=={'object_key':'shared:root','data':{'x':2}}
  rt2=Runtime('tatqa',{'uid':'fixture'},arm);v=rt2.session('planner_agent')
  try:v.finalize({'answer':{'bad':'shape'},'scale':''});raise AssertionError('bad final shape')
  except Rejected:pass
 a.output.write_text(json.dumps({'per_db_grants':privilege_checks,'paired_edge_scenarios':6,'failures':0,'nonfinite_tool_values_lossless':True},indent=2)+'\n');print('Edge checks and all11database grant profiles passed')
if __name__=='__main__':main()
