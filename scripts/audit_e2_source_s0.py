#!/usr/bin/env python3
"""Read pinned public sources and run original deterministic evaluators; no solvers/models."""
import argparse
import ast
import contextlib
import csv
import gzip
import importlib.util
import io
import json
from pathlib import Path
import re
import sys
import tempfile
import types


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def rows(path):
    if path.suffix == '.parquet':
        import pyarrow.parquet as pq
        return pq.read_table(path).to_pylist()
    text = path.read_text()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return [json.loads(line) for line in text.splitlines() if line]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, required=True)
    parser.add_argument('--dependency-path', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.dependency_path:
        sys.path.insert(0, str(args.dependency_path))
    root, out = args.source_root, args.output
    out.mkdir(parents=True, exist_ok=True)
    inventory, ids = {}, []
    def record(name, data, key, split, group=None):
        values = [str(x[key]) for x in data]
        inventory[name] = {'rows': len(data), 'unique_ids': len(set(values)), 'split': split}
        for x in data:
            ids.append({'source': name, 'source_split': split, 'task_id': str(x[key]),
                        'context_group': str(x.get(group, '')) if group else ''})
    bird = rows(root/'data/birdsql__bird_mini_dev__data__mini_dev_sqlite-00000-of-00001.json')
    record('bird_mini_sqlite', bird, 'question_id', 'mini_dev_sqlite', 'db_id')
    pg=rows(root/'data/birdsql__bird_mini_dev__data__mini_dev_pg-00000-of-00001.json')
    record('bird_mini_pg',pg,'question_id','mini_dev_pg','db_id')
    swe = rows(root/'data/SWE-bench__SWE-bench_Verified__data__test-00000-of-00001.parquet')
    record('swe_verified', swe, 'instance_id', 'test', 'repo')
    for f in sorted((root/'data').glob('birdsql__*.jsonl')):
        v = rows(f); name=f.name.split('__')[1]
        record(name,v,'instance_id','dev','selected_database')
        inventory[name]['nonempty_fields']={k:sum(bool(x.get(k)) for x in v) for k in ['sol_sql','test_cases','external_knowledge']}
    tat = rows(root/'tatqa/dataset_raw/tatqa_dataset_dev.json')
    flat = [{**q,'context_uid':c['table']['uid']} for c in tat for q in c['questions']]
    record('tatqa_dev',flat,'uid','dev','context_uid')
    inventory['tatqa_dev']['contexts']=len(tat)
    fin = rows(root/'finqa/dataset/test.json')
    record('finqa_public_test',fin,'id','test','filename')
    inventory['finqa_public_test']['report_pages']=len({x['filename'] for x in fin})
    hotraw=rows(root/'data/hotpot_distractor_validation.parquet')
    record('hotpot_distractor_dev',hotraw,'id','validation')
    hot=[{'_id':x['id'],'question':x['question'],'answer':x['answer'],
          'supporting_facts':list(map(list,zip(x['supporting_facts']['title'],x['supporting_facts']['sent_id']))),
          'context':list(map(list,zip(x['context']['title'],x['context']['sentences'])))} for x in hotraw]
    with gzip.open(root/'humaneval/data/HumanEval.jsonl.gz','rt') as f:human=[json.loads(x) for x in f]
    record('humaneval',human,'task_id','test')
    with (root/'data/browsecomp_encrypted.csv').open() as f:browse=list(csv.DictReader(f))
    inventory['browsecomp']={'rows':len(browse),'columns':list(browse[0]),'plaintext_decrypted':False,'ids':'row positions in versioned blob; no native task ID assumed'}
    # Eligibility is metadata-only; never filter on any solver/defense outcome.
    required_checks = {}
    for name, data, key, predicate in [
        ('bird_mini_sqlite', bird, 'question_id', lambda x: all(k in x for k in ['question','db_id','evidence','SQL','difficulty']) and bool(x['question']) and x['SQL'].lstrip().split()[0].upper() in ['SELECT','WITH']),
        ('bird_mini_pg', pg, 'question_id', lambda x: all(k in x for k in ['question','db_id','evidence','SQL','difficulty']) and bool(x['question']) and x['SQL'].lstrip().split()[0].upper() in ['SELECT','WITH']),
        ('tatqa_dev', flat, 'uid', lambda x: all(k in x for k in ['question','answer','scale','answer_type']) and bool(x['question'])),
        ('finqa_public_test', fin, 'id', lambda x: bool(x['table']) and bool(x['pre_text'] or x['post_text']) and all(k in x['qa'] for k in ['question','program','exe_ans'])),
        ('hotpot_distractor_dev', hotraw, 'id', lambda x: bool(x['question']) and bool(x['answer']) and len(x['context']['title']) == len(x['context']['sentences']) > 0 and len(x['supporting_facts']['title']) == len(x['supporting_facts']['sent_id']) > 0),
    ]:
        failures = [str(x[key]) for x in data if not predicate(x)]
        required_checks[name] = {'total':len(data), 'metadata_eligible':len(data)-len(failures), 'unresolved_ids':failures}
    (out/'source_schema_eligibility.json').write_text(json.dumps(required_checks,indent=2)+'\n')
    with (out/'OFFICIAL_TASK_ID_INVENTORY.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(ids[0]), lineterminator="\n");w.writeheader();w.writerows(ids)
    (out/'source_inventory.json').write_text(json.dumps(inventory,indent=2)+'\n')
    checks={}
    with tempfile.TemporaryDirectory(prefix='e2_s0_fixtures_') as td:
        tmp=Path(td)
        # Original TAT-QA scorer, unchanged. Gold fixtures are never runtime input.
        sys.path.insert(0,str(root/'tatqa'))
        from tatqa_metric import TaTQAEmAndF1
        for mode in ['native_scalar_gold','native_list_gold','serialized_list_gold','missing']:
            metric=TaTQAEmAndF1()
            for q in flat:
                a=q['answer']
                if mode in ['native_list_gold','serialized_list_gold']:
                    a=a if isinstance(a,list) else [a]
                if mode=='serialized_list_gold':a=json.loads(json.dumps(a))
                if mode=='missing':a=None
                metric(q,a,q['scale'])
            checks['tatqa_'+mode]=[float(x) for x in metric.get_overall_metric()]
        checks['tatqa_metrics_order']=['EM','F1','scale','operation (not supplied by official answer API)']
        # Original BIRD EX and F1 on the entire smallest official DB partition.
        sys.path.insert(0,str(root/'bird_mini/evaluation'))
        ex=module('bird_ex',root/'bird_mini/evaluation/evaluation_ex.py')
        f1=module('bird_f1',root/'bird_mini/evaluation/evaluation_f1.py')
        import evaluation_utils
        selected=[x for x in bird if x['db_id']=='superhero']
        result=[]
        for i,x in enumerate(selected):
            sql=x['SQL'];serialized=json.loads(json.dumps(sql))
            native=ex.execute_model(sql,sql,str(root/'data/superhero.sqlite'),i,30,'SQLite')['res']
            adapted=ex.execute_model(serialized,sql,str(root/'data/superhero.sqlite'),i,30,'SQLite')['res']
            soft=evaluation_utils.execute_sql(serialized,sql,str(root/'data/superhero.sqlite'),'SQLite',f1.calculate_f1_score)
            result.append({'task_id':str(x['question_id']),'native_ex':native,'serialized_ex':adapted,'soft_f1':soft})
        checks['bird_official_db_gold']={'cases':len(result),'results':result,'fixture_rule':'all tasks from smallest DB archive entry; not development/confirmatory selection'}
        checks['bird_invalid_sql']=ex.execute_model('NOT VALID SQL',selected[0]['SQL'],str(root/'data/superhero.sqlite'),0,30,'SQLite')['res']
        # Original HotpotQA evaluator and all twelve metrics, unchanged.
        hp=module('hotpot_eval',root/'hotpot/hotpot_evaluate_v1.py')
        gold=tmp/'hotpot_gold.json';gold.write_text(json.dumps(hot))
        good={'answer':{x['_id']:x['answer'] for x in hot},'sp':{x['_id']:x['supporting_facts'] for x in hot}}
        bad={'answer':{x['_id']:'S0_INVALID_ANSWER' for x in hot},'sp':{x['_id']:[] for x in hot}}
        for name,pred in [('native_gold',good),('serialized_gold',json.loads(json.dumps(good))),('wrong',bad)]:
            f=tmp/(name+'.json');f.write_text(json.dumps(pred));buf=io.StringIO()
            with contextlib.redirect_stdout(buf):hp.eval(str(f),str(gold))
            checks['hotpot_'+name]=ast.literal_eval(buf.getvalue().strip().splitlines()[-1])
        # Original FinQA public evaluator; retain assertion failures rather than repair gold.
        fq=module('finqa_eval',root/'finqa/code/evaluate/evaluate.py')
        pred=[{'id':x['id'],'predicted':fq.program_tokenization(x['qa']['program'])} for x in fin]
        f=tmp/'fin_gold_predictions.json';f.write_text(json.dumps(pred));buf=io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):v=fq.evaluate_result(str(f),str(root/'finqa/dataset/test.json'))
            checks['finqa_gold']={'status':'COMPLETED','execution_accuracy':v[0],'program_accuracy':v[1]}
        except Exception as e:
            checks['finqa_gold']={'status':'ORIGINAL_EVALUATOR_EXCEPTION','exception_type':type(e).__name__,'raw_gold_output_saved':False}
        # Execute only original BrowseComp grade_sample method with a deterministic fake sampler.
        tree=ast.parse((root/'simple_evals/browsecomp_eval.py').read_text())
        cls=next(x for x in tree.body if isinstance(x,ast.ClassDef) and x.name=='BrowseCompEval')
        fn=next(x for x in cls.body if isinstance(x,ast.FunctionDef) and x.name=='grade_sample')
        template=next(x for x in tree.body if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='GRADER_TEMPLATE' for t in x.targets))
        ns={'re':re};exec(compile(ast.Module(body=[template,fn],type_ignores=[]),'<original BrowseComp method>','exec'),ns)
        class Stub:
            def _pack_message(self,**kw):return kw
            def __call__(self,messages):return types.SimpleNamespace(response_text='correct: yes')
        grade=ns['grade_sample'](types.SimpleNamespace(grader_model=Stub()),'synthetic question','synthetic answer','synthetic response')
        call=next(x for x in cls.body if isinstance(x,ast.FunctionDef) and x.name=='__call__')
        original_test=next(x.value for x in ast.walk(call) if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='is_correct' for t in x.targets))
        score=eval(compile(ast.Expression(original_test),'<original BrowseComp score comparison>','eval'),{'grade_result':grade})
        checks['browsecomp_stub']={'stub_text':'correct: yes','original_grade_return':grade,'original_is_correct':score,'live_calls':0,'code_modified':False}
    report={'scope':'ORIGINAL_EVALUATOR_GOLD_OR_DETERMINISTIC_FIXTURES_ONLY','checks':checks,'formal_model_runs':0,'development_model_runs':0,'task_solvers_executed':0,'final_ids_selected':0,'sources_modified':False}
    (out/'evaluator_sanity.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'inventories':len(inventory),'enumerated_rows':len(ids),'checks':{k:v for k,v in checks.items() if k!='bird_official_db_gold'},'bird_cases':len(result)},indent=2))


if __name__=='__main__':main()
