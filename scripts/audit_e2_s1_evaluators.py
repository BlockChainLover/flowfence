#!/usr/bin/env python3
"""Original evaluator fixtures only; no model calls. Gold remains outside runtime."""
import argparse, ast, contextlib, hashlib, importlib.util, io, json, sys, tempfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from src.e2_s1.adapters import task_input, source_output, hotpot_native, hotpot_mirror


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-root', type=Path, required=True)
    p.add_argument('--dependency-path', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--phase', choices=['qa','pg'], required=True)
    a=p.parse_args();sys.path.insert(0,str(a.dependency_path));r=a.source_root;a.output.mkdir(parents=True,exist_ok=True)
    report={'formal_model_runs':0,'development_model_runs':0,'source_code_modified':False}
    if a.phase=='qa':
        import pyarrow.parquet as pq
        sys.path.insert(0,str(r/'tatqa'))
        from tatqa_metric import TaTQAEmAndF1
        tat=json.loads((r/'tatqa/dataset_raw/tatqa_dataset_dev.json').read_text())
        metrics={k:TaTQAEmAndF1() for k in ['native_list','adapted_list','native_scalar','missing']}
        n=0
        for c in tat:
            for q in c['questions']:
                task=task_input('tatqa',q,context=c)
                assert set(task)=={'uid','order','question','table','paragraphs','capabilities'}
                assert task['table']==c['table'] and task['paragraphs']==c['paragraphs']
                out=source_output('tatqa',task,{'answer':q['answer'],'scale':q['scale']})[q['uid']]
                native=q['answer'] if isinstance(q['answer'],list) else [q['answer']]
                assert out==[native,q['scale']]
                for name,answer in [('native_list',native),('adapted_list',out[0]),('native_scalar',q['answer']),('missing',None)]:metrics[name](q,answer,q['scale'])
                n+=1
        from tatqa_eval import evaluate_prediction_file
        with tempfile.TemporaryDirectory() as td:
            pred=Path(td)/'predictions.json'
            mapping={}
            for c in tat:
                for q in c['questions']:
                    mapping.update(source_output('tatqa',task_input('tatqa',q,context=c),{'answer':q['answer'],'scale':q['scale']}))
            pred.write_text(json.dumps(mapping));buf=io.StringIO()
            with contextlib.redirect_stdout(buf):evaluate_prediction_file(str(r/'tatqa/dataset_raw/tatqa_dataset_dev.json'),str(pred))
            wrapper_summary=[line for line in buf.getvalue().splitlines() if line.startswith(('Exact-match accuracy','F1 score','Scale score'))]
            assert wrapper_summary==['Exact-match accuracy 100.00','F1 score 100.00','Scale score 100.00']
        report['tatqa']={'original_file_entrypoint_summary':wrapper_summary,'questions':n,'contexts':len(tat),'metrics_order':['EM','F1','scale','operation'],'metrics':{k:list(v.get_overall_metric()) for k,v in metrics.items()},'serialization':'uid -> [answer-list, scale]','input_output_equivalence':True}
        hot=pq.read_table(r/'data/hotpot_distractor_validation.parquet').to_pylist();native=[hotpot_native(x) for x in hot]
        good={'answer':{},'sp':{}}
        for x,nat in zip(hot,native):
            assert hotpot_mirror(nat)==x
            task=task_input('hotpot',x)
            assert [[v['title'],[s['text'] for s in v['sentences']]] for v in task['context']]==nat['context']
            pred=source_output('hotpot',task,{'answer':x['answer'],'supporting_facts':nat['supporting_facts']})
            for k in good:good[k].update(pred[k])
        hp=load('hotpot_original',r/'hotpot/hotpot_evaluate_v1.py');scores={}
        with tempfile.TemporaryDirectory() as td:
            gold=Path(td)/'gold.json';gold.write_text(json.dumps(native))
            for name,pred in [('adapted_gold',good),('wrong',{'answer':{x['id']:'INVALID_S1_OUTPUT' for x in hot},'sp':{x['id']:[] for x in hot}})]:
                path=Path(td)/'pred.json';path.write_text(json.dumps(pred));buf=io.StringIO()
                with contextlib.redirect_stdout(buf):hp.eval(str(path),str(gold))
                scores[name]=ast.literal_eval(buf.getvalue().strip().splitlines()[-1])
        report['hotpot']={'questions':len(hot),'lossless_all_fields':True,'metrics':scores}
    else:
        import psycopg2
        sys.path.insert(0,str(r/'bird_mini/evaluation'))
        ex=load('original_ex',r/'bird_mini/evaluation/evaluation_ex.py'); f1=load('original_f1',r/'bird_mini/evaluation/evaluation_f1.py');ves=load('original_ves',r/'bird_mini/evaluation/evaluation_ves.py')
        rows=json.loads((r/'data/birdsql__bird_mini_dev__data__mini_dev_pg-00000-of-00001.json').read_text())
        with psycopg2.connect(dbname='bird',user='postgres',host='127.0.0.1') as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version(), current_setting('lc_collate'), current_setting('lc_ctype'), current_setting('TimeZone')");report['environment']=list(cur.fetchone())
        def check(pair):
            i,x=pair;sql=x['SQL'];buf=io.StringIO()
            # Do not capture global stdout concurrently. Official routines print no raw query on success.
            native=ex.execute_model(sql,sql,'',i,30,'PostgreSQL')['res']
            adapted=ex.execute_model(json.loads(json.dumps(sql)),sql,'',i,30,'PostgreSQL')['res']
            soft=f1.execute_model(sql,sql,'',i,30,'PostgreSQL')['res']
            return {'task_id':str(x['question_id']),'native_ex':native,'adapted_ex':adapted,'f1':soft}
        results=[]
        with ThreadPoolExecutor(max_workers=4) as pool:
            for result in pool.map(check,enumerate(rows)):
                results.append(result)
                if len(results)%50==0:
                    (a.output/'pg_progress.json').write_text(json.dumps({'completed':len(results),'total':500}))
        report['bird']={'records':results,'query_timeout_seconds':30,'ex_f1_workers':4,'negative_ex':ex.execute_model('NOT VALID SQL',rows[0]['SQL'],'',0,30,'PostgreSQL')['res']}
        # Fixed first five source records, three repeats, 100 original timing iterations, one worker.
        report['ves']={'workers':1,'iterations':100,'repeats':3,'selection':'first five source records, predeclared; no outcome selection','records':[]}
        for i,x in enumerate(rows[:5]):
            rewards=[ves.execute_model(x['SQL'],x['SQL'],'',i,100,30,'PostgreSQL')['reward'] for _ in range(3)]
            report['ves']['records'].append({'task_id':str(x['question_id']),'rewards':rewards})
        report['ves']['repeatable']=all(len(set(x['rewards']))==1 for x in report['ves']['records'])
    (a.output/(a.phase+'_evaluator.json')).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'phase':a.phase,'completed':True}))
if __name__=='__main__':main()
