import copy
import hashlib
import json
import subprocess
from datetime import datetime
from pathlib import Path
import pytest
from src.experiments.aamas_binding_r3 import (R3BindingEpisode, load_config, schedule, run_id,
    episode_metrics, frozen_assertions, CONDITIONS, DEFENSES)
from src.experiments.aamas_binding_r2 import R2BindingEpisode
from src.experiments.aamas_binding_semantic import BindingDryClient
from src.experiments.aamas_binding_v2 import TransportBudget, TransportClient
from src.defenses.mas_flowfence import contains_raw_secret, contains_sensitive_detail_request
from src.runtime.policy import default_secret_policies
from scripts.run_aamas_binding_r3 import run
from scripts.summarize_aamas_binding_r3 import summarize, comparisons

CONFIG=Path('configs/experiment/aamas2027/r3_formal.json')
START='89fbb3e68655d82877b73c7cd5837b3019b64215'


def read(path):return [json.loads(l) for l in path.read_text().splitlines() if l]


def test_frozen_files_match_start_including_detectors_ifc_registry_evaluator_tasks_prompts():
    f=frozen_assertions()
    for path,digest in f['files'].items():
        original=subprocess.check_output(['git','show',START+':'+path])
        assert hashlib.sha256(original).hexdigest()==digest
        assert Path(path).read_bytes()==original
    p=json.loads(Path('configs/experiment/aamas2027/e6_prompt_profile.json').read_text())
    for key,value in {'system_prompt':p['system_prompt'],**p['role_instructions']}.items():
        assert hashlib.sha256(value.encode()).hexdigest()==f['prompt_components'][key]


@pytest.mark.parametrize('condition,phrase',[(CONDITIONS[1],'private numeric limit'),(CONDITIONS[2],'private finance values')])
def test_exact_user_attacks_match_pre_r2_detector_but_not_prior_wording(condition,phrase):
    c,t,p,h=load_config(CONFIG);attack=p['attacks'][condition]
    assert phrase in attack and not contains_raw_secret(attack,default_secret_policies())
    assert contains_sensitive_detail_request(attack)
    for ref in ('393fbf98e96cf6306aac2904529c13d6598ef71f','5a900505548a1315c40c7ba3f6529c08829079d3',START):
        old=json.loads(subprocess.check_output(['git','show',ref+':configs/experiment/aamas2027/e6_prompt_profile.json'],text=True))
        assert all(attack!=a and ' '.join(attack.split())!=' '.join(a.split()) and phrase not in a for a in old['attacks'].values())
    pre=subprocess.check_output(['git','show','393fbf98e96cf6306aac2904529c13d6598ef71f:src/defenses/mas_flowfence.py'],text=True)
    assert phrase in pre and pre==Path('src/defenses/mas_flowfence.py').read_text()


def test_schedule_unique_108_no_seed_and_alternating_adjacent_pairs():
    c,t,p,h=load_config(CONFIG);pairs=schedule(c)
    assert len(pairs)==54 and len({run_id(cell) for pair in pairs for cell in pair})==108
    assert pairs==json.loads(Path('artifacts/aamas2027/R3_SCHEDULE.json').read_text())
    for i,pair in enumerate(pairs):
        assert [x['defense'] for x in pair]==list(DEFENSES)[::1 if i%2==0 else -1]
        assert pair[0]['replicate_id']==pair[1]['replicate_id']
        assert pair[0]['task_id']==pair[1]['task_id'] and pair[0]['condition']==pair[1]['condition']
        assert all('seed' not in x and x['replicate_id'] in (1,2,3) for x in pair)


@pytest.mark.parametrize('task',range(6))
@pytest.mark.parametrize('defense',DEFENSES)
def test_r3_inherits_unchanged_paths_no_oracle_and_clean_inputs(task,defense):
    c,t,p,h=load_config(CONFIG)
    a=R3BindingEpisode(t[task],'blackboard_4','clean',defense,3,c,BindingDryClient(),profile=p)
    b=R2BindingEpisode(t[task],'blackboard_4','clean',defense,1,c,BindingDryClient(),profile=p)
    ar=a.run();br=b.run()
    assert ar['success']==br['success']==True and a.context_history==b.context_history
    assert ar['replicate_id']==3 and 'seed' not in ar and '__replicate3__' in ar['run_id']
    assert not any(e['oracle_annotation_used'] for e in a.audit)
    for method in ('_workflow','_mediate','_prompt','_source','correctness','_generate','extra_event_metrics'):
        assert getattr(R3BindingEpisode,method) is getattr(R2BindingEpisode,method)


def test_episode_vs_propagation_counts_and_failed_privacy_unknown():
    es=[{'delivered_reconstructable_secret_exposure':1,'recipient_id':r} for r in (None,'external_vendor_agent','doc_writer_agent')]
    x=episode_metrics('completed',es)
    assert x['episode_reconstructable_disclosure']==1 and x['propagation_event_count']==3
    assert x['external_recipient_reconstructable_observations']==1
    assert episode_metrics('completed',[])['episode_reconstructable_disclosure']==0
    assert episode_metrics('failed',[])['episode_reconstructable_disclosure'] is None
    assert episode_metrics('failed',es)['partial_reconstructable_disclosure_observed']==1


@pytest.fixture(scope='module')
def dry(tmp_path_factory):
    folder=tmp_path_factory.mktemp('r3')/'formal';c,t,p,h=load_config(CONFIG)
    completion=run(c,t,p,h,folder,dry_run=True,source_sha=START)
    assert completion['completed']==108 and completion['provider_requests']==0
    return folder,c


def test_actual_pair_batches_wait_for_both_terminals_and_safe_complete_matrix(dry):
    folder,c=dry;rows=read(folder/'episodes.jsonl');log=read(folder/'schedule.jsonl')
    assert len(rows)==108 and len(log)==108 and not (folder/'transport_attempts.jsonl').exists()
    assert len({r['run_id'] for r in rows})==108
    for i in range(54):
        first,end=log[i*2:i*2+2]
        assert first['pair_index']==end['pair_index']==i
        assert first['status']=='dispatched' and end['status']=='terminal'
        for row in rows:
            if row['pair_index']==i:
                assert first['timestamp']<=row['timestamp']<=row['completed_at']<=end['timestamp']
        if i<53:assert end['timestamp']<=log[i*2+2]['timestamp']
    from scripts.package_aamas2027 import validate_safe_artifacts
    validate_safe_artifacts(list(folder.glob('*')),folder)


def test_summary_rebuild_and_dry_not_confirmatory(dry,tmp_path):
    folder,c=dry;r=summarize(folder,tmp_path/'derived')
    assert r['complete_pairs']==dict.fromkeys(CONDITIONS,18)
    assert not r['decisions']['R3_CONFIRMATORY_EVIDENCE_COMPLETE']
    assert r['completed']==108


@pytest.mark.parametrize('response',[{'text':'broken','finish_reason':'length'}, {'text':'{}','finish_reason':'stop'}])
def test_r3_model_output_failure_preserved_without_transport_retry(response):
    class Bad:
        model='MiniMax-M2.7'
        def __init__(self):self.n=0
        def available(self):return True
        def complete_messages(self,*a):self.n+=1;return response
    c,t,p,h=load_config(CONFIG);calls=[];waits=[];bad=Bad()
    budget=TransportBudget(9,lambda k,r:calls.append(r),lambda r:None,sleep=waits.append)
    ep=R3BindingEpisode(t[0],'blackboard_4',CONDITIONS[1],DEFENSES[0],1,c,TransportClient(bad,budget),profile=p)
    r=ep.run();assert r['status']=='failed' and r['episode_reconstructable_disclosure'] is None
    assert r['attempt']==1 and r['retry_of'] is None and bad.n==1 and not waits


def modified(dry):
    folder,c=dry;return copy.deepcopy(read(folder/'episodes.jsonl')),c


def test_decision_case_a_and_case_b_preserve_utility_boundary(dry):
    rows,c=modified(dry)
    for r in rows:
        if r['defense']==DEFENSES[0] and r['condition']!='clean':r['episode_reconstructable_disclosure']=1;r['privacy_safe_success']=False
    assert comparisons(rows,c)[-1]['PAPC_R2_CONFIRMATORY_ADVANTAGE']
    next(r for r in rows if r['defense']==DEFENSES[1] and r['condition']==CONDITIONS[1])['success']=False
    d=comparisons(rows,c)[-1];assert d['case']=='B' and d['PRIVACY_UTILITY_TRADEOFF'] and not d['PAPC_R2_CONFIRMATORY_ADVANTAGE']


def test_decision_clean_regression_cannot_support_advantage(dry):
    rows,c=modified(dry)
    for r in rows:
        if r['defense']==DEFENSES[0] and r['condition']!='clean':r['episode_reconstructable_disclosure']=1
    next(r for r in rows if r['defense']==DEFENSES[1] and r['condition']=='clean')['success']=False
    d=comparisons(rows,c)[-1];assert not d['CLEAN_UTILITY_PRESERVED'] and not d['PAPC_R2_CONFIRMATORY_ADVANTAGE']


def test_cases_c_d_e_and_coverage_without_failed_ties(dry):
    rows,c=modified(dry);assert comparisons(rows,c)[-1]['case']=='D'
    chosen=next(r for r in rows if r['defense']==DEFENSES[0] and r['condition']==CONDITIONS[1]);chosen['episode_reconstructable_disclosure']=1
    assert comparisons(rows,c)[-1]['case']=='C'
    chosen['episode_reconstructable_disclosure']=0
    next(r for r in rows if r['defense']==DEFENSES[1] and r['condition']==CONDITIONS[1])['episode_reconstructable_disclosure']=1
    assert comparisons(rows,c)[-1]['case']=='E'
    failed=[r for r in rows if r['defense']==DEFENSES[0] and r['condition']==CONDITIONS[2]][:4]
    for r in failed:r.update(status='failed',error_type='AGENT_JSON_PARSE_ERROR',success=False,episode_reconstructable_disclosure=None,privacy_safe_success=False)
    cs,ts,ps,cl,d=comparisons(rows,c)
    assert d['coverage'][CONDITIONS[2]]==14 and not d['R3_CONFIRMATORY_EVIDENCE_COMPLETE']
    assert all(p['disclosure_difference'] is None and p['matched_task_difference'] is None for p in ps if not p['both_completed'])
    assert next(r for r in cs if r['condition']==CONDITIONS[2] and r['defense']==DEFENSES[0])['privacy_unknown']==4


def test_old_artifacts_preserved():
    paths=subprocess.check_output(['git','ls-tree','-r','--name-only',START,'artifacts/aamas2027'],text=True).splitlines()
    assert not subprocess.check_output(['git','diff',START,'--',*paths],text=True)


def test_coverage_boundary_15_pairs_and_exact_fraction_tie(dry):
    rows,c=modified(dry)
    # Three unavailable IFC replicates leave15 pairs, which is allowed, not a
    # new requirement to complete every task. Unknown remains explicit.
    missing=[r for r in rows if r['condition']==CONDITIONS[1] and r['defense']==DEFENSES[0]][:3]
    for r in missing:r.update(status='failed',error_type='AGENT_JSON_PARSE_ERROR',success=False,episode_reconstructable_disclosure=None,privacy_safe_success=False)
    assert comparisons(rows,c)[-1]['R3_CONFIRMATORY_EVIDENCE_COMPLETE']
    # Cluster effects1/3+2/3-1 must be exactly a tie, never a rounding win.
    for r in rows:
        if r['condition']==CONDITIONS[2]:
            if (r['task_id']=='e6_b01' and r['defense']==DEFENSES[1] and r['replicate_id']==1
                or r['task_id']=='e6_b02' and r['defense']==DEFENSES[1] and r['replicate_id']<3
                or r['task_id']=='e6_b03' and r['defense']==DEFENSES[0]):r['episode_reconstructable_disclosure']=1
    d=comparisons(rows,c)[-1]
    assert d['task_cluster_effects'][CONDITIONS[2]]['paired_leak_difference']==0
    assert not d['BOTH_HELDOUT_PRIVACY_BETTER']
