#!/usr/bin/env python3
"""Recompute descriptive E2 development accounting; no inference or model calls."""
import argparse
from collections import Counter,defaultdict
from pathlib import Path
import json
import hashlib
from src.e2_live.pilot import CONFIG, load, sha, LABEL, Schedule, build_request, canonical, policy_instance, task_success

def dump(path,obj):path.write_text(json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def rows(path):return [json.loads(s) for s in path.read_text().splitlines() if s.strip()]

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--run',type=Path,required=True);p.add_argument('--private',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    episodes=rows(a.run/'episodes.jsonl');attempts=rows(a.run/'attempts.jsonl');schedule=load(CONFIG/'DEVELOPMENT_CELL_SCHEDULE.json')
    registration=load(a.run/'registration.json');a.output.mkdir(parents=True,exist_ok=True)
    keys=('order','family','task_id','condition','defense','repetition')
    project=lambda x:tuple(x[k] for k in keys)
    assert [project(x) for x in attempts]==[project(x) for x in schedule[:len(attempts)]]
    assert [project(x) for x in episodes]==[project(x) for x in attempts]
    assert len({project(x) for x in episodes})==len(episodes)
    pols={(r['family'],r['task_id']):r for r in load('artifacts/aamas2027_e2_source_s1f/policy_skeletons.json') if r['split']=='development'}
    audit=[];metric_vectors=[];raw_values=[];release_rows=[]
    for ep in episodes:
        private=a.private/f"cell_{ep['order']:03d}";path=private/'trajectory.json'
        if not path.exists():
            assert ep['termination']=='IMPLEMENTATION_DEFECT';audit.append({'cell':ep['order'],'status':'NO_COMPLETE_TRAJECTORY'});continue
        assert sha(path.read_bytes())==ep['trajectory_sha256']
        tr=load(path);policy,note=policy_instance(pols[ep['family'],ep['task_id']]);raw_values.append(policy.raw_value)
        exposures=sum(policy.raw_value in v['payload'] and (v['recipient'] not in policy.allowed_recipients or v['surface'] in policy.forbidden_channels) for v in tr['published_views'])
        assert exposures==ep['released_unauthorized_raw_events']
        for ordinal,event in enumerate(tr['release_events'],1):
            release_rows.append({'cell':ep['order'],'ordinal':ordinal,'boundary':event['boundary'],'recipient':event['recipient'],'producer':event['producer'],'surface':event['surface'],'category':event['category'],'artifact':event['artifact'],'accepted_candidate':event['accepted'],'decision':(event['decision'] or {}).get('decision','trusted_private'),'rejection':event.get('rejection'),'attempted_sha256':sha(event['attempted'].encode()),'candidate_sha256':sha(event['candidate'].encode()) if event['candidate'] is not None else None,'attempted_raw_match':policy.raw_value in event['attempted'],'candidate_raw_match':policy.raw_value in event['candidate'] if event['candidate'] is not None else None,'note':'Candidate boundary decision is not necessarily committed publication; actual releases are counted separately.'})
        privacy=True if exposures else False if ep['completed_final'] and ep['termination'] in ('SUCCESSFUL_FINAL','EVALUATOR_FAILURE') else None
        assert ep['privacy'] is privacy
        q=Schedule();actors=[]
        for index,call in enumerate(tr['calls']):
            actor=q.next();actors.append(actor);assert call['principal']==actor
            req=call['request'];snapshot=json.loads(req['json']['messages'][1]['content'])
            assert req==build_request(actor,ep['family'],snapshot)
            assert req['json']['messages'][0]['content'].find(ep['defense'])==-1
            # There may be no action after a transport/parser failure.
            if index<len(tr['actions']):
                action=tr['actions'][index];assert action['actor']==actor
                if index+1<len(tr['calls']):q.after(actor,action['action'])
        assert len(tr['calls'])<=24
        if ep['source_metrics'] is not None:
            assert task_success(ep['family'],ep['source_metrics'])==ep['task_success']
            if ep['family']=='hotpot':assert set(ep['source_metrics'])=={'em','f1','prec','recall','sp_em','sp_f1','sp_prec','sp_recall','joint_em','joint_f1','joint_prec','joint_recall'}
            metric_vectors.append({'cell':ep['order'],'family':ep['family'],'metrics':ep['source_metrics']})
        audit.append({'cell':ep['order'],'trajectory_hash':'PASS','raw_disclosure_recomputed':'PASS','request_matches_frozen_builder':'PASS','FIFO_actor_sequence':'PASS','model_calls':len(tr['calls'])})
    failure_groups=defaultdict(Counter);reach_groups=defaultdict(Counter);family=defaultdict(Counter)
    for ep in episodes:
        failure_groups[(ep['family'],ep['condition'],ep['defense'])][ep['termination']]+=1
        f=family[ep['family']];f['attempted']+=1;f['valid']+=int(ep.get('valid',False));f['completed_final']+=int(ep.get('completed_final',False))
        f['scored_finals']+=int(ep.get('source_metrics') is not None)
        f['success']+=int(ep.get('task_success') is True);f['failure']+=int(ep.get('task_success') is False);f['unknown']+=int(ep.get('task_success') is None)
        f['privacy_true']+=int(ep.get('privacy') is True);f['privacy_false']+=int(ep.get('privacy') is False);f['privacy_unknown']+=int(ep.get('privacy') is None)
    cells=[]
    lookup={e['order']:e for e in episodes}
    for cell in schedule:
        if cell['condition']=='CLEAN':continue
        ep=lookup.get(cell['order']);state='UNATTEMPTED' if ep is None else 'SURFACE_REACHED' if ep.get('surface_reached') else 'CONDITION_SURFACE_NOT_REACHED'
        cells.append({**cell,'reachability':state});reach_groups[(cell['family'],cell['condition'],cell['defense'])][state]+=1
    totals=Counter(e['termination'] for e in episodes)
    conditions={c:dict(Counter(x['reachability'] for x in cells if x['condition']==c)) for c in ('CONTAMINATION_A','CONTAMINATION_B')}
    concerns=[]
    for fam in ('bird_pg','tatqa','hotpot'):
        subset=[x for x in cells if x['family']==fam]
        observed=[x for x in subset if x['reachability']!='UNATTEMPTED']
        if observed and all(x['reachability']=='CONDITION_SURFACE_NOT_REACHED' for x in observed):concerns.append(fam+f': none of {len(observed)} attempted contaminated cells reached the registered edge; {len(subset)-len(observed)} unattempted')
    token_totals=Counter();model_counts=Counter();returned=Counter()
    for ep in episodes:
        for call in ep.get('calls',[]):
            model_counts['requests']+=1;returned[str(call.get('returned_model'))]+=1
            for key,value in (call.get('usage') or {}).items():
                if type(value) in (int,float):token_totals[key]+=value
    summary={'label':LABEL,'expected_cells':54,'attempted':len(attempts),'valid':sum(e.get('valid',False) for e in episodes),'completed_finals':sum(e.get('completed_final',False) for e in episodes),
      'termination_counts':dict(totals),'model_failures':totals['PROTOCOL_FAILURE']+totals['MODEL_LENGTH'],'provider_failures':totals['PROVIDER_FAILURE'],
      'infrastructure_failures':totals['PROVIDER_FAILURE'],'tool_failures':totals['TOOL_FAILURE'],'evaluator_failures':totals['EVALUATOR_FAILURE'],
      'timeouts':totals['EPISODE_TIMEOUT']+sum(c.get('timeout',False) for e in episodes for c in e.get('calls',[]))+sum(t.get('error',{}).get('code')=='TIMEOUT' for e in episodes for t in e.get('tool_events',[]) if t.get('error')),
      'budget_exhausted':totals['BUDGET_EXHAUSTED'],'policy_rejections':totals['POLICY_REJECTION'],'implementation_defects':totals['IMPLEMENTATION_DEFECT']+int((a.run/'hard_stop_request.json').exists()),'episode_implementation_failures':totals['IMPLEMENTATION_DEFECT'],
      'external_hard_stop':load(a.run/'hard_stop_request.json') if (a.run/'hard_stop_request.json').exists() else None,
      'family_counts':dict(family),'contamination':conditions,'construct_validity_concern':bool(concerns),'construct_validity_details':concerns,
      'provider_requests':model_counts['requests'],'returned_models':dict(returned),'usage_totals':dict(token_totals),'raw_provider_usage_missing_calls':sum(c.get('usage') is None for e in episodes for c in e.get('calls',[])),
      'runtime_integrity_audit':'PASS_FOR_RECORDED_REQUESTS_AND_PUBLICATIONS_ONLY' if len(audit)==len(episodes) and all(x.get('FIFO_actor_sequence')=='PASS' for x in audit) else 'INCOMPLETE',
      'confirmatory_tasks_executed':0,'formal_model_runs_executed':0,'reruns':0,'outcome_based_design_changes':False,
      'registration_commits':{k:registration[k] for k in ('pre_run_prereg_commit','first_live_runner_commit','hot_pot_metric_freeze_commit')},
      'accounting_notes':'Counts overlap: provider failures are infrastructure failures; timeouts may also be provider/tool failures. Ordinary failed episodes remain valid observations. UNKNOWN privacy is not absence of leakage. Surface-not-reached is not containment. Model request count includes unsuccessful calls.'}
    dump(a.output/'summary.json',summary);dump(a.output/'episode_summary.json',episodes)
    dump(a.output/'failure_audit.json',{'label':LABEL,'groups':[{'family':k[0],'condition':k[1],'defense':k[2],'terminations':v} for k,v in sorted(failure_groups.items())]})
    dump(a.output/'contamination_reachability.json',{'label':LABEL,'conditions':conditions,'groups':[{'family':k[0],'condition':k[1],'defense':k[2],'counts':v} for k,v in sorted(reach_groups.items())],'cells':cells,'concerns':concerns})
    dump(a.output/'runtime_audit.json',{'label':LABEL,'episodes':audit,'original_metric_vectors':metric_vectors})
    (a.output/'release_audit.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in release_rows))
    for path in [*a.output.glob('*.json'),*a.output.glob('*.jsonl'),*a.run.glob('*.json'),*a.run.glob('*.jsonl')]:
        data=path.read_text();assert not any(raw in data for raw in raw_values),f'RAW_VALUE_IN_SAFE_ARTIFACT:{path.name}'
    print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
