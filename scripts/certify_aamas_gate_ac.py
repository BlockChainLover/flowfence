#!/usr/bin/env python3
"""Certify Gate A-C with real benchmark imports and deterministic external doubles.

No provider request is allowed. Mock construction does not certify live services.
"""
import argparse
from contextlib import ExitStack,redirect_stdout,redirect_stderr
from copy import deepcopy
import io
import json
import logging
import os
from pathlib import Path
import runpy
import socket
import sys
import tempfile
import traceback
from types import SimpleNamespace
from unittest.mock import patch


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--benchmark',required=True,type=Path)
    parser.add_argument('--gate-ad', action='store_true', help='Exercise recovered scheduler for every task and scoped Coding write hook')
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args(); b=args.benchmark.resolve(); out=args.output.resolve(); out.mkdir(parents=True,exist_ok=True)
    os.environ.update(LITELLM_LOCAL_MODEL_COST_MAP='True',HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',PYTHONDONTWRITEBYTECODE='1',JOBLIB_MULTIPROCESSING='0',PYTHONPATH=str(Path(__file__).resolve().parents[1]))
    network=[]
    def deny(*a,**k):network.append('blocked');raise RuntimeError('offline certification forbids network')
    socket.socket.connect=deny;socket.create_connection=deny
    sys.path.insert(0,str(b))
    import litellm
    # A provider callable omitted from a test double must fail closed.
    def forbidden(*a,**k):raise RuntimeError('unmocked model generation forbidden')
    litellm.completion=forbidden;litellm.acompletion=forbidden
    from marble.engine.engine import Engine
    from marble.configs.config import Config
    from marble.environments import ResearchEnvironment,DBEnvironment,CodingEnvironment
    from marble.evaluator.evaluator import Evaluator
    from src.experiments.aamas_gate_ac import MarbleBoundaryAdapter,synthetic_sidecar,DEFENSES
    from tests.test_aamas_gate_ac import exercise_trajectories
    if args.gate_ad:
        from src.experiments.aamas_gate_ad import RecoveredMarbleAdapter
        MarbleBoundaryAdapter = RecoveredMarbleAdapter
    import yaml
    import jsonschema
    logging.disable(logging.CRITICAL)
    repo=Path(__file__).resolve().parents[1]
    schema=json.loads((repo/'experiments/aamas2027_external/PUBLIC_TASK_ELIGIBILITY_SCHEMA.json').read_text())
    predicate=json.loads((repo/'experiments/aamas2027_external/PUBLIC_TASK_ELIGIBILITY_PREDICATE.json').read_text())
    criteria_ids=[x['id'] for x in predicate['criteria']]
    counters={'mock_generations':0,'mock_sql_statements':0,'mock_subprocesses':0,'mock_http':0}
    model_inputs=[]
    response_override=[None]
    def fake_model(*a,**kw):
        counters['mock_generations']+=1
        model_inputs.append(deepcopy({'args':a,'kwargs':kw}))
        prompt=json.dumps(kw.get('messages',[]))
        content='STATIC PUBLIC FIXTURE'
        if 'innovation' in prompt:content='{"innovation":4,"safety":3,"feasibility":2}'
        if 'instruction_following' in prompt:content='{"instruction_following":4,"executability":3,"consistency":2,"quality":1}'
        if response_override[0] is not None:content=response_override[0]
        return [SimpleNamespace(content=content,tool_calls=None)]
    class Cursor:
        def execute(self,*a,**k):counters['mock_sql_statements']+=1
        def fetchall(self):return []
        def close(self):pass
    class Connection:
        def cursor(self,*a,**k):return Cursor()
        def close(self):pass
    def fake_process(*a,**k):counters['mock_subprocesses']+=1;return SimpleNamespace(returncode=0)
    def fake_http(*a,**k):
        counters['mock_http']+=1
        return SimpleNamespace(status_code=200,json=lambda:{'status':'success','data':{'alerts':[],'result':[{'values':[[1,'1'],[2,'1'],[3,'1']]}]}})
    records=[];pairs=[];bypasses=[];constructor_failures=[];scheduler_checks=[];topology_checks=[];coding_clean_checks=[]
    original_cwd=Path.cwd()
    with tempfile.TemporaryDirectory(prefix='gate-ac-init-') as temp, ExitStack() as stack:
        root=Path(temp);os.chdir(root)
        (root/'logs').mkdir();(root/'evaluator').symlink_to(b/'marble/evaluator',target_is_directory=True)
        (root/'marble/configs/coding_config').mkdir(parents=True);(root/'marble/workspace').mkdir()
        if (root/'MARBLE').exists():  # case-insensitive macOS volume
            (root/'marble/marble').symlink_to(root/'marble',target_is_directory=True)
        else:
            (root/'MARBLE').symlink_to(root,target_is_directory=True)
        for mod in ['marble.agent.base_agent','marble.evaluator.evaluator','marble.engine.engine_planner','marble.environments.coding_utils.coder','marble.environments.coding_utils.reviewer']:
            stack.enter_context(patch(mod+'.model_prompting',fake_model))
        stack.enter_context(patch('marble.agent.base_agent.token_counter',lambda *a,**k:0))
        stack.enter_context(patch('marble.engine.engine_planner.token_counter',lambda *a,**k:0))
        stack.enter_context(patch('subprocess.run',fake_process))
        stack.enter_context(patch('psycopg2.connect',lambda *a,**k:Connection()))
        stack.enter_context(patch('requests.get',fake_http))
        for environment in ['research','database','coding']:
            source=b/f'multiagentbench/{environment}/{environment}_main.jsonl'
            for order,line in enumerate(source.read_text().splitlines(),1):
                if not line.strip():continue
                row=json.loads(line);policy,attacks,fact_type=synthetic_sidecar(row,environment)
                data=deepcopy(row)
                data['coordinate_mode']='star';data['llm']='MiniMax-M2.7'
                data['environment'].update(type={'research':'Research','database':'DB','coding':'Coding'}[environment],max_iterations=data['environment'].get('max_iterations') or 5)
                if environment=='coding':data['environment']['workspace_dir']='marble/workspace'
                data['memory']={'type':'BaseMemory'};data['metrics']['evaluate_llm']='gpt-4o'
                data['output']={'format':'jsonl','file_path':'fixture_output.jsonl'}
                # Staging the exact original task into the official fixed path is initialization, not evaluator repair.
                (root/'marble/configs/coding_config/coding_config.yaml').write_text(yaml.safe_dump(data))
                row_checks=[];snapshots=[];contexts=[];errors=[];adapters=[]
                for defense in DEFENSES:
                    try:
                        with redirect_stdout(io.StringIO()),redirect_stderr(io.StringIO()):
                            engine=Engine(Config(deepcopy(data)))
                        adapter=MarbleBoundaryAdapter(engine,defense,[policy]);adapters.append(adapter)
                        snapshots.append(adapter.capability_snapshot())
                        owner=engine.agents[0]
                        owner.memory.update(owner.agent_id,{'private_sidecar':policy.raw_value})
                        start=len(model_inputs)
                        owner.act('STATIC PUBLIC INTEGRATION TASK')
                        contexts.append(model_inputs[start:])
                        if len(engine.agents)>1:
                            owner.send_message('fixture-session',engine.agents[1],attacks['A'])
                        # Exercise original memory/planner interface and safe final serializer.
                        engine.planner.update_progress('STATIC PUBLIC PROGRESS')
                        with redirect_stdout(io.StringIO()):
                            engine._write_to_jsonl({'fixture':'public'})
                        with patch('marble.agent.base_agent.model_prompting',side_effect=ValueError('fixture failure')):
                            try:owner.act('STATIC FAILURE TEST')
                            except Exception as e:errors.append(type(e).__name__)
                        row_checks.append(True)
                    except Exception as e:
                        row_checks.append(False);constructor_failures.append(dict(environment=environment,task_id=row['task_id'],defense=defense,error=type(e).__name__,detail=str(e)[:250]))
                parity=len(snapshots)==2 and snapshots[0]==snapshots[1] and contexts[0]==contexts[1] and errors==['ValueError','ValueError']
                pairs.append(dict(environment=environment,task_id=row['task_id'],capability_snapshot_equal=len(snapshots)==2 and snapshots[0]==snapshots[1],clean_model_context_equal=len(contexts)==2 and contexts[0]==contexts[1],failure_handling_equal=errors==['ValueError','ValueError'],pass_=parity))
                evaluator_ok=False;coding_bypass=False;scheduler_ok=None;planning_failure=None
                if adapters and all(row_checks):
                    engine=adapters[0].engine
                    with redirect_stdout(io.StringIO()),redirect_stderr(io.StringIO()):
                        if environment=='research':
                            engine.evaluator.evaluate_task_research(engine.task,'STATIC PUBLIC FIXTURE');evaluator_ok=bool(engine.evaluator.metrics['task_evaluation'])
                        elif environment=='database':
                            engine.evaluator.evaluate_task_db(engine.task,'STATIC PUBLIC FIXTURE',data['task']['labels'],data['task']['number_of_labels_pred'],data['task']['root_causes'])
                            evaluator_ok=bool(engine.evaluator.metrics['task_evaluation'])
                        else:
                            solution=root/'marble/workspace/solution.py';solution.write_text('# STATIC PUBLIC FIXTURE\n')
                            engine.evaluator.evaluate_code_quality(engine.task,'STATIC PUBLIC FIXTURE');evaluator_ok=bool(engine.evaluator.metrics['code_quality'])
                            # Prove a genuine internal write bypass under both defense arms, not by calling release directly.
                            for adapter in adapters:
                                solution.unlink(missing_ok=True)
                                response_override[0]='# '+policy.raw_value+'\n'
                                adapter.engine.environment.apply_action(adapter.engine.agents[0].agent_id,'create_solution',{'task_description':'public fixture','model_name':'MOCK_ONLY'})
                                leaked=solution.exists() and policy.raw_value in solution.read_text()
                                coding_bypass=coding_bypass or leaked
                                bypasses.append(dict(environment=environment,task_id=row['task_id'],defense=adapter.defense,surface='nested_coding_workspace_write',raw_written_before_outer_return=leaked))
                                if args.gate_ad:
                                    from marble.environments.coding_utils import coder
                                    response_override[0]='# STATIC PUBLIC CODE\n'
                                    direct=coder.create_solution_handler(adapter.engine.environment,'public fixture','MOCK_ONLY')
                                    clean_bytes=solution.read_bytes()
                                    wrapped=adapter.engine.environment.apply_action(adapter.engine.agents[0].agent_id,'create_solution',{'task_description':'public fixture','model_name':'MOCK_ONLY'})
                                    coding_clean_checks.append(dict(task_id=row['task_id'],defense=adapter.defense,same_bytes=solution.read_bytes()==clean_bytes,same_return=direct==wrapped))
                                response_override[0]=None
                    try:
                        engine.evaluator.evaluate_planning('STATIC','STATIC','STATIC','STATIC')
                        if args.gate_ad:
                            engine.evaluator.evaluate_communication('STATIC','STATIC')
                    except Exception as exc:
                        planning_failure=type(exc).__name__+': '+str(exc)
                    # Real STAR scheduler: representative tasks by default, all tasks in Gate A-D.
                    if order==1 or args.gate_ad:
                        scheduler_modes=[];scheduler_contexts=[]
                        for adapter in adapters:
                            en=adapter.engine
                            if environment=='coding':
                                (root/'marble/workspace/solution.py').write_text('# STATIC PUBLIC FIXTURE\n')
                            scheduler_start=len(model_inputs)
                            with patch.object(en.planner,'assign_tasks',return_value={'tasks':{x.agent_id:'PUBLIC SCHEDULE FIXTURE' for x in en.agents}}),patch.object(en.planner,'decide_next_step',return_value=False),redirect_stdout(io.StringIO()),redirect_stderr(io.StringIO()):
                                try:en.start();scheduler_modes.append('completed')
                                except Exception as e:
                                    scheduler_modes.append(type(e).__name__+': '+str(e))
                                    if order==1:
                                        (out/f'{environment}_{adapter.defense}_STACK.txt').write_text(traceback.format_exc())
                                scheduler_contexts.append(model_inputs[scheduler_start:])
                        scheduler_ok=scheduler_modes==['completed','completed']
                        scheduler_checks.append(dict(environment=environment,task_id=row['task_id'],outcomes=scheduler_modes,equal=scheduler_modes[0]==scheduler_modes[1],successful=scheduler_ok,model_contexts_equal=scheduler_contexts[0]==scheduler_contexts[1]))
                if args.gate_ad and order==1:
                    from src.experiments.aamas_gate_ad import CommunicationEdges
                    topology_cases=[]
                    for topology_name in ('STAR','GRAPH'):
                        with redirect_stdout(io.StringIO()),redirect_stderr(io.StringIO()):
                            ten=Engine(Config(deepcopy(data)))
                        ta=MarbleBoundaryAdapter(ten,DEFENSES[0],[policy])
                        ids=[a.agent_id for a in ten.agents];coordinator=ids[0]
                        allowed=[(a,z) for a in ids for z in ids if a!=z and (topology_name=='GRAPH' or coordinator in (a,z))]
                        edges=CommunicationEdges(ten.agents,allowed)
                        before=len(model_inputs)
                        for agent in ten.agents:agent.act('IDENTICAL PUBLIC TOPOLOGY TASK')
                        model_context=deepcopy(model_inputs[before:])
                        attempts=[]
                        for source in ten.agents:
                            for target in ten.agents:
                                if source is target:continue
                                before_box=deepcopy(target.msg_box)
                                try:source.send_message('edge-fixture',target,'PUBLIC EDGE FIXTURE');delivered=True
                                except PermissionError:delivered=False
                                assert delivered==((source.agent_id,target.agent_id) in allowed)
                                if not delivered:assert before_box==target.msg_box
                                attempts.append(delivered)
                                # Direct receive cannot bypass the same edge policy.
                                try:target.receive_message('direct-fixture',source,'PUBLIC EDGE FIXTURE');direct=True
                                except PermissionError:direct=False
                                assert direct==delivered
                        topology_cases.append(dict(condition=topology_name,capabilities=ta.capability_snapshot(),contexts=model_context,attempts=attempts,allowed=allowed))
                    topology_checks.append(dict(environment=environment,agents=len(ids),same_capabilities=topology_cases[0]['capabilities']==topology_cases[1]['capabilities'],same_model_contexts=topology_cases[0]['contexts']==topology_cases[1]['contexts'],star_deliveries=sum(topology_cases[0]['attempts']),graph_deliveries=sum(topology_cases[1]['attempts']),direct_receive_enforced=True,matrices={x['condition']:x['allowed'] for x in topology_cases}))
                c={k:True for k in criteria_ids}
                c['official_initialization']=True if all(row_checks) and environment!='database' else None
                c['original_evaluator_invocable']=False if planning_failure else (True if evaluator_ok else None)
                c['full_capability_parity']=None  # Full dynamic/nested capability coverage remains unverified.
                # Coverage is never inferred from equal API inputs or partial wrappers.
                c['complete_mediation']=False if coding_bypass else None
                c['original_utility_preserved']=True if evaluator_ok and environment!='database' else None
                reasons=[]
                if planning_failure:reasons.append('OFFICIAL_STAR_PLANNING_PROMPT_FORMAT_FAILURE')
                if coding_bypass:reasons.append('NESTED_CODING_WRITE_BYPASSES_CURRENT_ADAPTER')
                else:reasons.append('COMPLETE_RELEASE_COVERAGE_UNRESOLVED')
                if environment=='database':reasons+=['LIVE_DB_INFRASTRUCTURE_NOT_CERTIFIED','ORIGINAL_BATCH_JUDGE_PROVIDER_SCOPE_UNRESOLVED']
                if not all(row_checks):reasons.append('INITIALIZATION_FAILED')
                if not evaluator_ok:reasons.append('EVALUATOR_INVOCATION_UNRESOLVED')
                if not parity:reasons.append('PARITY_UNRESOLVED')
                status='INELIGIBLE' if False in c.values() else ('UNRESOLVED' if None in c.values() else 'ELIGIBLE')
                result=dict(task_id=row['task_id'],environment=environment,source_commit='8d60fa17b5596b44458a52d4296061b9fc13d6f2',official_order=order,evaluator_available=evaluator_ok,planning_evaluator_error=planning_failure,evaluator_mode='official STAR + original evaluator with deterministic judge double',initialization_status='REAL_CONSTRUCTOR_EXTERNAL_DOUBLES' if all(row_checks) else 'FAILED',augmentation_feasible=True,protected_fact_type_candidate=fact_type,authorized_principal_candidate=policy.owner_principal,forbidden_principal_or_surface_candidate=['shared_doc','public/final_output'],clean_raw_disclosure_dependency='NO',contamination_surface_candidate='shared_doc',A_recognizer_match=True,B_recognizer_match=True,A_raw_absent=True,B_raw_absent=True,mediation_surfaces_identified=['context','messages','memory','planner','tools','workspace','final','debug'],IFC_parity_feasible=parity,criteria=c,eligibility=status,exclusion_reason_code=reasons,development_candidate=False,confirmatory_candidate=False)
                jsonschema.validate(result,schema);records.append(result)
        # Exercise the unmodified standalone Database scorer with a static non-study fixture.
        fixture=root/'batch_fixture';(fixture/'group').mkdir(parents=True)
        (fixture/'group/result.json').write_text(json.dumps({'planning_scores':[1],'communication_scores':[1],'task_evaluation':{'root_cause':['STATIC_ROOT'],'predicted':'STATIC TEXT'}}))
        os.chdir(fixture)
        with patch('litellm.completion',return_value=SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content='STATIC_ROOT\nSTATIC_OTHER'))])),patch('litellm.utils.trim_messages',side_effect=lambda messages,**kw:messages),patch('time.sleep',return_value=None),redirect_stdout(io.StringIO()),redirect_stderr(io.StringIO()):
            runpy.run_path(str(b/'scripts/database/batch_eval.py'),run_name='gate_ac_fixture')
        os.chdir(original_cwd)
    assert not network,network
    trajectories=exercise_trajectories()
    counts={e:{s:sum(x['environment']==e and x['eligibility']==s for x in records) for s in ['ELIGIBLE','INELIGIBLE','UNRESOLVED']} for e in ['research','database','coding']}
    report=dict(imports='PASS',python=sys.version,record_count=len(records),counts=counts,constructor_failures=constructor_failures,parity_pairs=pairs,scheduler_checks=scheduler_checks,topology_checks=topology_checks,coding_clean_checks=coding_clean_checks,coding_bypasses=bypasses,network_attempts=len(network),counters=counters,original_database_batch_fixture='PASS',formal_model_runs=0,development_model_runs=0,scientific_outcomes_produced=False)
    (out/'CERTIFICATION.json').write_text(json.dumps(records,indent=2)+'\n')
    (out/'INTEGRATION_AUDIT.json').write_text(json.dumps(report,indent=2)+'\n')
    if not args.gate_ad:
        (out/'E3_MOCK_TRAJECTORIES.json').write_text(json.dumps(trajectories,indent=2)+'\n')
    print(json.dumps({'records':len(records),'counts':counts,'constructor_failures':len(constructor_failures),'parity_pass':sum(x['pass_'] for x in pairs),'scheduler':scheduler_checks,'network_attempts':len(network)}))

if __name__=='__main__':main()
