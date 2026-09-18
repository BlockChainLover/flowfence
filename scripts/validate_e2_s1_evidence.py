#!/usr/bin/env python3
"""Validate complete S1 audit records and conservative certification consistency."""
import argparse,collections,gzip,hashlib,json,sys
from pathlib import Path

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--artifacts',type=Path,required=True);p.add_argument('--dependency-path',type=Path,required=True);a=p.parse_args();sys.path.insert(0,str(a.dependency_path))
 import jsonschema
 schema=json.loads(Path('experiments/e2_source_s1/eligibility_schema.json').read_text());validator=jsonschema.Draft202012Validator(schema)
 rows=[]
 with gzip.open(a.artifacts/'eligibility.jsonl.gz','rt') as f:
  for line in f:row=json.loads(line);validator.validate(row);rows.append(row)
 expected={'bird_pg':500,'tatqa':1668,'hotpot':7405}
 assert dict(collections.Counter(r['family'] for r in rows))==expected
 assert len({(r['family'],r['task_id']) for r in rows})==9573
 assert all(r['status']=='UNRESOLVED' and r['checks']['family_complete_mediation']=='UNKNOWN' for r in rows)
 with gzip.open(a.artifacts/'adapter_reachability.jsonl.gz','rt') as f:reach=[json.loads(x) for x in f]
 assert {(r['family'],r['task_id']) for r in reach}=={(r['family'],r['task_id']) for r in rows}
 assert all(r['both_arms_public_input_and_final_serialization'] for r in reach)
 assert hashlib.sha256(Path('src/defenses/mas_flowfence.py').read_bytes()).hexdigest()=='6bb7cba43724c10213ee4d81cdf2f82877fa6f5b831ca71c0698495866307d62'
 for path in a.artifacts.rglob('*'):
  if not path.is_file():continue
  data=gzip.decompress(path.read_bytes()) if path.suffix=='.gz' else path.read_bytes()
  assert b'S1_FIXTURE_ONLY_OPAQUE_987654' not in data,str(path)
 pg=json.loads((a.artifacts/'serial_engine/pg_evaluator.json').read_text())
 assert len(pg['bird']['records'])==500 and all(x['native_ex']==x['adapted_ex']==1 for x in pg['bird']['records'])
 assert pg['ves']['repeatable'] is False
 qa=json.loads((a.artifacts/'qa_evaluator.json').read_text());assert qa['tatqa']['questions']==1668 and qa['hotpot']['questions']==7405
 assert len(qa['hotpot']['metrics']['adapted_gold'])==12
 report={'records_validated':len(rows),'all_official_ids_unique':True,'recognizer_unchanged':True,'safe_artifacts_omit_fixture_raw_value':True,'serial_postgres_EX_gold_pass':500,'models_called':0}
 (a.artifacts/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
