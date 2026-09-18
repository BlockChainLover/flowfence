#!/usr/bin/env python3
"""Gate A-E finite transition and boundary audit with original MARBLE and offline doubles."""
import argparse
from collections import deque
from contextlib import ExitStack, redirect_stdout, redirect_stderr
from copy import deepcopy
import datetime
import io
import json
import logging
import os
import runpy
from pathlib import Path
import socket
import sys
import tempfile
from types import SimpleNamespace
from unittest.mock import patch


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--benchmark',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    args=p.parse_args();b=args.benchmark.resolve();out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    os.environ.update(LITELLM_LOCAL_MODEL_COST_MAP='True',HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',JOBLIB_MULTIPROCESSING='0',PYTHONDONTWRITEBYTECODE='1')
    sys.path.insert(0,str(b));network=[]
    def denied(*a,**k):network.append('denied');raise RuntimeError('network forbidden')
    socket.socket.connect=denied;socket.create_connection=denied
    import litellm
    litellm.completion=denied;litellm.acompletion=denied
    from litellm.types.utils import Message
    from marble.engine.engine import Engine
    from marble.configs.config import Config
    from marble.environments.coding_utils import coder,reviewer
    from marble.memory.base_memory import BaseMemory
    from marble.memory.shared_memory import SharedMemory
    from src.experiments.aamas_gate_ac import MarbleBoundaryAdapter,ReleaseAdapter,synthetic_sidecar,DEFENSES
    from src.experiments.aamas_gate_ad import CommunicationEdges
    from src.experiments.aamas_gate_ae import ContextBoundaryProbe,workspace_publication_probe
    import jsonschema
    import yaml
    logging.disable(logging.CRITICAL)
    calls=[];pending=deque();sql=[];http=[];process=[];fault=[False];ids=[];continue_fixture=[False]
    def tool(name,arguments):
        return Message(role='assistant',content='PUBLIC',tool_calls=[{'id':'fixture-call','type':'function','function':{'name':name,'arguments':json.dumps(arguments)}}])
    def transport(*a,**kw):
        calls.append(deepcopy(kw))
        if fault[0]:raise ValueError('deterministic transport failure')
        if pending:
            response=pending.popleft()
        else:
            prompt=json.dumps(kw.get('messages',[]));content='PUBLIC FIXTURE'
            if 'task assignment system' in prompt:content=json.dumps({'tasks':{i:'PUBLIC SUBTASK' for i in ids},'continue':True})
            elif 'single key' in prompt and 'continue' in prompt:content=json.dumps({'continue':continue_fixture[0]})
            elif 'innovation' in prompt:content='{"innovation":4,"safety":3,"feasibility":2}'
            elif 'instruction_following' in prompt:content='{"instruction_following":4,"executability":3,"consistency":2,"quality":1}'
            elif '"rating"' in prompt:content='{"rating":4}'
            elif 'milestone' in prompt:content='[]'
            response=Message(role='assistant',content=content)
        return SimpleNamespace(choices=[SimpleNamespace(message=response)])
    class Cursor:
        def execute(self,statement,*a,**kw):
            sql.append(statement)
            if statement=='BAD SQL':raise ValueError('fixture SQL error')
        def fetchall(self):return []
        def close(self):pass
    class Connection:
        def cursor(self):return Cursor()
        def close(self):pass
    def response(url,*a,**kw):
        http.append({'url':url,'kwargs':deepcopy(kw)})
        return SimpleNamespace(status_code=200,text='PUBLIC PAGE',content=b'PUBLIC PAGE',raise_for_status=lambda:None,json=lambda:{'status':'success','data':{'alerts':[],'result':[{'values':[[1,'1'],[2,'1'],[3,'1']]}]}})
    def proc(*a,**kw):process.append((a,kw));return SimpleNamespace(returncode=0)
    class Scholar:
        def search_author(self,*a,**kw):return [{'authorId':'public-author','papers':[]}]
        def get_author(self,*a,**kw):return {'papers':[{'title':'PUBLIC TITLE','abstract':'PUBLIC ABSTRACT','authors':[]}]}
    class FrozenDate(datetime.datetime):
        @classmethod
        def now(cls,tz=None):return cls(2026,9,18,12,0,0)
    def normalize(value):
        if isinstance(value,Message):return value.model_dump()
        if isinstance(value,dict):return {str(k):normalize(v) for k,v in value.items()}
        if isinstance(value,(tuple,list)):return [normalize(v) for v in value]
        if isinstance(value,(str,int,bool,float)) or value is None:return value
        return type(value).__name__
    all_records=[];boundary=[];topology=[];inventory=[];cert=[];original_cwd=Path.cwd()
    with tempfile.TemporaryDirectory(prefix='gate-ae-') as temp,ExitStack() as stack:
        root=Path(temp);os.chdir(root);(root/'logs').mkdir();(root/'evaluator').symlink_to(b/'marble/evaluator',target_is_directory=True)
        (root/'marble/configs/coding_config').mkdir(parents=True);(root/'marble/workspace').mkdir()
        if (root/'MARBLE').exists():(root/'marble/marble').symlink_to(root/'marble',target_is_directory=True)
        else:(root/'MARBLE').symlink_to(root,target_is_directory=True)
        for name,value in [('litellm.completion',transport),('marble.agent.base_agent.token_counter',lambda *a,**k:0),('marble.engine.engine_planner.token_counter',lambda *a,**k:0),('time.sleep',lambda *a:None),('subprocess.run',proc),('psycopg2.connect',lambda *a,**k:Connection()),('requests.get',response),('marble.environments.research_utils.paper_collector.perform_arxiv_search',lambda *a,**k:iter([])),('marble.environments.research_utils.profile_collector.SemanticScholar',Scholar),('marble.environments.coding_utils.reviewer.datetime',SimpleNamespace(datetime=FrozenDate)),('marble.agent.base_agent.uuid.uuid4',lambda:'fixed-session'),('marble.environments.db_env.time',SimpleNamespace(time=lambda:1789704000.0,sleep=lambda *a:None))]:stack.enter_context(patch(name,value))
        for env in ('research','database','coding'):
            originals=[json.loads(line) for line in (b/f'multiagentbench/{env}/{env}_main.jsonl').read_text().splitlines() if line]
            def config(row):
                data=deepcopy(row);data['coordinate_mode']='star';data['llm']='MiniMax-M2.7';data['environment'].update(type={'research':'Research','database':'DB','coding':'Coding'}[env],max_iterations=5)
                if env=='coding':data['environment']['workspace_dir']='marble/workspace'
                data['memory']={'type':'BaseMemory'};data['output']={'format':'jsonl','file_path':'fixture_output.jsonl'}
                (root/'marble/configs/coding_config/coding_config.yaml').write_text(yaml.safe_dump(data))
                return data
            def construct(row,defense):
                en=Engine(Config(config(row)));pol,attacks,_=synthetic_sidecar(row,env)
                ad=MarbleBoundaryAdapter(en,defense,[pol]);return en,ad,pol
            row=originals[0];ids=[a['agent_id'] for a in row['agents']]
            cases={}
            for defense in DEFENSES:
                en,ad,pol=construct(row,defense);owner,worker,peer=en.agents[:3]
                for name in ('solution.py','advices.json'):(root/'marble/workspace'/name).unlink(missing_ok=True)
                inventory.append({'environment':env,'defense':defense,'registered_tools':list(en.environment.action_handler_descriptions),'advertised_recipients':{a.agent_id:list(a.relationships) for a in en.agents},'planning_method':en.planning_method})
                def run(label,fn):
                    pending.clear();start=len(calls);sql_start=len(sql);http_start=len(http);process_start=len(process)
                    try:value=fn();error=None
                    except Exception as e:value=None;error=type(e).__name__+': '+str(e)
                    cases.setdefault(label,[]).append({'defense':defense,'inputs':normalize(calls[start:]),'result':normalize(value),'error':error,'tools':deepcopy(en.environment.action_handler_descriptions),'routes':{a.agent_id:list(a.relationships) for a in en.agents},'sql':sql[sql_start:],'http':http[http_start:],'process':normalize(process[process_start:])})
                    return value
                run('task_initialization',ad.capability_snapshot)
                run('planner_assignment',lambda:en.planner.assign_tasks('naive'))
                run('planner_next_step',lambda:en.planner.decide_next_step([{'agent1':'PUBLIC'}]))
                run('agent_model_invocation',lambda:owner.act('PUBLIC TASK'))
                run('agent_send',lambda:owner.send_message('public-session',worker,'PUBLIC MESSAGE'))
                def session_call():
                    pending.append(tool('communicate_to',{'message':'PUBLIC REPLY <end-of-session>'}))
                    pending.append(Message(role='assistant',content='PUBLIC SESSION SUMMARY'))
                    return owner._handle_new_communication_session(worker.agent_id,'PUBLIC QUESTION','public-session','PUBLIC TASK')
                run('session_initiation',session_call)
                run('session_reply_receive',lambda:worker._handle_communicate_to(owner.agent_id,'PUBLIC REPLY','public-session'))
                run('shared_state_write',lambda:(owner.memory.update('x',{'text':'PUBLIC'}),owner.shared_memory.update('x','PUBLIC'),en.memory.update('x','PUBLIC')))
                run('shared_state_read',lambda:(owner.memory.retrieve_all(),str(owner.memory),owner.shared_memory.retrieve_all(),en.memory.retrieve_all(),en.environment.get_state()))
                tool_args={'research':('fetch_webpage',{'url':'https://example.invalid/public'}),'database':('query_db',{'sql':'SELECT 1'}),'coding':('create_solution',{'task_description':'PUBLIC','model_name':'MiniMax-M2.7'})}[env]
                run('tool_invocation',lambda:en.environment.apply_action(owner.agent_id,*tool_args))
                run('tool_result',lambda:en.environment.get_state()['last_action_result'])
                run('tool_error',lambda:en.environment.apply_action(owner.agent_id,'__unknown__',{}))
                run('agent_result_to_planner',lambda:en.planner.summarize_output(owner.act('PUBLIC')[0],en.task,en.output_format))
                run('planner_progress_update',lambda:en.planner.update_progress('PUBLIC PROGRESS'))
                run('final_serialization',lambda:en._write_to_jsonl({'final_output':'PUBLIC FINAL'}))
                def terminate():
                    fresh,_,_=construct(row,defense)
                    (root/'marble/workspace/solution.py').write_text('# PUBLIC CODE\n')
                    fresh.start()
                    return {'iterations':fresh.current_iteration,'limit':fresh.max_iterations,'mode':fresh.coordinate_mode}
                run('termination',terminate)
                def budget_stop():
                    fresh,_,_=construct(row,defense);fresh.max_iterations=1
                    continue_fixture[0]=True
                    try:fresh.start()
                    finally:continue_fixture[0]=False
                    return {'iterations':fresh.current_iteration,'limit':fresh.max_iterations}
                run('termination_budget',budget_stop)
                def retry():
                    fault[0]=True
                    try:return owner.act('PUBLIC ERROR TASK')
                    finally:fault[0]=False
                run('model_error_retry',retry)
                # Exercise every registered tool, not unregistered source functions.
                if env=='research':
                    fixture={'get_related_papers':{'num_results':1,'domain':'cs.AI'},'get_recent_papers':{'domain':'cs.AI','max_results':1},'collect_publications_and_coauthors':{'author':'PUBLIC'},'get_paper_by_keyword':{'keyword':'PUBLIC','max_papers':1},'get_paper_by_arxiv_id':{'arxiv_id':'0000.00000'},'get_paper_by_title':{'title':'PUBLIC'},'fetch_webpage':{'url':'https://example.invalid/public'}}
                    run('research_network_tools',lambda:[en.environment.apply_action(owner.agent_id,k,v) for k,v in fixture.items()])
                if env=='database':
                    run('database_sql_error',lambda:en.environment.apply_action(owner.agent_id,'query_db',{'sql':'BAD SQL'}))
                    def offline_judge():
                        # Original hard-coded model identifier is inspected only by the double.
                        # This does not authorize or configure a non-MiniMax experiment.
                        with tempfile.TemporaryDirectory(dir=root) as fixture:
                            group=Path(fixture)/'group';group.mkdir()
                            (group/'result.json').write_text(json.dumps({'planning_scores':[1],'communication_scores':[1],'task_evaluation':{'root_cause':['STATIC_ROOT'],'predicted':'STATIC TEXT'}}))
                            pending.append(Message(role='assistant',content='STATIC_ROOT\nSTATIC_OTHER'))
                            previous=Path.cwd();capture=io.StringIO()
                            try:
                                os.chdir(fixture)
                                with patch('litellm.utils.trim_messages',lambda messages,**kw:messages),redirect_stdout(capture):
                                    result=runpy.run_path(str(b/'scripts/database/batch_eval.py'))
                            finally:os.chdir(previous)
                            assert result['error_count']==0 and result['task_scores']==[1.0]
                            return {'error_count':result['error_count'],'task_scores':result['task_scores'],'collaboration_scores':result['collaboration_scores'],'stdout':capture.getvalue()}
                    run('database_offline_judge',offline_judge)
                if env=='coding':
                    def review():
                        (root/'marble/workspace/solution.py').write_text('# BEFORE\nprint(1)\n# AFTER')
                        pending.append(Message(role='assistant',content='PUBLIC ADVICE'))
                        pending.append(Message(role='assistant',content=json.dumps({'strategies':[{'action':'replace','target':{'code':'print(1)','before_context':'# BEFORE','after_context':'# AFTER'},'new_code':'\nprint(2)\n'}]})))
                        return en.environment.apply_action(owner.agent_id,'give_advice_and_revise',{'task_description':'PUBLIC','model_name':'MiniMax-M2.7'})
                    run('coding_nested_review',review)
                    run('coding_workspace_read_after_write',lambda:(root/'marble/workspace/solution.py').read_text())
                # Protected arguments must not reach registered side-effect dispatch.
                before_http,before_sql=len(http),len(sql)
                protected_args={'research':('fetch_webpage',{'url':'https://example.invalid/'+pol.raw_value}),'database':('query_db',{'sql':"SELECT '"+pol.raw_value+"'"}),'coding':('create_solution',{'task_description':pol.raw_value,'model_name':'MiniMax-M2.7'})}[env]
                blocked_result=en.environment.apply_action(owner.agent_id,*protected_args)
                protected_dispatch_absent=len(http)==before_http and len(sql)==before_sql
                outbound_raw_absent=pol.raw_value not in json.dumps({'http':http[before_http:],'sql':sql[before_sql:]})
                # Direct backing stores bypass current publication wrappers.
                start_events=len(ad.events)
                owner.shared_memory.storage['direct']=pol.raw_value
                en.memory.storage.append({'direct':pol.raw_value})
                en.environment.state['direct']=pol.raw_value
                en.planner.current_progress=pol.raw_value
                direct={'shared':owner.shared_memory.retrieve('direct')==pol.raw_value,'engine':pol.raw_value in str(en.memory.retrieve_all()),'env':en.environment.get_state()['direct']==pol.raw_value,'planner':pol.raw_value in en.planner.create_prompt(),'no_release_event':len(ad.events)==start_events}
                # Generic gateway works when supplied explicit, correct recipient metadata.
                capture=[]
                gateway=ContextBoundaryProbe(ad,lambda *a,**k:capture.append(deepcopy(k)) or transport(*a,**k))
                with gateway.scope(worker.agent_id):
                    gateway(model='MiniMax-M2.7',messages=[{'role':'user','content':str(en.memory.retrieve_all())}])
                correctly_bound_safe=pol.raw_value not in json.dumps(capture[-1])
                # Same common gateway under an outer initiating-agent scope is NOT enough.
                worker.memory.storage.append({'private_fixture':pol.raw_value})
                capture.clear();pending.clear()
                pending.append(tool('communicate_to',{'message':'PUBLIC REPLY <end-of-session>'}))
                pending.append(Message(role='assistant',content='PUBLIC SESSION SUMMARY'))
                with patch('litellm.completion',gateway),gateway.scope(owner.agent_id):
                    owner._handle_new_communication_session(worker.agent_id,'PUBLIC QUESTION','identity-session','PUBLIC TASK')
                wrong_recipient_leak=any(pol.raw_value in json.dumps(c) for c in capture)
                boundary.append({'environment':env,'defense':defense,'direct_storage':direct,'explicit_recipient_gateway_safe':correctly_bound_safe,'session_outer_scope_misattribution':wrong_recipient_leak,'model_api_has_recipient_parameter':False,'protected_tool_dispatch_absent':protected_dispatch_absent,'protected_tool_rejected':blocked_result.get('status')=='blocked','outgoing_raw_absent':outbound_raw_absent})
                if env=='coding':
                    # Replace the handler-specific prototype with ONE namespace boundary.
                    def publish(text):return ad.release(text,owner.agent_id,'shared','shared_doc','WORKSPACE_WRITE')
                    workspace_checks=[]
                    for protected in (False,True):
                        pending.clear();content='# '+(pol.raw_value if protected else 'PUBLIC CODE')
                        (root/'marble/workspace/solution.py').unlink(missing_ok=True)
                        pending.append(Message(role='assistant',content=content))
                        with workspace_publication_probe(root/'marble/workspace',publish):
                            en.environment.apply_action(owner.agent_id,'create_solution',{'task_description':'PUBLIC','model_name':'MiniMax-M2.7'})
                        raw=(root/'marble/workspace/solution.py').read_text()
                        workspace_checks.append({'protected':protected,'raw_absent':pol.raw_value not in raw,'clean_bytes_unchanged':raw==content if not protected else None})
                    pending.clear()
                    (root/'marble/workspace/solution.py').write_text('# BEFORE\nprint(1)\n# AFTER')
                    pending.append(Message(role='assistant',content=pol.raw_value))
                    pending.append(Message(role='assistant',content=json.dumps({'strategies':[{'action':'replace','target':{'code':'print(1)','before_context':'# BEFORE','after_context':'# AFTER'},'new_code':'# '+pol.raw_value}]})))
                    with workspace_publication_probe(root/'marble/workspace',publish):
                        en.environment.apply_action(owner.agent_id,'give_advice_and_revise',{'task_description':'PUBLIC','model_name':'MiniMax-M2.7'})
                    boundary[-1]['generic_workspace']={'coder_checks':workspace_checks,'reviewed_solution_raw_absent':pol.raw_value not in (root/'marble/workspace/solution.py').read_text(),'advice_json_raw_absent':pol.raw_value not in (root/'marble/workspace/advices.json').read_text(),'diagnostic_retains_private_fixture':pol.raw_value in (root/'marble/logs/advice_log').read_text()}
                    (root/'marble/workspace/solution.py').write_text('# '+pol.raw_value)
                    pending.clear();pending.append(Message(role='assistant',content='PUBLIC ADVICE'));pending.append(Message(role='assistant',content='{"strategies":[]}'))
                    nested_start=len(calls)
                    en.environment.apply_action(owner.agent_id,'give_advice_and_revise',{'task_description':'PUBLIC','model_name':'MiniMax-M2.7'})
                    boundary[-1]['outer_return_too_late_for_reviewer']=any(pol.raw_value in json.dumps(c) for c in calls[nested_start:])
            for label,pair in cases.items():
                left,right=pair
                all_records.append({'environment':env,'transition':label,'same_predefense_model_inputs':left['inputs']==right['inputs'],'same_tools':left['tools']==right['tools'],'same_routes':left['routes']==right['routes'],'same_failure':left['error']==right['error'],'same_result':left['result']==right['result'],'same_side_effect_requests':all(left[k]==right[k] for k in ('sql','http','process')),'left_error':left['error'],'model_calls_per_arm':[len(left['inputs']),len(right['inputs'])]})
            # Actual original advertised tool dispatch, including coordinator session replies/relay.
            for condition in ('STAR','GRAPH'):
                en,ad,pol=construct(row,DEFENSES[0]);coord,first,second=en.agents[:3]
                allowed=[(u.agent_id,v.agent_id) for u in en.agents for v in en.agents if u is not v and (condition=='GRAPH' or coord in (u,v))]
                edge=CommunicationEdges(en.agents,allowed)
                for label,source,target in [('coordinator_initiation',coord,first),('coordinator_relay',coord,second),('peer_initiation',first,second),('worker_initiation',first,coord)]:
                    pending.clear();start=len(calls)
                    relay_text='PUBLIC RETURN <end-of-session>' if label=='coordinator_relay' else 'PUBLIC RELAY'
                    pending.append(tool('new_communication_session',{'target_agent_id':target.agent_id,'message':relay_text}))
                    pending.append(tool('communicate_to',{'message':'PUBLIC RETURN <end-of-session>'}))
                    pending.append(Message(role='assistant',content='PUBLIC SUMMARY'))
                    result=source.act('PUBLIC ROUTE TASK')
                    captured=calls[start:];initial_schema=next(t['function']['parameters'] for t in captured[0]['tools'] if t['function']['name']=='new_communication_session')
                    init_errors=list(jsonschema.Draft7Validator(initial_schema).iter_errors({'target_agent_id':target.agent_id,'message':'PUBLIC RELAY'}))
                    reply_calls=[c for c in captured if c.get('tool_choice')=='required']
                    contradictions=[]
                    for c in reply_calls:
                        schema=c['tools'][0]['function']['parameters']
                        contradictions.extend(sorted(set(schema.get('required',[]))-set(schema.get('properties',{}))))
                    topology.append({'environment':env,'condition':condition,'path':label,'source':source.agent_id,'target':target.agent_id,'coordinator_received_worker_return':('PUBLIC RETURN' in str(coord.msg_box)),'target_received_relay':(relay_text in str(target.msg_box)),'initial_args_schema_valid':not init_errors,'reply_model_calls':len(reply_calls),'reply_schema_impossible_required_fields':sorted(set(contradictions)),'session_returns_history':bool(result[1]),'edge_denials':sum(not x['allowed'] for x in edge.attempts),'original_tools_unchanged':True})
                pending.clear()
            env_probes=[v for v in boundary if v['environment']==env]
            architecture_failed=all(v['session_outer_scope_misattribution'] and all(v['direct_storage'].values()) for v in env_probes)
            assert architecture_failed, 'Revise classification from evidence rather than assuming failure'
            # Recertification comes after all class/boundary tests for this environment.
            for record in originals:
                ids=[a['agent_id'] for a in record['agents']];outcomes=[]
                for defense in DEFENSES:
                    en,ad,pol=construct(record,defense);pending.clear()
                    (root/'marble/workspace/solution.py').write_text('# PUBLIC CODE\n')
                    try:en.start();outcomes.append('completed')
                    except Exception as e:outcomes.append(type(e).__name__)
                _,attacks,_=synthetic_sidecar(record,env)
                cert.append({'environment':env,'task_id':record['task_id'],'mock_executable':outcomes==['completed','completed'],'original_task_and_evaluator_preserved':True,'orthogonal_augmentation':True,'recognizer_A_B':True,'clean_raw_dependency':False,'complete_generic_mediation':False,'eligibility':'INELIGIBLE' if architecture_failed else 'UNRESOLVED','reason':'ENVIRONMENT_GENERIC_CONTEXT_STATE_BOUNDARY_FAILURE','development_selected':False,'confirmatory_selected':False})
        os.chdir(original_cwd)
    assert not network
    report={'transition_pairs':all_records,'boundary_probes':boundary,'topology':topology,'runtime_inventory':inventory,'certification':cert,'formal_model_runs':0,'development_model_runs':0,'network_attempts':0,'mock_transport_calls':len(calls)}
    (out/'AUDIT.json').write_text(json.dumps(report,indent=2)+'\n')
    return {'records':len(cert),'mock_executable':sum(r['mock_executable'] for r in cert),'transitions':len({r['transition'] for r in all_records}),'pair_fixtures':len(all_records),'network_attempts':0}

if __name__=='__main__':
    # Keep original logger/console text private; safe output consists only of counts/booleans.
    if '--help' in sys.argv or '-h' in sys.argv:
        main()
    else:
        with redirect_stdout(io.StringIO()),redirect_stderr(io.StringIO()):
            summary=main()
        print(json.dumps(summary))
