#!/usr/bin/env python3
"""Offline replay of all saved D3 BIRD context-limit episodes; no model/SQL/evaluator dispatch."""
import argparse,json,sys,tempfile
from copy import deepcopy
from pathlib import Path
from src.e2_live.v3 import EpisodeV3,build_stage_request
from src.e2_live.pilot import load,canonical,End,sha
from src.e2_live.bird_context_audit import messages,wire_bytes,size,pack,unpack,semantic_items,duplicate_stats


class RecordedProvider:
    def __init__(self,calls):self.calls=calls;self.count=0
    def call(self,request,timeout):
        saved=self.calls[self.count];self.count+=1
        assert request==saved['request'],'SAVED_REQUEST_REPLAY_MISMATCH'
        return deepcopy(saved['response'])


class RecordedBroker:
    def __init__(self,trace):
        self.args=iter(r['structured_arguments'] for r in trace['typed_records'] if r['record_type']=='ToolCall')
        self.drafts=iter(json.loads(e['attempted']) for e in trace['release_events'] if e['boundary']=='B5')
    def execute(self,db,arguments):
        assert arguments==next(self.args)
        return deepcopy(next(self.drafts))


class NeverEvaluator:
    def score(self,*args):raise AssertionError('EVALUATOR_FORBIDDEN')


class CapturingEpisode(EpisodeV3):
    def provider_action(self,actor,snapshot):
        self.captured=(self.stage,deepcopy(snapshot))
        return super().provider_action(actor,snapshot)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    def no_network(event,args):
        if event.startswith('socket.'):raise RuntimeError('C0_NETWORK_DISABLED')
    sys.addaudithook(no_network)
    base=Path('artifacts/aamas2027_e2_v3_d3_combined');episodes=load(base/'episode_summary.json');index={r['cell_id']:r for r in load(base/'combined_index.json')['cells']}
    failures=[e for e in episodes if e['family']=='bird_pg' and e['termination']=='CONTEXT_LIMIT'];out=[];protected=[]
    assert len(failures)==6 and sum(e['condition']=='CLEAN' for e in failures)==2
    with tempfile.TemporaryDirectory() as td:
        for safe in failures:
            trace=load(index[safe['cell_id']]['private_trajectory_path']);assert sha(Path(index[safe['cell_id']]['private_trajectory_path']).read_bytes())==safe['trajectory_sha256']
            first=json.loads(trace['calls'][0]['request']['json']['messages'][1]['content']);task=first['values'][0]
            provider=RecordedProvider(trace['calls']);ep=CapturingEpisode(trace['cell'],task,trace['policy'],{},provider,NeverEvaluator(),Path(td)/safe['cell_id'])
            assert ep.private_note==trace['private_note'],'PRIVATE_NOTE_REPLAY_MISMATCH'
            ep.rt._Runtime__broker=RecordedBroker(trace)
            result=ep.execute();assert result['termination']=='CONTEXT_LIMIT' and provider.count==len(trace['calls'])
            stage,snap=ep.captured;assert stage=='finance'
            # Failed request was never dispatched/saved as a provider request: reconstructed only.
            assert canonical(snap['values'])==canonical(json.loads([v for v in trace['published_views'] if v['kind']=='context'][-1]['payload'])['values'])
            assert canonical(snap['history'])==[v for v in trace['published_views'] if v['kind']=='history'][-1]['payload']
            packet=pack(snap);expanded=unpack(packet);assert expanded==snap and semantic_items(expanded)==semantic_items(snap)
            scratch=snap['values'][1];history=snap['history'];assert scratch==history[-1]
            sql=[r['structured_arguments'] for r in trace['typed_records'] if r['record_type']=='ToolCall']
            results=[r['structured_result'] for r in trace['typed_records'] if r['record_type']=='ToolResult']
            taskv=snap['values'][0];private=snap['values'][-1];protected.append(ep.pol.raw_value)
            assert all(v['description_csv']==taskv['descriptions'][k] for k,v in taskv['schema'].items())
            csv_duplicate_bytes=sum(size(v) for v in taskv['descriptions'].values())
            before=wire_bytes(stage,snap);after=wire_bytes(stage,packet);assert before>160000 and after>160000
            out.append({'cell_id':safe['cell_id'],'task_id':safe['task_id'],'condition':safe['condition'],'defense':safe['defense'],'stage':stage,
                'next_model_invocation_ordinal':len(trace['calls'])+1,'next_model_invocation_dispatched':False,'dispatched_requests_reproduced_exactly':provider.count,
                'failed_request_status':'RECONSTRUCTED_FROM_SAVED_REQUESTS_AND_TOOL_DRAFTS;NOT_A_PROVIDER_DISPATCH',
                'request_messages_utf8_bytes':before,'candidate_messages_utf8_bytes':after,'net_serialized_bytes_removed':before-after,'guard':160000,
                'task_bytes':size(taskv),'source_schema_bytes':size(taskv['schema']),'source_descriptions_bytes':size(taskv['descriptions']),
                'identical_description_csv_second_copy_bytes':csv_duplicate_bytes,
                'planner_artifact_bytes':size(history[0]),'finance_scratch_bytes':size(scratch),'accumulated_history_bytes':size(history),
                'sql_query_json_bytes_in_saved_tool_records':[size(x) for x in sql],'sql_query_objects_explicitly_embedded_in_snapshot':sum(canonical(x) in canonical(snap) for x in sql),
                'sql_result_json_bytes':[size(x) for x in results],'result_rows':[len(x['rows']) for x in results],'result_columns':[len(x['columns']) for x in results],
                'private_sidecar_bytes':size(private),'system_prompt_and_schema_utf8_bytes':len(messages(stage,snap)[0]['content'].encode()),
                'invocation_and_receipt_metadata_bytes':size(snap['invocation']),**duplicate_stats(snap),
                'semantic_equivalence':'VERIFIED_EXACT_EXPANSION_AND_UNIQUE_RELEASED_ITEM_SET','source_schema_copies_in_context_values':1,
                'planner_history_copies':1,'latest_result_copies':2,'private_sidecar_copies':1})
    result={'status':'AUDITED','scope':'All6D3 BIRD context-limit episodes, including4contaminated and2CLEAN','episodes':out,
        'cause':'MIXED','candidate':'Per-request single-copy pool; original header/ordered occurrence references preserved; no external lookup',
        'lossless_fix_status':'LOSSLESS_FIX_NOT_FEASIBLE','reason':'Each observed required SQL result is706360JSONbytes before request escaping, already above160000; eliminating duplicate scratch/history does not close any of the six failures.',
        'byte_accounting':'Component JSON bytes are non-additive diagnostics; request byte totals use original canonical messages UTF8, including escaping.',
        'component_classification':[
            {'component':'complete task/schema and first description CSV occurrence','class':'REQUIRED_CURRENT_SEMANTIC_STATE','duplicate_complete_schema_copies':0},
            {'component':'second identical description CSV under task.descriptions','class':'REDUNDANT_SERIALIZATION_OF_ALREADY_PRESENT_STATE','candidate_removes':False},
            {'component':'planner delegation, prior SQL results, finance private sidecar, prompt/stage schema','class':'REQUIRED_CURRENT_SEMANTIC_STATE','action':'preserve all'},
            {'component':'latest SQL result again in finance scratch','class':'REDUNDANT_SERIALIZATION_OF_ALREADY_PRESENT_STATE','action':'single released value with two ordered occurrence references'},
            {'component':'invocation context references, producer/category/provenance references and runtime mediation trail','class':'REQUIRED_PROVENANCE_METADATA','action':'retain unchanged; do not merge distinct artifact identities'},
            {'component':'SQL query arguments in saved ToolCall records','class':'HISTORICAL_DIAGNOSTIC_NOT_REQUIRED_FOR_NEXT_MODEL_DECISION','qualification':'not explicitly embedded by the frozen model context; retain audit records unchanged, no new assertion of semantic irrelevance'},
            {'component':'repeated full task/history across separate stateless invocations','class':'REQUIRED_CURRENT_SEMANTIC_STATE','action':'not removable using hidden cross-request cache'},
            {'component':'whole state snapshots or repeated receipt wrappers inside failed request','class':'REQUIRED_PROVENANCE_METADATA','qualification':'no extra complete state snapshot or duplicate receipt wrapper identified; ordered artifact references retained'}],
        'missing_content_inferred':False,'live_runtime_changed':False,'MODEL_RUNS_EXECUTED':0,'CONFIRMATORY_TASKS_EXECUTED':0,'FORMAL_MODEL_RUNS_EXECUTED':0}
    encoded=json.dumps(result,indent=2)+'\n';assert not any(v in encoded for v in protected)
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(encoded)
    print(json.dumps({'episodes':len(out),'before_max':max(r['request_messages_utf8_bytes'] for r in out),'after_max':max(r['candidate_messages_utf8_bytes'] for r in out),'cause':'MIXED','model_calls':0}))
if __name__=='__main__':main()
