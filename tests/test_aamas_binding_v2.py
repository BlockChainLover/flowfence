import copy
import hashlib
import json
import subprocess
from pathlib import Path
import pytest
from src.experiments.aamas_binding_v2 import (PARSED, TransportBudget, TransportClient, TransportFailure,
    V2BindingEpisode, V2MiniMaxClient, check_pilot, load_config)
from src.experiments.aamas_binding_semantic import BindingDryClient, matrix_cells
from src.experiments.aamas_llm_agents import ProviderFailure, parse_action
from scripts.run_aamas_binding_v2 import run

CONFIG=Path('configs/experiment/aamas2027/e6_v2_binding_semantic.json')
START='393fbf98e96cf6306aac2904529c13d6598ef71f'

class Fake:
    model='MiniMax-M2.7'
    def __init__(self, values): self.values=iter(values);self.n=0
    def complete_messages(self,*a):
        self.n+=1; v=next(self.values)
        if isinstance(v,Exception): raise v
        return v
    def available(self): return True


def budget():
    rows=[]; waits=[]
    b=TransportBudget(100,lambda kind,row:rows.append((kind,row)),lambda row:None,sleep=waits.append)
    return b,rows,waits


def request(b,c,call='c'): return b.request(c,'','', 'r',call,'planner_agent')


def test_config_hash_and_scientific_equality():
    c,t,p,h=load_config(CONFIG)
    assert len(matrix_cells(c))==108
    assert h[c['task_file']]=='8be76843e8e5c95f40731e45fca93e8cf0108c393942d7d144aadd04ea1b7440'
    assert h[c['prompt_file']]=='82404cd411f34335c7b936c88cd55801be6eeace6c0ec8b7d7c61bf19b7ce5ae'
    old=Path('configs/experiment/aamas2027/e6_binding_semantic.json')
    assert hashlib.sha256(old.read_bytes()).hexdigest()=='703adfb46cc215c3f1a2009b692624a98ba98d229f5a330141bc687aea21ae30'


@pytest.mark.parametrize('kind',['HTTP_429','HTTP_500','HTTP_529','HTTP_503','PROVIDER_TRANSPORT_ERROR'])
def test_retry_only_infrastructure_and_all_attempts_logged(kind):
    b,rows,waits=budget();c=Fake([ProviderFailure(kind),ProviderFailure(kind),{'text':'answer','finish_reason':'stop'}])
    assert request(b,c)['text']=='answer'
    terminal=[r for k,r in rows if r['status']!='started']
    assert waits==[5,15] and b.attempts==3 and b.logical_generations==1
    assert len(terminal)==3 and terminal[2]['retry_of']=='c__transport2'
    assert terminal[0]['error_type']==kind


@pytest.mark.parametrize('kind',['HTTP_401','HTTP_403'])
def test_auth_immediately_stops_all_subsequent(kind):
    b,rows,waits=budget();c=Fake([ProviderFailure(kind)])
    with pytest.raises(ProviderFailure,match=kind): request(b,c)
    with pytest.raises(ProviderFailure,match='NOT_ATTEMPTED'): request(b,c,'d')
    assert b.attempts==1 and c.n==1 and not waits


def test_5xx_limit_and_three_exhausted_logical_stop():
    b,rows,waits=budget();c=Fake([ProviderFailure('HTTP_529') for _ in range(9)])
    for i in range(3):
        with pytest.raises(ProviderFailure,match='HTTP_529'):request(b,c,str(i))
    with pytest.raises(ProviderFailure,match='NOT_ATTEMPTED'):request(b,c,'end')
    assert b.attempts==9 and b.logical_generations==3 and waits==[5,15]*3


def test_success_resets_consecutive_exhaustion():
    b,_,_=budget();c=Fake([ProviderFailure('HTTP_500')]*6+[{'text':'x'}]+[ProviderFailure('HTTP_500')]*6)
    for i in range(5):
        try: request(b,c,str(i))
        except ProviderFailure: pass
    assert b.stop_reason is None and b.infrastructure_failures==2


@pytest.mark.parametrize('kind',['PROVIDER_EMPTY_CHOICES','PROVIDER_RESPONSE_PARSE_ERROR','AGENT_SCHEMA_ERROR','HTTP_400'])
def test_no_retry_response_or_noninfra_failure(kind):
    b,_,waits=budget();c=Fake([ProviderFailure(kind)])
    with pytest.raises(ProviderFailure):request(b,c)
    assert c.n==1 and waits==[]


def test_no_retry_after_partial_response_timeout():
    b,_,waits=budget();c=Fake([TransportFailure('PROVIDER_TRANSPORT_ERROR',response_started=True,http_status=200)])
    with pytest.raises(ProviderFailure):request(b,c)
    assert c.n==1 and not waits


@pytest.mark.parametrize('response',[{'text':'invalid','finish_reason':'length'},
    {'text':'invalid','finish_reason':'stop'},{'text':'{}'},
    {'text':'{"action":"hold","message":"wrong answer"}'}])
def test_returned_model_results_never_retried(response):
    b,_,waits=budget();c=Fake([response]);result=request(b,c)
    try:parse_action(result['text'],'planner_agent')
    except ProviderFailure: pass
    assert c.n==1 and not waits


def episode(client=None,task=0,defense='none',sink=None):
    c,t,p,h=load_config(CONFIG)
    return V2BindingEpisode(t[task],'chain_4','clean',defense,1,c,client or BindingDryClient(),profile=p,sink=sink)


def test_reasoning_vs_parsed_action_and_mediation_order(monkeypatch):
    import src.experiments.aamas_llm_agents as base
    order=[]; original=base.parse_action
    def parsed(*a):order.append('parse');return original(*a)
    monkeypatch.setattr(base,'parse_action',parsed)
    class Think(BindingDryClient):
        def complete_messages(self,*a):
            r=super().complete_messages(*a);r['text']='<think>$4800; 4.8K USD</think>'+r['text'];return r
    def sink(kind,row):
        if kind=='generated_attempts': order.append('full')
        if kind=='parsed_action_attempts': order.append('action')
        if kind=='events' and row['origin']=='agent_generated': order.append('mediate')
    ep=episode(Think(),sink=sink);r=ep.run()
    assert r['success'] and r[PARSED[0]]==r[PARSED[1]]==0
    assert r['pre_mediation_generated_exact_secret_attempts']==3
    assert r['pre_mediation_generated_reconstructable_secret_attempts']==3
    assert order[:4]==['full','parse','action','mediate']


def test_parsed_unsafe_action_counted_without_feedback():
    class Leaky(BindingDryClient):
        def complete_messages(self,*a):
            r=super().complete_messages(*a);action=json.loads(r['text']);action['message']+='; 4.8K USD'
            r['text']=json.dumps(action);return r
    ep=episode(Leaky());r=ep.run()
    assert r[PARSED[1]]==3 and r['delivered_reconstructable_secret_exposure']>0
    from src.experiments.aamas_binding_semantic import BindingEpisode
    c,t,p,h=load_config(CONFIG)
    old=BindingEpisode(t[0],'chain_4','clean','none',1,c,Leaky(),profile=p);before=old.run()
    for k in ('success','delivered_reconstructable_secret_exposure','intervention_count'):
        assert r[k]==before[k]
    assert ep.context_history==old.context_history


def test_parser_failure_has_no_action_diagnostic():
    ep=episode(Fake([{'text':'bad $4800','finish_reason':'length'}]));r=ep.run()
    assert r['status']=='failed' and r[PARSED[0]]==0 and r['pre_mediation_generated_exact_secret_attempts']==1


@pytest.mark.parametrize('task',[0,1,2,3,4,5])
@pytest.mark.parametrize('defense',['none','ifc_safeview','flowfence_lite_nonoracle'])
def test_approve_hold_fairness_no_oracle(task,defense):
    ep=episode(task=task,defense=defense);r=ep.run()
    assert r['success'] and len(ep.parsed_generated)==3
    assert not any(e['oracle_annotation_used'] for e in ep.audit)
    if task>=4:
        assert r['finance_correctly_holds'] and r['writer_correctly_holds']
        assert r['external_tool_executions']==0 and not r['final_sent']


def test_matrix_safe_exclusive_and_pilot_gate(tmp_path):
    c,t,p,h=load_config(CONFIG);out=tmp_path/'dry'
    assert run(c,t,p,h,out,dry_run=True)['completed']==108
    assert not (out/'transport_attempts.jsonl').exists()
    from src.defenses.mas_flowfence import contains_raw_secret
    from src.runtime.policy import default_secret_policies
    assert all(not contains_raw_secret(f.read_text(),default_secret_policies()) for f in out.glob('*.json*'))
    with pytest.raises(FileExistsError):run(c,t,p,h,out,dry_run=True)
    pc,pt,pp,ph=load_config(Path('configs/experiment/aamas2027/e6_v2_pilot.json'))
    po=tmp_path/'pilot';run(pc,pt,pp,ph,po,dry_run=True)
    with pytest.raises(ValueError,match='PILOT_GATE_FAILED'):check_pilot(po,pc)
    reg=json.loads((po/'registration.json').read_text());reg['dry_run']=False
    (po/'registration.json').write_text(json.dumps(reg))
    calls=[json.loads(l) for l in (po/"call_attempts.jsonl").read_text().splitlines()]
    for call in calls: call.update(provider_request=True,model_version="MiniMax-M2.7")
    (po/"call_attempts.jsonl").write_text("\n".join(map(json.dumps,calls)))
    assert check_pilot(po,pc)
    rows=[json.loads(l) for l in (po/'episodes.jsonl').read_text().splitlines()]
    rows[0]['status']='failed';(po/'episodes.jsonl').write_text('\n'.join(map(json.dumps,rows)))
    with pytest.raises(ValueError,match='PILOT_GATE_FAILED'):check_pilot(po,pc)
    with pytest.raises(ValueError,match='requires --pilot'):run(c,t,p,h,tmp_path/'formal')


def test_historical_bytes_and_scientific_sources_preserved():
    paths=['src/defenses/mas_flowfence.py','src/runtime/policy.py','src/experiments/aamas_binding_semantic.py',
           'src/experiments/aamas_llm_agents.py','src/experiments/aamas_stress.py',
           'src/experiments/aamas_metrics.py','artifacts/aamas2027/E6_binding_semantic',
           'artifacts/aamas2027/E3_representation_stress']
    paths += subprocess.check_output(['git','ls-tree','-r','--name-only',START,'artifacts/aamas2027'],text=True).splitlines()
    paths=list(dict.fromkeys(paths))
    assert not subprocess.check_output(['git','diff',START,'--',*paths],text=True)


def test_http_adapter_payload_unchanged_and_response_timeout_not_retryable(monkeypatch):
    import urllib.request
    requests=[]
    class Response:
        status=200
        def __enter__(self):return self
        def __exit__(self,*a):pass
        def read(self):raise TimeoutError()
    def opening(req,timeout):
        requests.append((json.loads(req.data),timeout));return Response()
    monkeypatch.setattr(urllib.request,'urlopen',opening)
    c=V2MiniMaxClient(model='MiniMax-M2.7',temperature=0,max_tokens=4096,timeout_seconds=180,
        provider_settings={'openai_api_key':'test-placeholder','openai_base_url':'https://example.invalid'})
    b,_,waits=budget()
    with pytest.raises(TransportFailure) as exc:request(b,c)
    assert exc.value.response_started and len(requests)==1 and waits==[]
    assert requests[0]==({'model':'MiniMax-M2.7','messages':[{'role':'system','content':''},{'role':'user','content':''}], 'temperature':0,'max_tokens':4096},180)


def test_global_stop_during_retry_keeps_first_actual_attempt_marked_sent():
    b,_,_=budget()
    def stop(_):b.stop_reason='HTTP_403'
    b.sleep=stop
    c=TransportClient(Fake([ProviderFailure('HTTP_529')]),b)
    ep=episode(c);r=ep.run()
    assert r['status']=='failed' and ep.calls[0]['provider_request']
    assert b.attempts==1


def test_http_5xx_with_model_text_is_never_retried(monkeypatch):
    import io
    import urllib.error
    import urllib.request
    def opening(*a,**kw):
        raise urllib.error.HTTPError('https://example.invalid',529,'busy',{},io.BytesIO(json.dumps({'choices':[{'message':{'content':'model answer'}}]}).encode()))
    monkeypatch.setattr(urllib.request,'urlopen',opening)
    c=V2MiniMaxClient(model='MiniMax-M2.7',provider_settings={'openai_api_key':'placeholder','openai_base_url':'https://example.invalid'})
    b,rows,waits=budget()
    with pytest.raises(TransportFailure):request(b,c)
    assert b.attempts==1 and not waits and rows[-1][1]['response_started']


def test_summary_scientific_pairs_exclude_incomplete_task_ties(tmp_path):
    from scripts.summarize_aamas_binding_v2 import summarize
    c,t,p,h=load_config(CONFIG)
    c.update(task_ids=['e6_b05'],topologies=['chain_4'],conditions=['clean'])
    out=tmp_path/'run';run(c,t,p,h,out,dry_run=True)
    rows=[json.loads(l) for l in (out/'episodes.jsonl').read_text().splitlines()]
    for r in rows:
        if r['defense']!='none':r.update(status='failed',success=False,privacy_safe_success=False,error_type='AGENT_JSON_PARSE_ERROR')
    (out/'episodes.jsonl').write_text('\n'.join(map(json.dumps,rows)))
    result=summarize(out,tmp_path/'summary')
    op=next(o for o in result['operational_paired'] if o['topology']==o['condition']=='overall')
    assert op['neither_completed']==op['unavailable_privacy_comparison']==1
    pair=next(x for x in result['paired'] if x['topology']==x['condition']=='overall' and x['metric']=='success')
    assert pair['available']==pair['tie']==0
    assert not result['formal_evidence_complete']
    rows[0][PARSED[0]]+=1
    (out/'episodes.jsonl').write_text('\n'.join(map(json.dumps,rows)))
    with pytest.raises(AssertionError):summarize(out,tmp_path/'tampered')
