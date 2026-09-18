#!/usr/bin/env python3
"""Reapply unchanged S1 predicate and prove fact-balance feasibility/infeasibility."""
import argparse,collections,gzip,json
from pathlib import Path

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--s1',type=Path,required=True);p.add_argument('--certification',type=Path,required=True);a=p.parse_args();out=a.certification
 runtime=json.loads((out/'runtime_certification.json').read_text());sources=json.loads((out/'source_runtime_certification.json').read_text())
 assert runtime['status']=='VERIFIED' and runtime['transition_classes_verified']==23 and runtime['failures']==0 and runtime['modeled_bypasses_remaining']==0
 assert sources['bird']['original_ex_pass']==500 and sources['tatqa']['records']==1668 and sources['hotpot']['records']==7405
 with gzip.open(out/'task_certification.jsonl.gz','rt') as f:certs={(x['family'],x['task_id']):x for x in map(json.loads,f)}
 with gzip.open(a.s1/'eligibility.jsonl.gz','rt') as f:old=list(map(json.loads,f))
 updated=[]
 for row in old:
  original=json.loads(json.dumps(row));cert=certs[(row['family'],row['task_id'])]
  assert cert['source_input_complete'] and cert['native_output_equal'] and cert['gold_input_excluded'] and all(cert['AB_recognizer_match']) and all(cert['AB_raw_absent'])
  for k in ('original_evaluator','adapter_equivalence','collective_capabilities','family_structural_parity','family_complete_mediation'):
   if row['checks'][k]=='UNKNOWN':row['checks'][k]='TRUE'
  values=set(row['checks'].values())
  row['status']='ELIGIBLE' if values=={'TRUE'} and row['naturalness']=='NATURAL' else 'INELIGIBLE' if 'FALSE' in values else 'UNRESOLVED'
  for k in ('naturalness','compatible_types','rationale'):assert row[k]==original[k]
  updated.append(row)
 with gzip.open(out/'eligibility.jsonl.gz','wt') as f:
  for x in updated:f.write(json.dumps(x)+'\n')
 pools={f:[x for x in updated if x['family']==f] for f in ('bird_pg','tatqa','hotpot')}
 summary={f:{'official':len(rows),'eligible':sum(x['status']=='ELIGIBLE' for x in rows),'ineligible':sum(x['status']=='INELIGIBLE' for x in rows),'unresolved':sum(x['status']=='UNRESOLVED' for x in rows),'exclusion_reasons':{}} for f,rows in pools.items()}
 # Machine-checkable infeasibility certificate: every eligible BIRD record has only P4.
 # Any20 BIRD selections therefore require20 P4, contradicting the global bound15.
 bird=[x for x in pools['bird_pg'] if x['status']=='ELIGIBLE']
 assert len(bird)>=23 and all(x['compatible_types']==['P4'] for x in bird)
 proof={'FACT_BALANCE_FEASIBILITY':'FAILED','required_bird_confirmatory':20,'all_eligible_bird_compatible_types':['P4'],'eligible_bird_checked':len(bird),'minimum_forced_P4':20,'global_required_P4':15,'contradiction':'20 > 15','proof_scope':'unchanged recorded S1 naturalness compatibility sets; no claim that every conceivable independent P3 justification is impossible','cluster_constraints':'Additional constraints can only shrink feasible set; impossible already before clustering.','allocation_witness':None,'selected_development':0,'selected_confirmatory':0,'selection_algorithm_created':False}
 (out/'eligibility_summary.json').write_text(json.dumps(summary,indent=2)+'\n');(out/'balance_infeasibility.json').write_text(json.dumps(proof,indent=2)+'\n')
 print(json.dumps({'pools':summary,'balance':proof},indent=2))
if __name__=='__main__':main()
