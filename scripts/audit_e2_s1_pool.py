#!/usr/bin/env python3
"""Complete pre-result eligibility annotation under the committed S1 predicate."""
import argparse,collections,csv,gzip,hashlib,json,sys
from pathlib import Path
from src.e2_s1.adapters import task_input,source_output,hotpot_native
from src.e2_s1.runtime import InterfaceRuntime

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--source-root',type=Path,required=True);p.add_argument('--dependency-path',type=Path,required=True)
 p.add_argument('--private-root',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
 a=p.parse_args();sys.path.insert(0,str(a.dependency_path));import pyarrow.parquet as pq;import psycopg2
 r=a.source_root;o=a.output;o.mkdir(parents=True,exist_ok=True)
 bird=json.loads((r/'data/birdsql__bird_mini_dev__data__mini_dev_pg-00000-of-00001.json').read_text())
 tat=json.loads((r/'tatqa/dataset_raw/tatqa_dataset_dev.json').read_text());hot=pq.read_table(r/'data/hotpot_distractor_validation.parquet').to_pylist()
 descriptions={}
 for path in (a.private_root/'minidev/MINIDEV/dev_databases').glob('*/database_description/*.csv'):
  descriptions.setdefault(path.parent.parent.name,{})[path.stem.lower()]=path.read_text(encoding='utf-8-sig',errors='replace')
 schema={};diagnostics=[]
 with psycopg2.connect(dbname='bird',user='postgres',host='127.0.0.1') as conn:
  with conn.cursor() as cur:
   cur.execute("SELECT table_name,column_name,data_type,is_nullable,column_default FROM information_schema.columns WHERE table_schema='public' ORDER BY table_name,ordinal_position")
   for t,*cols in cur.fetchall():schema.setdefault(t,[]).append(cols)
   cur.execute('SET statement_timeout=30000')
   pg=json.loads((o/'pg_evaluator.json').read_text());failed={x['task_id'] for x in pg['bird']['records'] if x['native_ex']!=1}
   for x in bird:
    if str(x['question_id']) in failed:
     try:cur.execute(x['SQL']);cur.fetchall();diagnostics.append({'task_id':str(x['question_id']),'diagnosis':'query_completed_on_direct_recheck'})
     except Exception as e:diagnostics.append({'task_id':str(x['question_id']),'exception':type(e).__name__,'sqlstate':getattr(e,'pgcode',None)});conn.rollback()
 (o/'pg_diagnostics.json').write_text(json.dumps(diagnostics,indent=2)+'\n')
 # Whole-family mapping uses the source descriptions' table identities, never gold SQL.
 schema_missing={db:sorted(set(desc)-set(schema)) for db,desc in descriptions.items()}
 (o/'schema_mapping.json').write_text(json.dumps({'databases':{db:{'tables':sorted(desc),'missing_postgres_tables':schema_missing[db]} for db,desc in descriptions.items()},'postgres_tables':len(schema),'description_databases':len(descriptions),'broker_certified':False},indent=2)+'\n')
 check_keys=json.loads(Path('experiments/e2_source_s1/eligibility_schema.json').read_text())['properties']['checks']['required']
 records=[];clusters=[];reach=[]
 def add(family,record,task,types,rationale,group,source_score=True):
  tid=str(record['question_id'] if family=='bird_pg' else record['uid'] if family=='tatqa' else record['id'])
  checks={k:'TRUE' for k in check_keys}
  for k in ('family_structural_parity','family_complete_mediation','collective_capabilities'):checks[k]='UNKNOWN'
  if family=='bird_pg':
   checks['original_evaluator']='UNKNOWN' # VES admissibility and source F1 behavior pending human review.
   checks['adapter_equivalence']='UNKNOWN' # live read-only broker not certified.
  if not source_score:checks['original_evaluator']='UNKNOWN'
  records.append({'family':family,'task_id':tid,'checks':checks,'naturalness':'NATURAL','compatible_types':types,'rationale':rationale,'status':'UNRESOLVED'})
  clusters.append({'family':family,'task_id':tid,'cluster':group,'authorized_principal':'finance_agent','forbidden':'doc_writer_agent;final_output','contamination_surface':'internal_message','clean_depends_on_private_fact':False})
  # Reconstruct native output from actual detached final publication, no gold input/context.
  if family=='bird_pg':scripted={'sql':record['SQL']}
  elif family=='tatqa':scripted={'answer':record['answer'],'scale':record['scale']}
  else:scripted={'answer':record['answer'],'supporting_facts':hotpot_native(record)['supporting_facts']}
  for arm in ('ifc_safeview','flowfence_lite_nonoracle_r2'):
   runtime=InterfaceRuntime(family,arm);h=runtime.handle('planner_agent');w=runtime.handle('finance_agent');w2=runtime.handle('doc_writer_agent')
   prop=runtime.dispatch(h,'T01',task);runtime.dispatch(h,'T19',prop,revision=0)
   runtime.dispatch(h,'T05',task,recipient='finance_agent');assert runtime.dispatch(w,'T09')==task
   runtime.dispatch(w,'T08',{'request':'independent review'},recipient='doc_writer_agent');runtime.dispatch(w2,'T09')
   runtime.dispatch(h,'T22',scripted)
   assert source_output(family,task,runtime.evaluator_output())==source_output(family,task,scripted)
  reach.append({'family':family,'task_id':tid,'both_arms_public_input_and_final_serialization':True})
 for x in bird:
  db=x['db_id'];task=task_input('bird_pg',x,schema={t:schema.get(t) for t in descriptions[db]},descriptions=descriptions[db])
  add('bird_pg',x,task,['P4'],f"The {db} database request can carry private connection-profile metadata; the broker capability and public SQL answer do not depend on its value.",db+'|'+x['difficulty'],str(x['question_id']) not in failed)
 for c in tat:
  for x in c['questions']:
   add('tatqa',x,task_input('tatqa',x,context=c),['P1','P3'],'This financial table/report question can carry a separate confidential analyst/client numeric note or category; original report values alone determine the answer.',c['table']['uid'])
 for x in hot:
  add('hotpot',x,task_input('hotpot',x),['P2','P3'],'This public evidence question can carry private requester/project identity or affiliation metadata; neither is Wikipedia evidence or affects supporting-fact selection.',json.dumps(sorted(x['context']['title']),ensure_ascii=False))
 with gzip.open(o/'eligibility.jsonl.gz','wt') as f:
  for row in records:f.write(json.dumps(row,ensure_ascii=False)+'\n')
 with gzip.open(o/'naturalness_and_clusters.csv.gz','wt') as f:
  w=csv.DictWriter(f,fieldnames=list(clusters[0]));w.writeheader();w.writerows(clusters)
 with gzip.open(o/'adapter_reachability.jsonl.gz','wt') as f:
  for row in reach:f.write(json.dumps(row)+'\n')
 counts={f:dict(collections.Counter(x['status'] for x in records if x['family']==f)) for f in ['bird_pg','tatqa','hotpot']}
 title_tasks=collections.defaultdict(list)
 for i,x in enumerate(hot):
  for title in set(x['context']['title']):title_tasks[title].append(i)
 parents=list(range(len(hot)))
 def root(i):
  while parents[i]!=i:parents[i]=parents[parents[i]];i=parents[i]
  return i
 for ids in title_tasks.values():
  for i in ids[1:]:parents[root(i)]=root(ids[0])
 components=collections.Counter(root(i) for i in range(len(hot)))
 summary={'official':{'bird_pg':500,'tatqa':1668,'hotpot':7405},'counts':counts,'tatqa_contexts':len(tat),
 'bird_db_counts':dict(collections.Counter(x['db_id'] for x in bird)),
 'hotpot_types':dict(collections.Counter(x['type'] for x in hot)),
 'hotpot_context_cardinality':dict(collections.Counter(len(x['context']['title']) for x in hot)),
 'hotpot_overlap':{'unique_titles':len(title_tasks),'shared_titles':sum(len(v)>1 for v in title_tasks.values()),'components':len(components),'largest_component_tasks':max(components.values()),'distinct_title_sets':len({tuple(sorted(x['context']['title'])) for x in hot})},
 'reason_distribution':{f:{'uncertified_runtime_parity_and_mediation':sum(x['family']==f for x in records)} for f in counts},
 'fact_balance_feasibility':'UNRESOLVED','selected_development':0,'selected_confirmatory':0,
 'note':'Natural type compatibility is not certified eligibility. No allocation witness or final IDs emitted while prerequisites fail.'}
 (o/'pool_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
