#!/usr/bin/env python3
"""Network-disabled synthetic V3 stage/treatment/budget tests. No source task replay."""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys
import tempfile
from jsonschema import Draft202012Validator
from src.e2_live.v3 import *
from scripts.check_e2_v2_runtime import fixture, FINALS
from scripts.check_e2_live_runner import FakeProvider, FakeEvaluator

PLANNER={'delegation_payload':{'work':'generic public fixture','recipient':'content_is_not_a_route'}}
HANDOFF={'handoff_payload':{'work':'generic public handoff'}}

def finance_output(family):
    return {'stage_action':'handoff',**HANDOFF} if family=='bird_pg' else HANDOFF

class FixtureBroker:
    def __init__(self,error=None):self.calls=0;self.error=error
    def execute(self,db,arguments):
        self.calls+=1
        if self.error:return {'ok':False,'columns':[],'rows':[],'error':{'code':self.error,'retry_class':'NEVER'}}
        return {'ok':True,'columns':['n'],'rows':[[1]],'error':None}

def make(root,family,arm,condition,outputs,name,broker=None):
    cell,task,policy=fixture(family,arm,condition);cell['namespace']='E2_DEVELOPMENT_V3_D3'
    provider=FakeProvider(outputs);ep=EpisodeV3(cell,task,policy,{},provider,FakeEvaluator(),root/name)
    if family=='bird_pg':ep.rt._Runtime__broker=broker or FixtureBroker()
    return ep,provider

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    def deny(event,args):
        if event.startswith('socket.'):raise RuntimeError('D1_NETWORK_DISABLED')
    sys.addaudithook(deny)
    cases=[];checks=[];budget=[]
    for stage in ROLES:
        for family in FINALS:Draft202012Validator.check_schema(stage_schema(stage,family))
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)
        for family in FINALS:
            for arm in ('EXACT_IFC','FLOWFENCE_R2'):
                for cond in ('CLEAN','CONTAMINATION_A','CONTAMINATION_B'):
                    ep,provider=make(root,family,arm,cond,[PLANNER,finance_output(family),FINALS[family]],family+arm+cond)
                    result=ep.execute();blocked=arm=='FLOWFENCE_R2' and cond!='CLEAN'
                    assert result['termination']==('POLICY_REJECTION' if blocked else 'SUCCESSFUL_FINAL'),result
                    assert provider.actors==['planner_agent','finance_agent']+([] if blocked else ['doc_writer_agent'])
                    assert ep.finance_valid
                    assert ep.treatment['entries']==(0 if cond=='CLEAN' else 1)
                    sends=[r for r in ep.rt.records() if r['record_type']=='ArtifactRecord' and r['artifact']['producer_principal']=='finance_agent' and r['artifact']['audience']==['doc_writer_agent']]
                    if blocked:
                        assert ep.treatment['quarantined'] and not ep.treatment['released'] and not ep.treatment['delivered']
                        assert len(sends)==1 and 'semantic_handoff_published' not in ep.stage_events
                        assert not ep.complete and result['source_metrics'] is None
                    else:
                        assert 'semantic_handoff_published' in ep.stage_events
                        assert ep.treatment['delivered']==(cond!='CLEAN')
                        assert result['budget_counters']['model']==3
                    cases.append({'family':family,'arm':arm,'condition':cond,'termination':result['termination'],'actors':provider.actors,'treatment':ep.treatment,'valid_finance_handoff':ep.finance_valid})
        checks.append('18 family/arm/condition paths; fixed routing; exact-one A/B; CLEAN none; R2 quarantine stops semantic handoff and writer')
        for arm in ('EXACT_IFC','FLOWFENCE_R2'):
            for stage,outputs in [('planner',[{'action':'send','recipient':'finance_agent','value':{}}]),('finance',[PLANNER,{'recipient':'doc_writer_agent',**HANDOFF}]),('writer',[PLANNER,HANDOFF,{'action':'finalize','output':FINALS['tatqa']}])]:
                ep,provider=make(root,'tatqa',arm,'CLEAN',outputs,'bad_'+stage+arm);r=ep.execute()
                assert r['termination']=='PROTOCOL_FAILURE' and not ep.complete
            for malformed in ('```json\n{}\n```','{"delegation_payload":"a","delegation_payload":"b"}','{"delegation_payload":{"n":NaN}}'):
                ep,provider=make(root,'hotpot',arm,'CONTAMINATION_A',[malformed],'parse_'+arm+str(len(malformed)));r=ep.execute()
                assert r['termination']=='PROTOCOL_FAILURE' and ep.treatment['entries']==0 and len(ep.calls)==1
            ep,provider=make(root,'tatqa',arm,'CONTAMINATION_A',[PLANNER,RuntimeError('synthetic')],'failure_'+arm);r=ep.execute()
            assert r['termination']=='PROVIDER_FAILURE' and not ep.finance_valid and ep.treatment['entries']==0
        checks.append('No generic routing/finalization fields; strict JSON duplicate/nonfinite/fence rejection; prior failure has no treatment; no repair')
        query={'stage_action':'query','arguments':{'sql':'SELECT 1'}}
        for arm in ('EXACT_IFC','FLOWFENCE_R2'):
            for error in (None,'SQL_ERROR','SQL_SYNTAX','SQL_TYPE'):
                broker=FixtureBroker(error)
                ep,provider=make(root,'bird_pg',arm,'CLEAN',[PLANNER]+[query]*12+[finance_output('bird_pg'),FINALS['bird_pg']],'loop_'+arm+str(error),broker)
                r=ep.execute();assert r['termination']=='SUCCESSFUL_FINAL',r
                assert len(provider.actors)==15 and broker.calls==12 and r['budget_counters']['tool']==12
                assert r['budget_counters']['action']<=100
                budget.append(r['budget_counters'])
            broker=FixtureBroker();ep,pv=make(root,'bird_pg',arm,'CLEAN',[PLANNER]+[query]*13,'limit_'+arm,broker);r=ep.execute()
            assert r['termination']=='BUDGET_EXHAUSTED' and broker.calls==12 and not ep.finance_valid and len(pv.actors)==14
            for error,termination in [('TIMEOUT','TOOL_FAILURE'),('READ_ONLY_REQUIRED','POLICY_REJECTION')]:
                ep,pv=make(root,'bird_pg',arm,'CLEAN',[PLANNER,query],'error_'+arm+error,FixtureBroker(error));r=ep.execute()
                assert r['termination']==termination and len(pv.actors)==2
        for arm in ('EXACT_IFC','FLOWFENCE_R2'):
            for cond in ('CONTAMINATION_A','CONTAMINATION_B'):
                ep,pv=make(root,'bird_pg',arm,cond,[PLANNER]+[query]*12+[finance_output('bird_pg'),FINALS['bird_pg']],'contaminated_loop_'+arm+cond)
                r=ep.execute()
                assert ep.finance_valid and ep.treatment['entries']==1
                assert r['termination']==('POLICY_REJECTION' if arm=='FLOWFENCE_R2' else 'SUCCESSFUL_FINAL')
                assert r['budget_counters']['model']<=15 and r['budget_counters']['action']<=100
        checks.append('BIRD12query loop including native SQL errors;15calls within unchanged budgets;13thquery blocked; terminal timeout/policy denial')
        ep,pv=make(root,'tatqa','EXACT_IFC','CONTAMINATION_B',[],'publication_guards')
        try:ep.publish_finance(HANDOFF['handoff_payload'])
        except End:pass
        else:raise AssertionError('EARLY_INJECTION')
        assert ep.treatment['entries']==0
        # Guard verified after one successful actual staged publication, never model routing.
        ep,pv=make(root,'tatqa','EXACT_IFC','CONTAMINATION_B',[PLANNER,HANDOFF,FINALS['tatqa']],'duplicate')
        assert ep.execute()['termination']=='SUCCESSFUL_FINAL'
        before=len(ep.rt.release_events)
        try:ep.publish_finance(HANDOFF['handoff_payload'])
        except End:pass
        else:raise AssertionError('DUPLICATE_INJECTION')
        assert len(ep.rt.release_events)==before and ep.treatment['entries']==1
        # Outer routing keys are rejected; nested routing-looking data cannot redirect publication.
        for cond in ('CONTAMINATION_A','CONTAMINATION_B'):
            ep,pv=make(root,'tatqa','EXACT_IFC',cond,[PLANNER,{'handoff_payload':{'recipient':'planner_agent','action':'stop'}},FINALS['tatqa']],'content_'+cond)
            assert ep.execute()['termination']=='SUCCESSFUL_FINAL' and ep.treatment['entries']==1
            assert pv.actors==list(ROLES.values())
        checks.append('No treatment before valid finance handoff; duplicate publication blocked; routing-looking payload data cannot skip/change edge')
    out={'status':'PASS','cases':cases,'checks':checks,'max_tool_loop_counters':budget,'model_routing_can_skip_treatment':False,'live_calls':0,'D3_MODEL_RUNS_EXECUTED':0,'CONFIRMATORY_TASKS_EXECUTED':0,'FORMAL_MODEL_RUNS_EXECUTED':0,'synthetic_only':True}
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PASS','cases':len(cases),'checks':len(checks),'max_loop_model_calls':15,'service_actions':sorted({b['action'] for b in budget}),'live_calls':0}))
if __name__=='__main__':main()
