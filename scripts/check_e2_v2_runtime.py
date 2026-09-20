#!/usr/bin/env python3
"""Offline synthetic staged-runtime certification; never run V1/confirmatory tasks."""
import argparse
from copy import deepcopy
import io
import json
from pathlib import Path
import socket
import sys
import tempfile
import urllib.error
from unittest.mock import patch
from src.e2_live.v2 import EpisodeV2, Scaffold, StagedSchedule, build_request
from src.e2_live.pilot import Episode, End, load, canonical, CONFIG
from src.e2_live.transport_v2 import diagnostics, TransportFailure, provider_worker
from scripts.check_e2_live_runner import FakeProvider, FakeEvaluator


def fixture(family, arm='EXACT_IFC', condition='CLEAN'):
    templates=load('experiments/e2_source_s1f/policy_templates.json')
    typ={'bird_pg':'P4','tatqa':'P1','hotpot':'P2'}[family]
    policy={k:deepcopy(v) for k,v in templates.items() if k not in ('fact_templates','ordinal_rule','secret_id_rule','limitations')}
    policy.update(family=family,task_id='SYNTHETIC_D1',split='synthetic_certification',fact_type=typ,
                  fact_generation_template=templates['fact_templates'][typ],generation_ordinal=100,secret_id='synthetic_d1_private')
    task={'task_id':'SYNTHETIC_D1','question':'Offline protocol fixture, not a source task.'}
    if family=='bird_pg':task.update(db_id='fixture',schema={},descriptions={})
    if family=='tatqa':task.update(uid='SYNTHETIC_D1',table=[],paragraphs=[])
    if family=='hotpot':task.update(id='SYNTHETIC_D1',context=[])
    return {'order':1,'family':family,'task_id':'SYNTHETIC_D1','condition':condition,'defense':arm,'repetition':1},task,policy


FINALS={'bird_pg':{'sql':'SELECT 1'},'tatqa':{'answer':['fixture'],'scale':''},'hotpot':{'answer':'fixture','supporting_facts':[]}}
DELEGATE={'action':'send','recipient':'finance_agent','value':{'work':'public fixture'},'kind':'delegation'}
HANDOFF={'action':'send','recipient':'doc_writer_agent','value':{'result':'public fixture'},'kind':'result'}


def run_fixture(root, family, arm, condition, actions, name, cls=EpisodeV2):
    cell,task,policy=fixture(family,arm,condition)
    provider=FakeProvider(actions)
    episode=cls(cell,task,policy,{},provider,FakeEvaluator(),root/name)
    return episode.execute(),episode,provider


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    def deny(event, details):
        if event.startswith('socket.'):
            raise RuntimeError('D1_NETWORK_DISABLED')
    sys.addaudithook(deny)
    checks=[];counters=[];cases=[]
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)
        for family in FINALS:
            for arm in ('EXACT_IFC','FLOWFENCE_R2'):
                for condition in ('CLEAN','CONTAMINATION_A','CONTAMINATION_B'):
                    actions=[DELEGATE,HANDOFF,{'action':'finalize','output':FINALS[family]}]
                    r,ep,provider=run_fixture(root,family,arm,condition,actions,f'{family}_{arm}_{condition}')
                    blocked=arm=='FLOWFENCE_R2' and condition!='CLEAN'
                    assert r['termination']==('POLICY_REJECTION' if blocked else 'SUCCESSFUL_FINAL'),r
                    expected=['planner_agent','finance_agent']+([] if blocked else ['doc_writer_agent'])
                    assert provider.actors==expected
                    injected=[e for e in ep.rt.release_events if '"handoff"' in e['attempted'] and e['boundary']=='B2']
                    publications=[x for x in injected if x['producer']=='finance_agent']
                    # Each injection has one initial artifact; accepted delivery repeats B2 on receive.
                    unique={x['artifact'] for x in publications}
                    assert len(unique)==(0 if condition=='CLEAN' else 1)
                    if blocked:
                        assert len(ep.rt.release_events)>0 and r['release_decisions']['quarantine']==1
                        assert not ep.scaffold.flags['FINANCE_HANDOFF_COMPLETED']
                        assert not any('"handoff"' in x['payload'] for x in ep.publications)
                    else:
                        assert ep.scaffold.events==['PLANNER_DELEGATED','FINANCE_HANDOFF_COMPLETED','DOC_WRITER_INVOKED','SCAFFOLD_COMPLETE']
                        assert r['budget_counters']['model']==3
                        assert r['budget_counters']['message']==(2 if condition=='CLEAN' else 3)
                        assert r['budget_counters']['action']<20
                        counters.append(r['budget_counters'])
                    cases.append({'family':family,'arm':arm,'condition':condition,'termination':r['termination'],
                                  'actors':provider.actors,'injection_artifacts':len(unique),'scaffold':r['scaffold_flags']})
        checks.append('18 synthetic family/arm/condition paths: clean completion, exactly-one A/B path entry, whole-artifact quarantine')
        for arm in ('EXACT_IFC','FLOWFENCE_R2'):
            for seq in ([{'action':'finalize','output':FINALS['tatqa']}], [DELEGATE,{'action':'finalize','output':FINALS['tatqa']}]):
                r,ep,p=run_fixture(root,'tatqa',arm,'CLEAN',seq,f'premature_{arm}_{len(seq)}')
                assert r['termination']=='PROTOCOL_FAILURE' and not r['completed_final'] and r['source_metrics'] is None
            # Wrong edge never injects; stop rather than scripted conversion.
            seq=[{'action':'send','recipient':'doc_writer_agent','kind':'delegation','value':{}},{'action':'stop','reason':'normal'}]
            r,ep,p=run_fixture(root,'tatqa',arm,'CONTAMINATION_A',seq,'wrong_'+arm)
            assert p.actors==['planner_agent','planner_agent'] and not ep.reached
            assert not any(ep.scaffold.flags.values())
            r,ep,p=run_fixture(root,'tatqa',arm,'CLEAN',[{'action':'history'}]*24,'budget_'+arm)
            assert r['termination']=='BUDGET_EXHAUSTED' and len(r['calls'])==24
        checks.append('Early final is protocol failure in both arms; wrong-edge cannot advance/inject; unchanged 24-call budget')
        # After writer invocation original queued planner/finance order is retained.
        seq=[DELEGATE,HANDOFF,{'action':'history'},{'action':'history'},HANDOFF,{'action':'finalize','output':FINALS['tatqa']}]
        r,ep,p=run_fixture(root,'tatqa','EXACT_IFC','CONTAMINATION_B',seq,'repeat')
        assert p.actors==['planner_agent','finance_agent','doc_writer_agent','planner_agent','finance_agent','doc_writer_agent']
        assert r['termination']=='SUCCESSFUL_FINAL' and r['budget_counters']['message']==4
        assert len({e['artifact'] for e in ep.rt.release_events if '"handoff"' in e['attempted'] and e['boundary']=='B2'})==1
        for text in ('{"action":"history","SCAFFOLD_COMPLETE":true}', '{"action":"history","action":"history"}', '{"action":"private_put","value":NaN}'):
            r,ep,p=run_fixture(root,'hotpot','EXACT_IFC','CLEAN',[text],'forge_'+str(len(text)))
            assert r['termination']=='PROTOCOL_FAILURE' and not ep.scaffold.complete
        checks.append('Deferred FIFO restored, duplicate handoff does not reinject, model cannot set flags; strict parser unchanged')
        # Frozen parameters/arm-blind prompts use identical trusted snapshots.
        cell,task,policy=fixture('tatqa')
        ep=EpisodeV2(cell,task,policy,{},FakeProvider([]),FakeEvaluator(),root/'requests')
        snap=ep.snapshot('planner_agent')
        req=build_request('planner_agent','tatqa',snap)
        assert {k:v for k,v in req['json'].items() if k!='messages'}==load(CONFIG/'LIVE_MODEL_CONFIG.json')['request_parameters']
        assert req['url']==load(CONFIG/'LIVE_MODEL_CONFIG.json')['endpoint']
        try:ep.rt.session('planner_agent').finalize(FINALS['tatqa'])
        except Exception as exc:assert str(exc)=='PREMATURE_FINALIZE'
        else:raise AssertionError('DIRECT_FINAL_BYPASS')
        checks.append('Trusted runtime rejects direct premature final; same frozen sampling/provider configuration')
        # V1 and V2 deterministic transport failure path; no historical cell replay.
        req={'url':'https://unused.invalid','headers':{},'json':{'messages':[{'content':'PRIVATE_FIXTURE_VALUE'}]}}
        key='D1_CREDENTIAL_FIXTURE_VALUE'
        error=urllib.error.HTTPError('https://unused.invalid',429,'do not retain '+key,{'x-request-id':'request_fixture_123'},io.BytesIO(json.dumps({'base_resp':{'status_code':1002,'status_msg':key}}).encode()))
        diag=diagnostics(error,req,key)
        assert diag['exception_class']=='HTTPError' and diag['http_status']==429 and diag['provider_error_code']==1002 and diag['provider_request_id']=='request_fixture_123'
        assert key not in canonical(diag)
        for echo in (key,'PRIVATE_FIXTURE_VALUE'):
            d=diagnostics(urllib.error.HTTPError('x',500,'x',{'x-request-id':echo},io.BytesIO(b'{}')),req,key)
            assert d['provider_request_id'] is None
        timeout=diagnostics(urllib.error.URLError(TimeoutError('private text')),req,key)
        assert timeout['timeout'] and timeout['underlying_exception_class']=='TimeoutError'
        assert diagnostics(ConnectionError('private text'))['http_status'] is None
        for cls,label in ((Episode,'before_v1_synthetic'),(EpisodeV2,'after_v2_synthetic')):
            r,ep,p=run_fixture(root,'tatqa','EXACT_IFC','CLEAN',[TransportFailure(diag)],label,cls=cls)
            assert r['termination']=='PROVIDER_FAILURE' and len(r['calls'])==1
            record=load(ep.private/'call_01_response.json')
            assert ('transport_diagnostics' in record)==(cls is EpisodeV2)
            if cls is EpisodeV2:assert record['transport_diagnostics']==diag and r['calls'][0]['transport_diagnostics']==diag
        # Exercise worker serialization without opening a socket.
        class Pipe:
            def send(self,value):self.value=value
            def close(self):pass
        class Opener:
            def open(self,*a,**kw):raise ConnectionError('private text')
        pipe=Pipe()
        with patch('urllib.request.build_opener',return_value=Opener()):provider_worker(pipe,req,key,240)
        assert pipe.value[0]=='error' and pipe.value[1]['exception_class']=='ConnectionError'
        checks.append('Transport before/after: V1 synthetic loses diagnostics; V2 retains HTTP/request/code/type/timeout; echo suppression; worker serialization; no retry')
    out={'status':'PASS','checks':checks,'cases':cases,'minimum_scaffold_counters':counters,
         'synthetic_only':True,'source_task_ids_used':False,'D2_MODEL_RUNS_EXECUTED':0,'CONFIRMATORY_TASKS_EXECUTED':0,'FORMAL_MODEL_RUNS_EXECUTED':0}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':'PASS','cases':len(cases),'checks':len(checks),'live_model_calls':0}))
if __name__=='__main__':main()
