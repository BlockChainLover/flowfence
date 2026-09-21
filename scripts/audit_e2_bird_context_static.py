#!/usr/bin/env python3
"""C0 public-input serialization audit; no model, SQL engine, or evaluator execution."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
from src.e2_live.pilot import load, canonical
from src.e2_live.v3 import EpisodeV3
from src.e2_live.bird_context_audit import pack, unpack, semantic_items, wire_bytes, duplicate_stats, size
from src.e2_s1.adapters import task_input
from scripts.check_e2_v2_runtime import fixture


class ForbiddenDispatch:
    def call(self, *args, **kwargs):raise AssertionError('MODEL_DISPATCH_FORBIDDEN')
    def score(self, *args, **kwargs):raise AssertionError('EVALUATOR_FORBIDDEN')


class DeterministicBroker:
    def __init__(self, profile):self.profile=profile;self.calls=0
    def execute(self, db, arguments):
        self.calls+=1
        assert arguments=={'sql':'SELECT 1'}, 'TASK_SPECIFIC_QUERY_FORBIDDEN'
        rows=([['fixed',1]] if self.profile=='identical_small_results' else
              [[f'action{self.calls:02d}_row{i:04d}_'+('x'*64),i] for i in range(256)])
        return {'ok':True,'columns':['fixture_text','fixture_number'],'rows':rows,'error':None}


def verify_packet(snap, ep):
    original=deepcopy(snap);events=deepcopy(ep.rt.release_events);records=deepcopy(ep.rt.records())
    packet=pack(snap);expanded=unpack(packet)
    assert expanded==snap and semantic_items(expanded)==semantic_items(snap)
    assert packet['header']['invocation']==snap['invocation']
    assert ep.rt.release_events==events and ep.rt.records()==records
    # Both directions are detached; lookup is solely into this already-released packet.
    expanded['values'][0]['c0_mutation_probe']=True
    assert snap==original and 'c0_mutation_probe' not in unpack(packet)['values'][0]
    mutated=deepcopy(packet);mutated['released_value_pool'][0]['c0_mutation_probe']=True
    assert snap==original
    for bad in (-1,True,len(packet['released_value_pool'])):
        changed=deepcopy(packet);changed['values_pool_indices'][0]=bad
        try:unpack(changed)
        except ValueError:pass
        else:raise AssertionError('INVALID_REFERENCE_ACCEPTED')
    return packet


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-root',type=Path,required=True);p.add_argument('--schema',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    def deny(event,args):
        if event.startswith('socket.'):raise RuntimeError('C0_NETWORK_DISABLED')
    sys.addaudithook(deny)
    manifests={'V1':'aamas2027_e2_source_s1f/development.json','D2':'aamas2027_e2_v2_d2/development.json',
               'D3':'aamas2027_e2_v3_d3/development.json','confirmatory':'aamas2027_e2_source_s1f/confirmatory.json'}
    selected=[(split,str(r['task_id'])) for split,path in manifests.items() for r in load(Path('artifacts')/path) if r['family']=='bird_pg']
    assert len(selected)==29 and len({tid for _,tid in selected})==29
    # Project only public fields immediately. No reference answer/difficulty is accessed.
    public={str(r['question_id']):{k:r[k] for k in ('question_id','question','db_id','evidence')}
            for r in load(a.source_root/'data/birdsql__bird_mini_dev__data__mini_dev_pg-00000-of-00001.json')}
    schema=load(a.schema);rows=[];protected=[];pairs=0
    with tempfile.TemporaryDirectory() as td:
        for split,tid in selected:
            record=public[tid];tables=schema[record['db_id']]['tables']
            task=task_input('bird_pg',record,schema=tables,descriptions={k:v['description_csv'] for k,v in tables.items()})
            for profile in ('identical_small_results','distinct_256_row_results'):
                paired=None
                for arm in ('EXACT_IFC','FLOWFENCE_R2'):
                    cell,_,policy=fixture('bird_pg',arm,'CLEAN')
                    ep=EpisodeV3(cell,task,policy,{},ForbiddenDispatch(),ForbiddenDispatch(),Path(td)/'unused')
                    protected.append(ep.pol.raw_value);broker=DeterministicBroker(profile);ep.rt._Runtime__broker=broker
                    ep.stage='planner';initial=ep.snapshot('planner_agent');initial_packet=verify_packet(initial,ep)
                    assert ep.pol.raw_value not in canonical(initial_packet)
                    ep.service('planner_agent','send',recipient='finance_agent',value={'delegation_payload':{'work':'Fixed C0 public fixture'}},kind='delegation')
                    ep.stage='finance';measure=[];pair_values=[]
                    for n in range(13):
                        if n:
                            result=ep.service('finance_agent','query',arguments={'sql':'SELECT 1'})
                            ep.scratch['finance_agent']=ep.service('finance_agent','private_put',value=result)
                        snap=ep.snapshot('finance_agent');packet=verify_packet(snap,ep)
                        before=wire_bytes('finance',snap);after=wire_bytes('finance',packet)
                        measure.append({'sql_actions':n,'before_bytes':before,'after_bytes':after,'net_bytes_removed':before-after,**duplicate_stats(snap)})
                        pair_values.append(canonical(packet))
                    assert broker.calls==12 and ep.budget.counts['tool']==12 and not ep.calls
                    # Old/new representation must not widen the recipient's access.
                    try:ep.rt.session('doc_writer_agent').context(('private:finance_agent',))
                    except Exception as exc:
                        assert type(exc).__name__=='Rejected'
                    else:raise AssertionError('PRIVATE_RECIPIENT_BYPASS')
                    if paired is None:paired=pair_values
                    else:assert pair_values==paired;pairs+=len(pair_values)
                    rows.append({'split':split,'task_id':tid,'arm':arm,'fixture_profile':profile,
                                 'task_bytes':size(task),'initial_planner_before_bytes':wire_bytes('planner',initial),
                                 'initial_planner_after_bytes':wire_bytes('planner',initial_packet),'finance':measure,
                                 'finance_max_before_bytes':max(m['before_bytes'] for m in measure),
                                 'finance_max_after_bytes':max(m['after_bytes'] for m in measure),
                                 'max_net_bytes_removed':max(m['net_bytes_removed'] for m in measure),
                                 'service_budget_counts':dict(ep.budget.counts)})
            print(json.dumps({'public_task_serialization_completed':len(rows)//4,'of':29}),flush=True)
    out={'status':'PASS_STATIC_FIXTURE_AUDIT_NOT_CONTEXT_CLOSURE','selected_tasks':29,'confirmatory_public_inputs':20,
         'fixture_episodes':len(rows),'finance_snapshots':len(rows)*13,'paired_finance_snapshots':pairs,
         'context_guard':160000,'true_worst_case_bound':'NO_FINITE_BOUND_FROM_FROZEN_CAPABILITIES',
         'worst_case_reason':'12 SQL actions bounds count, not result rows/bytes; broker fetchall has no result-size bound.',
         'semantic_equivalence':'VERIFIED','parity':'VERIFIED','mediation':'VERIFIED',
         'certification_scope':'Offline candidate and released deterministic snapshots only; no model interpretation or live integration certified.',
         'max_fixture_before_bytes':max(r['finance_max_before_bytes'] for r in rows),
         'max_fixture_after_bytes':max(r['finance_max_after_bytes'] for r in rows),
         'max_fixture_net_bytes_removed':max(r['max_net_bytes_removed'] for r in rows),
         'MODEL_RUNS_EXECUTED':0,'CONFIRMATORY_TASKS_EXECUTED':0,'FORMAL_MODEL_RUNS_EXECUTED':0,
         'sql_engine_calls':0,'evaluator_calls':0,'gold_fields_accessed':False,'tasks':rows}
    encoded=json.dumps(out,indent=2)+'\n';assert not any(v in encoded for v in protected)
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(encoded)
    print(json.dumps({k:v for k,v in out.items() if k!='tasks'}))

if __name__=='__main__':main()
