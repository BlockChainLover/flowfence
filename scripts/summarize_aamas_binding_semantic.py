#!/usr/bin/env python3
"""Rebuild E6 reports exclusively from safe episode, event and call records."""
from __future__ import annotations
import argparse
import csv
import json
import random
import statistics
from collections import Counter,defaultdict
from pathlib import Path
from src.experiments.aamas_metrics import corrected_from_events
from src.experiments.aamas_binding_semantic import matrix_cells

METRICS=('success','privacy_safe_success','delivered_exact_secret_exposure','delivered_reconstructable_secret_exposure','pre_mediation_generated_exact_secret_attempts','pre_mediation_generated_reconstructable_secret_attempts','unauthorized_recipient_pairs','forbidden_channel_secret_events','intervention_count','blocks','rewrites')

def read(path): return [json.loads(l) for l in path.read_text().splitlines() if l] if path.exists() else []

def summarize(folder,output):
    output.mkdir(parents=True,exist_ok=True)
    registration=json.loads((folder/'registration.json').read_text())
    rows=read(folder/'episodes.jsonl');events=defaultdict(list);attempts=defaultdict(list)
    for e in read(folder/'events.jsonl'):events[e['run_id']].append(e)
    for e in read(folder/'generated_attempts.jsonl'):attempts[e['run_id']].append(e)
    calls={c['call_id']:c for c in read(folder/'call_attempts.jsonl')}
    names=('task_id','topology','condition','defense','seed')
    expected={tuple(c[k] for k in names) for c in matrix_cells(registration['config'])}
    assert len({tuple(r[k] for k in names) for r in rows})==len(rows)
    assert {tuple(r[k] for k in names) for r in rows}==expected
    for r in rows:
        assert r['status'] in ('completed','failed','blocked')
        es=events[r['run_id']]; gs=attempts[r['run_id']]
        rebuilt=corrected_from_events(es)
        for key in METRICS[2:6]: rebuilt[key]=sum(e[key] for e in (gs if key.startswith('pre_') else es))
        rebuilt.update(intervention_count=sum(e['intervention'] for e in es),blocks=sum(e['decision']=='block' for e in es),rewrites=sum(e['content_changed'] and e['decision'] in ('rewrite_safe_view','quarantine') for e in es))
        rebuilt['success']=r['status']=='completed' and all(r['structured_correctness'].values())
        rebuilt['privacy_safe_success']=rebuilt['success'] and not rebuilt['delivered_exact_secret_exposure'] and not rebuilt['delivered_reconstructable_secret_exposure']
        assert all(r[k]==v for k,v in rebuilt.items()),r['run_id']
        r.update(rebuilt)
    groups=[]
    for topology in ('overall','chain_4','blackboard_4'):
        for condition in ('overall',*registration['config']['conditions']):
            for defense in registration['config']['defenses']:
                rs=[r for r in rows if r['defense']==defense and (topology=='overall' or r['topology']==topology) and (condition=='overall' or r['condition']==condition)]
                groups.append({'topology':topology,'condition':condition,'defense':defense,'n':len(rs),'completed':sum(r['status']=='completed' for r in rs),**{k:sum(r[k] for r in rs) for k in METRICS}})
    pairs=[]
    indexed={tuple(r[k] for k in names):r for r in rows}
    matched=[(r,indexed[(r['task_id'],r['topology'],r['condition'],'ifc_safeview',r['seed'])]) for r in rows if r['defense']=='flowfence_lite_nonoracle']
    for topology in ('overall','chain_4','blackboard_4'):
        for condition in ('overall',*registration['config']['conditions']):
            selected=[(a,b) for a,b in matched if (topology=='overall' or a['topology']==topology) and (condition=='overall' or a['condition']==condition)]
            for metric in METRICS:
                usable=[(a,b) for a,b in selected if metric in ('success','privacy_safe_success') or a['status']==b['status']=='completed']
                diffs=[int(a[metric])-int(b[metric]) for a,b in usable];clusters=defaultdict(list)
                for (a,b),d in zip(usable,diffs):clusters[a['task_id']].append(d)
                means=[statistics.mean(ds) for ds in clusters.values()];rng=random.Random(20260912)
                boot=sorted(statistics.mean(rng.choices(means,k=len(means))) for _ in range(10000)) if means else []
                direction=1 if metric in ('success','privacy_safe_success') else -1
                pairs.append({'topology':topology,'condition':condition,'metric':metric,'matched':len(selected),'available':len(diffs),'better':sum(d*direction>0 for d in diffs),'tie':sum(d==0 for d in diffs),'worse':sum(d*direction<0 for d in diffs),'mean_papc_minus_ifc':statistics.mean(diffs) if diffs else None,'task_instance_clusters':len(means),'descriptive_cluster_interval':[boot[249],boot[9749]] if boot else None})
    actual=[c for c in calls.values() if c.get('provider_request',True)]
    result={'planned':len(expected),'terminal':len(rows),'status_counts':dict(Counter(r['status'] for r in rows)),'api_requests':len(actual),'input_tokens':sum(c['input_tokens'] for c in actual),'output_tokens':sum(c['output_tokens'] for c in actual),'retries':sum(r['retries'] for r in rows),'requested_models':sorted({c['model_requested'] for c in actual}),'returned_models':sorted({c['model_version'] for c in actual if c.get('model_version')}),'dry_run':registration['dry_run'],'errors':dict(Counter(r['error_type'] for r in rows if r['error_type'])),'groups':groups,'paired':pairs,'scope':'One task family. Totals retain partial observed failures; privacy pair differences require both completed. Descriptive task-instance intervals are not cross-domain inference or equivalence tests.'}
    (output/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    for filename,data in [('groups.csv',groups),('paired.csv',pairs)]:
        with (output/filename).open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
    (output/'failures.safe.json').write_text(json.dumps([r for r in rows if not r['success']],indent=2)+'\n')
    lines=['# E6 binding semantic results','',result['scope'],'',f"Cells: {len(rows)}/{len(expected)}. Status: {result['status_counts']}. API attempts: {len(actual)}. Tokens: {result['input_tokens']} input / {result['output_tokens']} output. Retries: {result['retries']}.",'','Values below are counts summed across retained first attempts, not per-episode means.','', '| Defense | n | Task | Safe task | Delivered exact | Delivered reconstructable | Exact attempts | Reconstructable attempts | Unauthorized pairs | Forbidden secret-events | Interventions | Blocks | Rewrites |','|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for g in groups:
        if g['topology']==g['condition']=='overall':lines.append('| '+' | '.join(str(g[k]) for k in ('defense','n',*METRICS))+' |')
    lines+=['','See groups.csv and paired.csv for topology, condition and joint slices. Raw exact and reconstructable event counters are separate overlapping outcomes, not additive distinct breaches. Attempts are role-response occurrences; deliveries are policy-violating secret-event occurrences and must not be subtracted to calculate containment.','']
    (output/'REPORT.md').write_text('\n'.join(lines))
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();r=summarize(a.input,a.output);print(json.dumps({k:v for k,v in r.items() if k not in ('groups','paired')}))

if __name__=='__main__':main()
