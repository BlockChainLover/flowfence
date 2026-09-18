#!/usr/bin/env python3
"""Cross-check final S1-R evidence, unchanged annotations/pins, and infeasibility proof."""
import argparse,collections,gzip,hashlib,importlib.metadata,json,subprocess,sys
from pathlib import Path

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--artifacts',type=Path,required=True);p.add_argument('--source-root',type=Path,required=True);a=p.parse_args();out=a.artifacts
 import jsonschema,psycopg2
 oldroot=Path('artifacts/aamas2027_e2_source_s1');manifest=json.loads((oldroot/'source_manifest.json').read_text())
 for name,expected in manifest['files'].items():assert hashlib.sha256((a.source_root/name).read_bytes()).hexdigest()==expected,name
 for repo,pin in manifest['code_pins'].items():assert subprocess.check_output(['git','-C',str(a.source_root/repo),'rev-parse','HEAD'],text=True).strip()==pin
 frozen='6bb7cba43724c10213ee4d81cdf2f82877fa6f5b831ca71c0698495866307d62';assert hashlib.sha256(Path('src/defenses/mas_flowfence.py').read_bytes()).hexdigest()==frozen
 schema=json.loads(Path('experiments/e2_source_s1/eligibility_schema.json').read_text());validator=jsonschema.Draft202012Validator(schema)
 with gzip.open(oldroot/'eligibility.jsonl.gz','rt') as f:old={(x['family'],x['task_id']):x for x in map(json.loads,f)}
 with gzip.open(out/'eligibility.jsonl.gz','rt') as f:rows=list(map(json.loads,f))
 assert len(rows)==9573 and len({(x['family'],x['task_id']) for x in rows})==9573
 for x in rows:
  validator.validate(x);before=old[(x['family'],x['task_id'])]
  for k in ('naturalness','compatible_types','rationale'):assert x[k]==before[k]
  assert x['status']=='ELIGIBLE' and set(x['checks'].values())=={'TRUE'}
 balance=json.loads((out/'balance_infeasibility.json').read_text());assert balance['minimum_forced_P4']==20>balance['global_required_P4']==15
 assert all(x['compatible_types']==['P4'] for x in rows if x['family']=='bird_pg')
 assert not balance['selection_algorithm_created'] and balance['selected_development']==balance['selected_confirmatory']==0
 runtime=json.loads((out/'runtime_certification.json').read_text());edge=json.loads((out/'edge_cases.json').read_text())
 assert runtime['transition_classes_verified']==23 and runtime['failures']==edge['failures']==runtime['modeled_bypasses_remaining']==0
 source=json.loads((out/'source_runtime_certification.json').read_text());assert source['bird']['original_ex_pass']==500 and source['task_level_AB_certified']==9573 and source['typed_evaluator_jobs']==9573
 assert source['tatqa']['metrics'][:3]==[1.0,1.0,1.0] and len(source['hotpot']['metrics'])==12
 for path in out.iterdir():
  if path.suffix not in ('.json','.gz'):continue
  data=gzip.decompress(path.read_bytes()) if path.suffix=='.gz' else path.read_bytes()
  assert b'S1R_CERT_PRIVATE_7319' not in data and b'S1R_PRIVATE_FIXTURE_' not in data,path
 sys.path.insert(0,str(a.source_root/'bird_mini/evaluation'));import evaluation_ex as ex
 bird=json.loads((a.source_root/'data/birdsql__bird_mini_dev__data__mini_dev_pg-00000-of-00001.json').read_text())
 assert ex.execute_model('NOT VALID SQL',bird[0]['SQL'],'',0,30,'PostgreSQL')['res']==0
 with psycopg2.connect(dbname='bird',user='postgres',host='127.0.0.1',options='-c max_parallel_workers_per_gather=0') as conn:
  with conn.cursor() as cur:
   cur.execute("SELECT version(), current_setting('server_encoding'),current_setting('lc_collate'),current_setting('lc_ctype'),current_setting('max_parallel_workers_per_gather')")
   env=list(cur.fetchone());assert env[1:]==['UTF8','C','C','0'] and '14.24' in env[0]
 report={'official_records_validated':len(rows),'naturalness_and_compatibility_unchanged':True,'source_pins_and_hashes_unchanged':True,'recognizer_hash':frozen,'original_EX_negative_fixture':0,'environment':env,'pglast_version':importlib.metadata.version('pglast'),'paired_runtime_fixtures':runtime['paired_runtime_scenarios']+edge['paired_edge_scenarios'],'transition_classes_verified':23,'modeled_bypasses_remaining':0,'safe_evidence_omits_raw_fixture_values':True,'balance_infeasibility_verified':True,'formal_model_runs':0,'development_model_runs':0}
 (out/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
