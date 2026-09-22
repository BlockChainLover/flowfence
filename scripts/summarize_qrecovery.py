#!/usr/bin/env python3
"""Read-only saved-evidence recovery audit and descriptive task-level tables."""
import argparse
from collections import Counter, defaultdict
import gzip
import json
from pathlib import Path
from src.e2_live.pilot import canonical, load, sha
from src.e2_live.qrecovery import ROOT, schedule, TrustedStateRecoveryPolicy, QuarantineEvent


def rows(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()] if path.exists() else []


def ratio(a,b): return a/b if b else None


def execution_accounting(cells, attempts, terminal):
    scheduled_ids = {c['cell_id'] for c in cells}
    attempted_ids = {c['cell_id'] for c in attempts}
    finished_ids = {c['cell_id'] for c in terminal}
    if len(scheduled_ids) != len(cells): raise ValueError('DUPLICATE_SCHEDULE_ID')
    if len(attempted_ids) != len(attempts):
        raise ValueError(f'DUPLICATE_FORMAL_DISPATCH: unique_attempted={len(attempted_ids)} records={len(attempts)}')
    if len(finished_ids) != len(terminal): raise ValueError('DUPLICATE_TERMINAL_ID')
    assert finished_ids <= attempted_ids <= scheduled_ids, 'EXECUTION_MEMBERSHIP_VIOLATION'
    unattempted_ids = scheduled_ids - attempted_ids
    in_flight_ids = attempted_ids - finished_ids
    assert not unattempted_ids & attempted_ids
    assert not in_flight_ids & finished_ids
    assert scheduled_ids == finished_ids | in_flight_ids | unattempted_ids
    ordered = lambda ids: [c['cell_id'] for c in cells if c['cell_id'] in ids]
    value = dict(scheduled=len(scheduled_ids), attempted=len(attempted_ids), finished=len(finished_ids),
        in_flight=len(in_flight_ids), unattempted=len(unattempted_ids),
        scheduled_ids=ordered(scheduled_ids), attempted_ids=ordered(attempted_ids), finished_ids=ordered(finished_ids),
        in_flight_ids=ordered(in_flight_ids), unattempted_ids=ordered(unattempted_ids), partition_valid=True,
        clean_attempted=sum(c['cell_id'] in attempted_ids and c['condition']=='CLEAN' for c in cells),
        contaminated_attempted=sum(c['cell_id'] in attempted_ids and c['condition']!='CLEAN' for c in cells))
    assert value['attempted'] == value['finished'] + value['in_flight']
    assert value['scheduled'] == value['finished'] + value['in_flight'] + value['unattempted']
    return value


def analyze(new, old, cells, attempts):
    allrows = old+new
    table_a=[]
    for defense in ('EXACT_IFC','FLOWFENCE_R2','FLOWFENCE_RECOVERY'):
        es=[e for e in allrows if e['defense']==defense and e['condition']!='CLEAN']
        reached=[e for e in es if e.get('treatment',{}).get('entries',0)>0]
        table_a.append(dict(defense=defense,attempted=len(es),treatment_reaching=len(reached),
            original_artifact_released=sum(e.get('treatment',{}).get('released',False) for e in reached),
            original_artifact_reaches_writer=sum(e.get('treatment',{}).get('delivered',False) for e in reached),
            quarantined=sum(e.get('treatment',{}).get('quarantined',False) for e in reached),
            recovery_attempted=sum(e.get('recovery',{}).get('attempted',False) for e in reached),
            writer_invoked_after_quarantine=sum(e.get('recovery',{}).get('writer_invoked',False) for e in reached),
            schema_valid_finals=sum(e.get('completed_final',False) for e in reached),
            final_rate_treatment_reaching=ratio(sum(e.get('completed_final',False) for e in reached),len(reached))))
    groups=defaultdict(list)
    task_groups=defaultdict(list)
    for e in allrows:
        groups[e['family'],e['condition'],e['defense']].append(e)
        task_groups[e['family'],e['condition'],e['defense'],e['task_id']].append(e)
    utility=[]; privacy=[]; task_rows=[]
    for (family,condition,defense),es in sorted(groups.items()):
        scored=[e for e in es if e.get('source_metrics') is not None]
        success=sum(e.get('task_success') is True for e in es)
        keys=sorted({k for e in scored for k in e['source_metrics']})
        utility.append(dict(family=family,condition=condition,defense=defense,attempted=len(es),scored=len(scored),native_success=success,
            success_over_attempted=ratio(success,len(es)),success_over_scored=ratio(success,len(scored)),
            original_metric_means_scored={k:sum(e['source_metrics'][k] for e in scored)/len(scored) for k in keys}))
        privacy.append(dict(family=family,condition=condition,defense=defense,
            TRUE=sum(e.get('privacy') is True for e in es),FALSE=sum(e.get('privacy') is False for e in es),
            UNKNOWN=sum(e.get('privacy') is None for e in es)))
    for (family,condition,defense,task),es in sorted(task_groups.items()):
        scored=[e for e in es if e.get('source_metrics') is not None]
        task_rows.append(dict(family=family,condition=condition,defense=defense,task_id=task,attempted=len(es),scored=len(scored),
            native_success=sum(e.get('task_success') is True for e in es),
            success_rate=ratio(sum(e.get('task_success') is True for e in es),len(es)),
            final_rate=ratio(sum(e.get('completed_final',False) for e in es),len(es))))
    paired=[]
    for condition in ('CONTAMINATION_A','CONTAMINATION_B'):
        for family in ('tatqa','hotpot'):
            recovery={r['task_id']:r for r in task_rows if (r['condition'],r['family'],r['defense'])==(condition,family,'FLOWFENCE_RECOVERY')}
            for baseline in ('EXACT_IFC','FLOWFENCE_R2'):
                prior={r['task_id']:r for r in task_rows if (r['condition'],r['family'],r['defense'])==(condition,family,baseline)}
                matched=sorted(set(recovery)&set(prior))
                pairs=[dict(task_id=t,recovery_attempted=recovery[t]['attempted'],baseline_attempted=prior[t]['attempted'],
                    success_rate_difference=recovery[t]['success_rate']-prior[t]['success_rate'],
                    final_rate_difference=recovery[t]['final_rate']-prior[t]['final_rate']) for t in matched]
                paired.append(dict(family=family,condition=condition,baseline=baseline,paired_tasks=len(pairs),
                    equal_weight_success_difference=ratio(sum(p['success_rate_difference'] for p in pairs),len(pairs)),
                    equal_weight_final_difference=ratio(sum(p['final_rate_difference'] for p in pairs),len(pairs)),pairs=pairs))
    means=[]
    for family,condition,defense in sorted(groups):
        ts=[r for r in task_rows if (r['family'],r['condition'],r['defense'])==(family,condition,defense)]
        means.append(dict(family=family,condition=condition,defense=defense,tasks=len(ts),
            success_rate_equal_weight=ratio(sum(t['success_rate'] for t in ts),len(ts)),
            final_rate_equal_weight=ratio(sum(t['final_rate'] for t in ts),len(ts))))
    recovered=[e for e in new if e.get('recovery',{}).get('attempted')]
    contaminated=[e for e in new if e['condition']!='CLEAN']
    integrity=dict(treatment_reaching=sum(e.get('treatment',{}).get('entries',0)>0 for e in contaminated),
        quarantine_committed=sum(e.get('treatment',{}).get('quarantined',False) for e in contaminated),
        recovery_attempted=len(recovered),original_artifact_released=sum(e.get('treatment',{}).get('released',False) for e in contaminated),
        artifact_writer_exposure=sum(e.get('recovery',{}).get('writer_exposure') is True for e in recovered),
        artifact_reentry=sum(e.get('recovery',{}).get('artifact_reentry') is True for e in recovered),
        valid_provenance=sum(e.get('recovery',{}).get('provenance_valid') is True for e in recovered),
        writer_invoked=sum(e.get('recovery',{}).get('writer_invoked',False) for e in recovered),
        final_produced=sum(e.get('completed_final',False) for e in recovered))
    execution=execution_accounting(cells, attempts, new)
    execution.update(implementation_defects=[e['cell_id'] for e in new if e['termination']=='IMPLEMENTATION_DEFECT'],
        termination_counts=dict(Counter(e['termination'] for e in new)),
        completed_finals=sum(e.get('completed_final',False) for e in new))
    treatment=[dict(cell_id=e['cell_id'],scheduled=e['condition']!='CLEAN',
        valid_pre_handoff=e.get('valid_finance_handoff'),treatment=e.get('treatment'),recovery=e.get('recovery'),
        schema_valid_final=e.get('completed_final'),evaluator=e.get('source_metrics'),privacy=e.get('privacy'),termination=e['termination']) for e in new]
    failures=[dict(cell_id=c['cell_id'],termination='UNATTEMPTED',recovery_failure=None) for c in cells if c['cell_id'] in execution['unattempted_ids']]
    failures += [dict(cell_id=cid,termination='IN_FLIGHT',recovery_failure=None) for cid in execution['in_flight_ids']]
    failures += [dict(cell_id=e['cell_id'],termination=e['termination'],recovery_failure=e.get('recovery_failure'),
                     defects=e.get('live_integrity_defects',[])) for e in new if e['termination']!='SUCCESSFUL_FINAL']
    return {'execution_summary':execution,'containment_continuation':table_a,'evaluator_summary':utility,'privacy_summary':privacy,
            'recovery_provenance_summary':integrity,'treatment_reachability':treatment,'failure_audit':failures,
            'task_level_summary':dict(tasks=task_rows,equal_weight=means,paired=paired),
            'original_metric_vectors':[dict(cell_id=e['cell_id'],family=e['family'],metrics=e.get('source_metrics')) for e in new]}


def audit(new,private):
    checked=0;provenance=[]
    for e in new:
        path=private/e['cell_id']/'trajectory.json'
        if not path.exists():
            assert e['termination']=='IMPLEMENTATION_DEFECT'
            continue
        assert sha(path.read_bytes())==e['trajectory_sha256'], 'TRAJECTORY_CHANGED'
        raw=load(path);checked+=1
        assert raw['cell']=={k:e[k] for k in raw['cell']}
        violated=any(p['unauthorized_raw'] for p in raw['published_views'])
        complete=e.get('completed_final',False)
        privacy=True if violated else False if complete and e['termination'] in ('SUCCESSFUL_FINAL','EVALUATOR_FAILURE') else None
        assert e.get('privacy') is privacy
        if e.get('source_metrics') is not None:
            assert load(private/e['cell_id']/'evaluator/evaluator_output.json')==e['source_metrics']
        if e.get('recovery',{}).get('attempted'):
            sources=load(private/e['cell_id']/'recovery_sources.json')
            p=sources['provenance']
            expected=TrustedStateRecoveryPolicy().recover(canonical(sources['task_initial']),{},QuarantineEvent(p['quarantined_artifact_id']))
            assert sources['structured_state']=={} and sources['reconstructed_values']==expected.values
            assert p['artifact_sources']==[] and p['fields']==expected.provenance['fields']
            task_records=[r for r in raw['typed_records'] if r['record_type']=='StateObject' and r['kind']=='TASK_STATE']
            assert len(task_records)==1
            initial_artifact=task_records[0]['artifact_ref']
            events=[x for x in raw['release_events'] if x['artifact']==initial_artifact and x['category']=='TASK_STATE']
            assert events and all(json.loads(x['attempted'])==sources['task_initial'] for x in events)
            qevents=[x for x in raw['release_events'] if x['artifact']==p['quarantined_artifact_id']]
            assert qevents and not any(x['accepted'] for x in qevents)
            assert any((x['decision'] or {}).get('decision')=='quarantine' for x in qevents)
            for call in raw['calls']:
                if call['principal']!='doc_writer_agent': continue
                snapshot=json.loads(call['request']['json']['messages'][1]['content'])
                assert snapshot['values']==expected.values and snapshot['history']==[]
                assert [x['artifact_ref'] for x in snapshot['invocation']['context']]==[initial_artifact]
            provenance.append(dict(cell_id=e['cell_id'],source_object_verified=True,writer_input_verified=e['recovery']['writer_invoked'],fields=p['fields'],artifact_sources=[]))
    return dict(status='PASS',trajectories_verified=checked,recovery_sources=provenance)


def table(records,columns):
    return '\n'.join(['| '+' | '.join(columns)+' |','| '+' | '.join(['---']*len(columns))+' |']+
        ['| '+' | '.join(str(r.get(c)) for c in columns)+' |' for r in records])


def report(data,reg,finished):
    ex=data['execution_summary']; integ=data['recovery_provenance_summary']
    status=('FORMAL_COMPLETED_AFTER_AUTHORIZED_REPORTING_CORRECTION' if reg.get('reporting_fix_sha') else 'FINISHED') if finished and ex['finished']==280 and not ex['implementation_defects'] else 'INCOMPLETE_OR_STOPPED'
    text=f'''# QRecovery formal report

Status: {status}. Preregistration {reg['preregistration_commit']}; implementation {reg['implementation_commit']}.

Scheduled280; attempted{ex['attempted']}; finished{ex['finished']}; clean{ex['clean_attempted']}; contaminated{ex['contaminated_attempted']}; implementation defects{len(ex['implementation_defects'])}. Every ordinary failure stays in attempted denominators. Historical720unchanged and never rerun.

## Table A — containment and continuation (contaminated)

'''
    text+=table(data['containment_continuation'],['defense','attempted','treatment_reaching','original_artifact_released','original_artifact_reaches_writer','quarantined','recovery_attempted','writer_invoked_after_quarantine','schema_valid_finals'])
    text+='\n\n## Table B — native utility (separate benchmarks)\n\n'
    text+=table(data['evaluator_summary'],['family','defense','condition','attempted','scored','native_success','success_over_attempted','success_over_scored'])
    text+='\n\n## Table C — raw-value privacy\n\n'
    text+=table(data['privacy_summary'],['family','defense','condition','TRUE','FALSE','UNKNOWN'])
    text+='\n\n## Table D — recovery integrity\n\n'+table([integ],list(integ))
    text+='\n\n## Task-level descriptive comparisons\n\n'
    text+=table(data['task_level_summary']['paired'],['family','condition','baseline','paired_tasks','equal_weight_success_difference','equal_weight_final_difference'])
    text+='\n\nTask-level rows, equal-weight means and original evaluator metric vectors are retained in derived/. Repetitions are not independent semantic samples. No new significance method or pooled cross-benchmark utility is introduced. Exact IFC comparisons are descriptive; neither superiority nor equivalence is established. Historical versus new runs may differ in provider time/cohort. CLEAN one-repetition results are only a regression check.\n'
    text+=f"\nRecognized-artifact writer exposure: {integ['artifact_writer_exposure']}; reentry: {integ['artifact_reentry']}. Terminal R2 has zero writer exposure and zero treatment-reaching contaminated finals. Recovery produced {integ['final_produced']} finals after {integ['recovery_attempted']} recovery attempts. These counts must be read with pre-handoff failures and provenance availability, not interpreted as general confidentiality.\n"
    text+='\nThis implementation reconstructs from public task/evidence only; it has no independent structured finance result. Zero reentry plus nonzero continuation would support only the bounded claim that terminal rejection is not architecturally necessary under this separation. Low or zero utility is retained without tuning. TRUE/FALSE/UNKNOWN use the frozen observation rule; no exposure is not automatically FALSE. No paper claim is promoted and no anonymous manuscript is edited.\n'
    text+='\nTermination accounting: '+json.dumps(ex['termination_counts'])+'\n\nSTOP for human scientific review. No further experiment, retry, merge or paper revision is authorized by this report.\n'
    if reg.get('reporting_fix_sha'):
        text += ('\n## Authorized reporting interruption and continuation\n\n'
                 'The formal run stopped after10CLEANobservations because in-flight IDs overlapped unattempted IDs. '
                 'Human review classified this as reporting-only and retained all10observations without rerun. '
                 'The reporting correction and partition validation preceded every contaminated recovery execution. '
                 'The original STOP and defective snapshots remain immutable. Remaining270identities are dispatched once by attempted-ID membership. '
                 'Scientific recovery implementation remains '+reg['implementation_commit']+'.\n\n'
                 'HARD_STOP_SHA: '+reg['hard_stop_sha']+'; AMENDMENT_SHA: '+reg['amendment_sha']+
                 '; REPORTING_FIX_SHA: '+reg['reporting_fix_sha']+'.\n\n'
                 f"Accounting: scheduled={ex['scheduled']}, attempted={ex['attempted']}, finished={ex['finished']}, "
                 f"in_flight={ex['in_flight']}, unattempted={ex['unattempted']}. Historical reporting defects corrected:1. "
                 f"New episode implementation defects:{len(ex['implementation_defects'])}.\n")
    return text


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--run',type=Path,default=ROOT/'run')
    p.add_argument('--continuation',type=Path,help='Read-only merge with separate authorized continuation run')
    p.add_argument('--output',type=Path,default=ROOT/'combined/derived')
    p.add_argument('--report',type=Path,default=Path('QRECOVERY_FORMAL_REPORT.md'))
    a=p.parse_args()
    reg=load(a.run/'registration.json'); new=rows(a.run/'episodes.jsonl'); attempts=rows(a.run/'attempts.jsonl')
    cells=reg['schedule']; assert cells==schedule()
    audits=[audit(new,Path(reg['private_root']))]
    terminal=(a.run/'completion.json').exists()
    if a.continuation:
        cr=load(a.continuation/'registration.json')
        assert cr['schedule']==cells and cr['implementation_commit']==reg['implementation_commit']
        suffix=rows(a.continuation/'episodes.jsonl')
        suffix_attempts=rows(a.continuation/'attempts.jsonl')
        assert not {c['cell_id'] for c in attempts} & {c['cell_id'] for c in suffix_attempts}
        audits.append(audit(suffix,Path(cr['private_root'])))
        new += suffix; attempts += suffix_attempts; reg=cr
        terminal=terminal and (a.continuation/'completion.json').exists()
    assert [e['cell_id'] for e in attempts]==[c['cell_id'] for c in cells[:len(attempts)]]
    assert [e['cell_id'] for e in new]==[c['cell_id'] for c in cells[:len(new)]]
    old=json.loads(gzip.decompress(Path('artifacts/aamas2027_e2a_combined/derived/episode_summary.json.gz').read_bytes()))
    data=analyze(new,old,cells,attempts)
    data['saved_evidence_audit']=dict(status='PASS',trajectories_verified=sum(x['trajectories_verified'] for x in audits),
        recovery_sources=[s for x in audits for s in x['recovery_sources']])
    a.output.mkdir(parents=True,exist_ok=True)
    for name,value in data.items(): (a.output/(name+'.json')).write_text(json.dumps(value,indent=2)+'\n')
    a.report.write_text(report(data,reg,terminal))
    print(json.dumps({k:v for k,v in data['execution_summary'].items() if not k.endswith('_ids')}))
if __name__=='__main__':main()
