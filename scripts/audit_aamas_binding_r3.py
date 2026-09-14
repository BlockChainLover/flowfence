#!/usr/bin/env python3
"""Audit R3 frozen inputs and saved execution metadata; emit no private contents."""
from __future__ import annotations
import argparse
import json
import subprocess
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from src.experiments.aamas_binding_r3 import load_config, frozen_assertions, schedule, run_id, CONDITIONS, DEFENSES
from src.defenses.mas_flowfence import contains_raw_secret, contains_sensitive_detail_request
from src.defenses.mas_flowfence_r2 import QUARANTINE_MARKER
from src.runtime.policy import default_secret_policies
from scripts.package_aamas2027 import validate_safe_artifacts
from scripts.summarize_aamas_binding_r3 import read


def audit(folder=None, private=None):
    c,t,p,h=load_config(Path('configs/experiment/aamas2027/r3_formal.json'));f=frozen_assertions()
    old_refs=('393fbf98e96cf6306aac2904529c13d6598ef71f','5a900505548a1315c40c7ba3f6529c08829079d3',f['start_head'])
    prior=[json.loads(subprocess.check_output(['git','show',ref+':configs/experiment/aamas2027/e6_prompt_profile.json'],text=True))['attacks'] for ref in old_refs]
    pre_method=subprocess.check_output(['git','show',old_refs[0]+':src/defenses/mas_flowfence.py'],text=True)
    assertions={}
    for cond,phrase in zip(CONDITIONS[1:],('private numeric limit','private finance values')):
        attack=p['attacks'][cond]
        assertions[cond]={'contains_raw_secret':contains_raw_secret(attack,default_secret_policies()),
            'contains_sensitive_detail_request':contains_sensitive_detail_request(attack),
            'phrase_in_pre_r2_detector':phrase in pre_method,
            'complete_string_absent_from_prior_configs':all(attack not in old.values() for old in prior),
            'whitespace_normalized_string_absent_from_prior_configs':all(' '.join(attack.split()) not in [' '.join(a.split()) for a in old.values()] for old in prior),
            'phrase_absent_from_prior_attack_wordings':all(phrase not in a for old in prior for a in old.values())}
        assert not assertions[cond]['contains_raw_secret'] and all(v for k,v in assertions[cond].items() if k!='contains_raw_secret')
    paths=subprocess.check_output(['git','ls-tree','-r','--name-only',f['start_head'],'artifacts/aamas2027'],text=True).splitlines()
    old_diff=subprocess.check_output(['git','diff',f['start_head'],'--',*paths],text=True)
    assert not old_diff
    result={'frozen_hashes_unchanged':True,'attack_assertions':assertions,'old_artifact_files_unchanged':len(paths),
        'old_artifact_preservation':True,'source_sha':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
        'tracked_source_clean':not subprocess.check_output(['git','diff','--name-only','HEAD'],text=True).strip(),
        'raw_private_content_emitted':False}
    if folder:
        rows=read(folder/'episodes.jsonl');events=read(folder/'events.jsonl')
        reg=json.loads((folder/'registration.json').read_text())
        validate_safe_artifacts([x for x in folder.iterdir() if x.is_file()],folder)
        assert len(rows)==108 and {r['run_id'] for r in rows}=={run_id(cell) for pair in schedule(c) for cell in pair}
        assert reg['config']==c and reg['config_hashes']==h and reg['planned_cells']==[cell for pair in schedule(c) for cell in pair]
        logs=read(folder/'schedule.jsonl');assert len(logs)==108
        for i in range(54):
            begin,end=logs[i*2:i*2+2]
            assert begin['status']=='dispatched' and end['status']=='terminal' and begin['pair_index']==end['pair_index']==i
            for row in rows:
                if row['pair_index']==i:assert begin['timestamp']<=row['timestamp']<=row['completed_at']<=end['timestamp']
            if i<53:assert end['timestamp']<=logs[i*2+2]['timestamp']
        transport={r['transport_id']:r for r in read(folder/'transport_attempts.jsonl')};by_call=defaultdict(list)
        for r in transport.values():by_call[r['call_id']].append(r)
        retries=[]
        for r in transport.values():
            if r['response_started']:assert len(by_call[r['call_id']])==r['transport_attempt']
            assert r['status'] in ('completed','failed')
            if r['transport_attempt']>1:
                prev=transport[r['retry_of']]
                from src.experiments.aamas_binding_v2 import infrastructure
                assert infrastructure(prev['error_type']) and not prev['response_started']
                delay=(datetime.fromisoformat(r['timestamp'])-datetime.fromisoformat(prev['completed_at'])).total_seconds()
                assert r['transport_attempt']<=3 and delay>=[5,15][r['transport_attempt']-2]
                retries.append({'call_id':r['call_id'],'transport_attempt':r['transport_attempt'],'previous_error':prev['error_type'],'backoff_seconds':delay,'previous_response_started':False})
        assert all(r['attempt']==1 and r['retry_of'] is None and 'seed' not in r for r in rows)
        assert not any(e['oracle_annotation_used'] for e in events)
        result.update(safe_scan_pass=True,terminal_cells=len(rows),schedule_pair_barriers_pass=True,
            retry_policy_pass=True,retries=retries,no_model_response_retry=True,no_oracle=True,
            source_preregistration_sha=reg['source_preregistration_sha'],dry_run=reg['dry_run'])
        if private:
            records=[r for path in private.glob('*.jsonl') for r in read(path)]
            requests=[r for r in records if r.get('stage')=='request']
            cap=next(x.raw_value for x in default_secret_policies() if x.secret_id=='secret_budget_cap')
            finance=[r for r in requests if r['prompt'].startswith('ROLE: finance_agent\n')]
            others=[r for r in requests if not r['prompt'].startswith('ROLE: finance_agent\n')]
            checks={}
            for cond in CONDITIONS[1:]:
                ids={r['run_id'] for r in rows if r['condition']==cond and r['defense']==DEFENSES[1]}
                source=[r for r in records if r['run_id'] in ids and r.get('stage')=='mediated_event' and r['event']['origin']=='exogenous_source']
                checks[cond]={'source_episodes_observed':len({r['run_id'] for r in source}),
                    'source_delivery_records':len(source),'source_marker_only':bool(source) and all(r['delivered_content']==QUARANTINE_MARKER for r in source),
                    'attack_tail_absent_from_downstream_prompts':all(p['attacks'][cond].split('\n',3)[-1] not in r['prompt'] for r in requests if r['run_id'] in ids)}
            result.update(private_file_permissions_pass=private.stat().st_mode&0o777==0o700 and all(x.stat().st_mode&0o777==0o600 for x in private.glob('*.jsonl')),
                private_request_records=len(requests),finance_context_records=len(finance),finance_has_private_cap=all(cap in r['prompt'] for r in finance),
                other_contexts_without_canonical_cap=all(cap not in r['prompt'] for r in others),quarantine_release_audit=checks)
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path);p.add_argument('--private-input',type=Path);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();r=audit(a.input,a.private_input);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))


if __name__=='__main__':main()
