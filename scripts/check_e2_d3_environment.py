#!/usr/bin/env python3
"""D3-only original evaluator/broker fixture checks; no model calls or live episodes."""
import argparse
import tempfile
from pathlib import Path
from src.e2_live.pilot import *
from src.e2_live.d3 import verify as integrity, d3_inputs as inputs
from src.e2_s1.adapters import source_output

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source-root',type=Path,required=True);p.add_argument('--schema',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    checks=integrity(a.source_root);schema=load(a.schema);tasks,policies,golds=inputs(a.source_root,schema)
    evaluator=Evaluator(a.source_root,golds);report=[]
    with tempfile.TemporaryDirectory() as td:
        for family in ('bird_pg','tatqa','hotpot'):
            key=next(k for k in tasks if k[0]==family);gold=golds[key];task=tasks[key]
            output=({'sql':gold['SQL']} if family=='bird_pg' else {'answer':gold['answer'],'scale':gold['scale']} if family=='tatqa' else {'answer':gold['answer'],'supporting_facts':hotpot_native(gold)['supporting_facts']})
            cell={'family':family,'task_id':key[1]};native=source_output(family,task,output)
            metric=evaluator.score(cell,native,Path(td)/family,120)
            assert task_success(family,metric)
            report.append({'family':family,'source_reference_fixture_pass':True,'original_metric_keys':list(metric)})
            if family=='bird_pg':
                result=supervised('tool',(schema,task['db_id'],{'sql':gold['SQL']}),30);assert result['ok']
                blocked=supervised('tool',(schema,task['db_id'],{'sql':'CREATE TABLE forbidden_fixture(x int)'}),30)
                assert not blocked['ok'] and blocked['error']['code']=='READ_ONLY_REQUIRED'
    try:supervised('tool',(schema,next(iter(schema)),{'sql':'SELECT 1'}),0.000001)
    except TimeoutError:pass
    else:raise AssertionError('SUPERVISOR_DEADLINE')
    assert not mp.active_children()
    import psycopg2
    with psycopg2.connect(dbname='bird',user='postgres',host='127.0.0.1') as conn:
        with conn.cursor() as c:
            c.execute("SELECT current_setting('server_version'),current_setting('server_encoding'),current_setting('lc_collate'),current_setting('lc_ctype'),current_setting('TimeZone')")
            environment=list(c.fetchone())
    assert environment[0].startswith('14.24') and environment[1:]==['UTF8','C','C','Asia/Shanghai']
    result={'status':'PASS','integrity':checks,'environment':environment,'fixtures':report,'broker_reference_select':'PASS','broker_write_denied':'PASS','supervised_timeout_cancel_join':'PASS','source_schema_sha256':sha(a.schema.read_bytes()),'model_calls':0,'development_episodes':0,'confirmatory_tasks':0}
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
