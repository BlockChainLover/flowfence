#!/usr/bin/env python3
"""Precommitted metadata-only D3 selection; no model/source-content/evaluator access."""
import argparse
from collections import defaultdict, Counter
from copy import deepcopy
import csv
import gzip
import json
from pathlib import Path
import subprocess

RULE_FILES=('E2_D3_SELECTION_RULE.md','scripts/select_e2_d3.py')
FROZEN=Path('artifacts/aamas2027_e2_source_s1f')
OUT=Path('artifacts/aamas2027_e2_v3_d3')


def load(p):return json.loads(Path(p).read_text())
def save(p,v):p.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
def git(*args):return subprocess.check_output(['git',*args]).decode().strip()


def select(meta, exclusions):
    bird=defaultdict(list);tat=defaultdict(list);hot={}
    for (f,tid),row in sorted(meta.items()):
        if f=='hotpot':hot[tid]=json.loads(row['cluster'])
        elif (f,tid) not in exclusions:
            (bird if f=='bird_pg' else tat)[row['cluster'].split('|')[0] if f=='bird_pg' else row['cluster']].append(tid)
    excluded_tat={meta[k]['cluster'] for k in exclusions if k[0]=='tatqa'}
    tat={k:v for k,v in tat.items() if k not in excluded_tat}
    parent={tid:tid for tid in hot};owners={}
    def find(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]];x=parent[x]
        return x
    for tid,titles in sorted(hot.items()):
        for title in sorted(set(titles)):
            if title in owners:
                a,b=find(tid),find(owners[title]);parent[max(a,b)]=min(a,b)
            else:owners[title]=tid
    components=defaultdict(list)
    for tid in sorted(hot):components[find(tid)].append(tid)
    banned={find(tid) for f,tid in exclusions if f=='hotpot'}
    available={k:v for k,v in components.items() if k not in banned}
    assert min(len(bird),len(tat),len(available))>=3,'INSUFFICIENT_D3_DIVERSITY_NO_RELAXATION'
    selected={'bird_pg':[sorted(bird[k])[0] for k in sorted(bird)[:3]],
              'tatqa':[sorted(tat[k])[0] for k in sorted(tat)[:3]],
              'hotpot':[available[k][0] for k in sorted(available)[:3]]}
    return selected,{tid:find(tid) for tid in hot},{k:len(v) for k,v in components.items()}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--rule-commit',required=True);p.add_argument('--output',type=Path,default=OUT);a=p.parse_args()
    commit=git('rev-parse',a.rule_commit+'^{commit}');git('merge-base','--is-ancestor',commit,'HEAD')
    for path in RULE_FILES:assert subprocess.check_output(['git','show',commit+':'+path])==Path(path).read_bytes()
    assert not a.output.exists(),'NO_OVERWRITE_SELECTED_D3'
    config=load('experiments/e2_source_s1f/selection_config.json')
    with gzip.open(config['eligibility'],'rt') as f:eligible={(r['family'],r['task_id']):r for r in map(json.loads,f)}
    with gzip.open(config['clusters'],'rt') as f:meta={(r['family'],r['task_id']):r for r in csv.DictReader(f)}
    assert set(meta)==set(eligible) and len(meta)==9573
    assert Counter(f for f,tid in eligible)=={'bird_pg':500,'tatqa':1668,'hotpot':7405}
    for f,tid in meta:
        assert eligible[f,tid]['status']=='ELIGIBLE' and eligible[f,tid]['naturalness']=='NATURAL'
        assert eligible[f,tid]['compatible_types']=={'bird_pg':['P4'],'tatqa':['P1','P3'],'hotpot':['P2','P3']}[f]
    old=load(FROZEN/'development.json')+load(FROZEN/'confirmatory.json')+load('artifacts/aamas2027_e2_v2_d2/development.json')
    exclusions={(r['family'],r['task_id']) for r in old};assert len(exclusions)==78
    selected,components,sizes=select(meta,exclusions)
    rows=[]
    for family in ('bird_pg','tatqa','hotpot'):
        for position,(tid,typ) in enumerate(zip(selected[family],config['dev_types'][family]),1):
            m=meta[family,tid];assert (family,tid) not in exclusions
            assert m['authorized_principal']=='finance_agent' and m['forbidden']=='doc_writer_agent;final_output' and m['contamination_surface']=='internal_message'
            rows.append({'namespace':'E2_DEVELOPMENT_V3_D3','split':'development_d3','permanently_development_only':True,
                'family':family,'task_id':tid,'fact_type':typ,'selection_position_in_family':position,
                'context_cluster_id':m['cluster'],'overlap_component_id':components.get(tid),
                'overlap_component_size':sizes.get(components.get(tid)),
                'compatible_types':eligible[family,tid]['compatible_types'],'eligibility':'ELIGIBLE','naturalness':'NATURAL',
                'source_pin':next(r['source_pin'] for r in old if r['family']==family),
                'evaluator_identifier':config['evaluator_ids'][family]})
    templates=load('experiments/e2_source_s1f/policy_templates.json');policies=[]
    for ordinal,row in enumerate(sorted(rows,key=lambda r:(r['family'],r['task_id'])),79):
        policy={k:deepcopy(v) for k,v in templates.items() if k not in ('fact_templates','ordinal_rule','secret_id_rule','limitations')}
        policy.update(family=row['family'],task_id=row['task_id'],split='development_d3',namespace='E2_DEVELOPMENT_V3_D3',fact_type=row['fact_type'],
            fact_generation_template=templates['fact_templates'][row['fact_type']],generation_ordinal=ordinal,
            secret_id=f"e2_private_{row['family']}_{row['task_id']}_{row['fact_type']}")
        policies.append(policy)
    schedule=[]
    for c in range(3):
        for t,row in enumerate(sorted(rows,key=lambda r:(r['family'],r['task_id']))):
            arms=['EXACT_IFC','FLOWFENCE_R2'] if (c+t)%2==0 else ['FLOWFENCE_R2','EXACT_IFC']
            for arm in arms:
                n=len(schedule)+1
                schedule.append({'namespace':'E2_DEVELOPMENT_V3_D3','cell_id':f'E2_DEVELOPMENT_V3_D3_{n:03d}','order':n,
                    'family':row['family'],'task_id':row['task_id'],'fact_type':row['fact_type'],
                    'condition':['CLEAN','CONTAMINATION_A','CONTAMINATION_B'][(c+t)%3],'defense':arm,'repetition':1})
    assert len(rows)==9 and len(schedule)==54
    a.output.mkdir(parents=True)
    save(a.output/'development.json',rows);save(a.output/'policy_skeletons.json',policies);save(a.output/'CELL_SCHEDULE.json',schedule)
    save(a.output/'selection_provenance.json',{'D3_SELECTION_RULE_COMMIT':commit,'namespace':'E2_DEVELOPMENT_V3_D3',
        'eligible_pool':config['eligibility'],'cluster_metadata':config['clusters'],'excluded_ids':78,'D3_TASKS_SELECTED':9,
        'D3_DISJOINT_FROM_V1_DEV':True,'D3_DISJOINT_FROM_D2_DEV':True,'D3_DISJOINT_FROM_CONFIRMATORY':True,'ranking_inputs':'IDs,compatible types,cluster metadata,exclusion lists only',
        'source_content_read':False,'model_outputs_read':False,'raw_values_instantiated':False,
        'confirmatory_quotas_unchanged':{'P1':15,'P2':15,'P3':10,'P4':20},'D3_MODEL_RUNS_EXECUTED':0})
    print(json.dumps({'rule_commit':commit,'selected':9,'cells':54,'model_calls':0}))
if __name__=='__main__':main()
