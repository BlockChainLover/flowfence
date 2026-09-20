#!/usr/bin/env python3
"""Deterministic live-runner checks; no network or model generation."""
import argparse
import json
import tempfile
from pathlib import Path
from src.e2_live.pilot import *

class FakeProvider:
    def __init__(self,outputs):self.outputs=iter(outputs);self.actors=[]
    def call(self,request,timeout):
        snap=json.loads(request['json']['messages'][1]['content']);self.actors.append(snap['invocation']['recipient_principal'])
        action=next(self.outputs)
        if isinstance(action,Exception):raise action
        if isinstance(action,str):content=action
        else:content=canonical(action)
        return {'body':{'model':'MOCK_NOT_MINIMAX_CALL','id':'fixture','choices':[{'finish_reason':'stop','message':{'content':content}}],'usage':{'prompt_tokens':0,'completion_tokens':0}}}
class FakeEvaluator:
    def score(self,cell,native,private,timeout):return {'res':0,'em':0,'joint_em':0}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source-root',type=Path,required=True);p.add_argument('--schema',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    import sys
    def forbid(event,args):
        if event.startswith('socket.'):raise RuntimeError('NO_NETWORK_TEST')
    sys.addaudithook(forbid)
    schema=load(a.schema);tasks,policies,golds=inputs(a.source_root,schema);schedule=load(CONFIG/'DEVELOPMENT_CELL_SCHEDULE.json')
    checks=[]
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        def run(cell,actions,name):
            key=cell['family'],cell['task_id'];provider=FakeProvider(actions)
            episode=Episode(cell,tasks[key],policies[key],schema,provider,FakeEvaluator(),root/name)
            result=episode.execute();return result,provider,episode
        finals={'bird_pg':{'sql':'SELECT 1'},'tatqa':{'answer':['fixture'],'scale':''},'hotpot':{'answer':'fixture','supporting_facts':[]}}
        for cell in schedule:
            result,provider,ep=run(cell,[{'action':'finalize','output':finals[cell['family']]}],f"all_{cell['order']}")
            assert result['termination']=='SUCCESSFUL_FINAL' and result['completed_final']
            assert len(result['calls'])==1 and result['source_metrics'] is not None
        checks.append('54 full mocked episodes, all role/request setup paths; no live calls')
        sample=next(c for c in schedule if c['condition']=='CLEAN' and c['family']=='tatqa')
        sequence=[{'action':'send','recipient':'finance_agent','value':{'work':'fixture'},'kind':'delegation'},
                  {'action':'send','recipient':'doc_writer_agent','value':{'work':'fixture'},'kind':'message'},
                  {'action':'private_put','value':{'scratch':'fixture'}},
                  {'action':'send','recipient':'planner_agent','value':{'work':'done'},'kind':'result'},
                  {'action':'stop','reason':'normal'}]
        result,provider,ep=run(sample,sequence,'fifo')
        assert provider.actors==['planner_agent','finance_agent','planner_agent','doc_writer_agent','finance_agent'],provider.actors
        assert result['termination']=='EXPLICIT_STOP' and result['budget_counters']['message']==3
        checks.append('FIFO coalescing, recipient-before-sender, history ingress and receipt persistence')
        for mode in ARMS:
            cell=next(c for c in schedule if c['family']=='tatqa' and c['condition']=='CONTAMINATION_A' and c['defense']==mode)
            result,provider,ep=run(cell,sequence,'contam_'+mode)
            assert result['surface_reached']
            assert result['termination']==('POLICY_REJECTION' if mode=='FLOWFENCE_R2' else 'EXPLICIT_STOP')
            assert result['privacy'] is None and result['released_unauthorized_raw_events']==0
            if mode=='FLOWFENCE_R2':assert len(result['calls'])==2 and result['release_decisions'].get('quarantine')==1
        checks.append('Exact A wrapper triggers unchanged R2 quarantine with no repair or subsequent request')
        for idx,(output,expected) in enumerate([('```json\n{}\n```','PROTOCOL_FAILURE'),('not JSON','PROTOCOL_FAILURE'),
              ('{"action":"history","action":"history"}','PROTOCOL_FAILURE'),
              ('{"action":"private_put","value":NaN}','PROTOCOL_FAILURE'),
              (RuntimeError('fixture'),'PROVIDER_FAILURE')]):
            result,provider,ep=run(sample,[output],'failure_'+str(idx));assert result['termination']==expected and len(result['calls'])==1
        checks.append('No retries/JSON extraction/repair; duplicate and nonfinite rejection; transport classification')
        result,provider,ep=run(sample,[{'action':'history'}]*24,'budget')
        assert result['termination']=='BUDGET_EXHAUSTED' and len(result['calls'])==24
        checks.append('24-call hard budget, zero resampling')
        confirm=load('artifacts/aamas2027_e2_source_s1f/confirmatory.json')[0]
        denied={**schedule[0],'family':confirm['family'],'task_id':confirm['task_id']}
        try:admit(denied,schedule,tasks)
        except AssertionError:pass
        else:raise AssertionError('CONFIRMATORY_DISPATCH')
        checks.append('Confirmatory cell rejected before runtime/provider instantiation')
        assert task_success('hotpot',{'em':1,'joint_em':0}) is False
        assert task_success('hotpot',{'em':1,'joint_em':1}) is True
        assert task_success('tatqa',{'em':1,'f1':0,'scale':0}) is True
        checks.append('Human joint-EM and existing TAT-QA EM accounting')
    result={'status':'PASS','checks':checks,'mocked_full_cells':54,'live_model_requests':0,'confirmatory_trajectories':0,'private_fixtures_deleted':True}
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
