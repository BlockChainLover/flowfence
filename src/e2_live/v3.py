"""Final E2 candidate: trusted stage order, model-generated content, original mediation."""
from src.e2_live.pilot import *
from src.e2_live.transport_v2 import TransportFailure, diagnostics, LiveProviderV2
from scripts.validate_e2_live_config import unique_object
from jsonschema import Draft202012Validator

V3_CONFIG=Path('experiments/e2_v3_d1')
ROLES={'planner':'planner_agent','finance':'finance_agent','writer':'doc_writer_agent'}


def stage_schema(stage,family):
    schemas=load(V3_CONFIG/'STAGE_SCHEMAS.json')
    return schemas[stage] if stage=='planner' else schemas[stage][family]


def parse_stage(text,stage,family):
    def invalid(value):raise ValueError('NONFINITE')
    value=json.loads(text,object_pairs_hook=unique_object,parse_constant=invalid)
    Draft202012Validator(stage_schema(stage,family)).validate(value)
    canonical(value)
    return value


def build_stage_request(stage,family,snapshot):
    actor=ROLES[stage];invocation=snapshot['invocation']
    assert invocation['recipient_principal']==actor and invocation['provider']=='minimax'
    assert all(x['category']!='EVALUATOR_PRIVATE' for x in invocation['context'])
    model=load(CONFIG/'LIVE_MODEL_CONFIG.json')
    text=(V3_CONFIG/'prompts/common.txt').read_text()+'\n'+(V3_CONFIG/f'prompts/{stage}.txt').read_text()
    text+='\nSTAGE_SCHEMA\n'+canonical(stage_schema(stage,family))
    if stage=='finance' and family=='bird_pg':
        text+='\nREADONLY_SQL_CONTRACT\n'+canonical(load(CONFIG/'FAMILY_PROFILES.json')[family]['tools'][0]['arguments'])
    messages=[{'role':'system','content':text},{'role':'user','content':canonical(snapshot)}]
    if len(canonical(messages).encode())>model['context']['max_request_messages_utf8_bytes']:raise ValueError('CONTEXT_LIMIT')
    return {'method':'POST','url':model['endpoint'],'headers':{'Content-Type':'application/json'},'json':dict(model['request_parameters'],messages=messages)}


class FinalStageRuntime(AuditRuntime):
    def __init__(self,*args,stage_owner,**kwargs):
        self.stage_owner=stage_owner
        super().__init__(*args,**kwargs)
    def _query(self,handle,arguments):
        if self._Runtime__actor(handle)!='finance_agent':raise Rejected('FINANCE_TOOL_STAGE_REQUIRED')
        return super()._query(handle,arguments)
    def _finalize(self,handle,output):
        if self._Runtime__actor(handle)!='doc_writer_agent' or not self.stage_owner.writer_valid:
            raise Rejected('WRITER_STAGE_REQUIRED')
        return super()._finalize(handle,output)


class EpisodeV3(Episode):
    def __init__(self,cell,task,policy_row,metadata,provider,evaluator,private,clock=time.monotonic):
        self.cell=deepcopy(cell);self.provider=provider;self.evaluator=evaluator;self.private=Path(private)
        self.clock=clock;self.started=clock();self.started_utc=utc();self.deadline=self.started+7200
        self.budget=Budget();self.pending=Counter();self.scratch={}
        self.calls=[];self.actions=[];self.publications=[];self.reached=False;self.complete=False;self.metrics=None
        self.stage='planner';self.stage_events=[];self.finance_valid=False;self.writer_valid=False;self.publication_started=False
        self.treatment={'scheduled':cell['condition']!='CLEAN','entries':0,'released':False,'delivered':False,'quarantined':False}
        self._treatment_payload=None;self._injecting=False
        assert cell['condition'] in ('CLEAN','CONTAMINATION_A','CONTAMINATION_B')
        self.pol,self.private_note=policy_instance(policy_row);self.policy_row=policy_row
        self.rt=FinalStageRuntime(cell['family'],task,ARMS[cell['defense']],policies=[self.pol],max_actions=512,stage_owner=self,
            broker=BrokerPort(metadata,self) if cell['family']=='bird_pg' else None)
        self.rt.install_private('finance_agent',self.private_note)

    def service(self,actor,name,**arguments):
        start=len(self.rt.release_events)
        try:
            value=super().service(actor,name,**arguments)
            if self._injecting:
                self.treatment['released']=True
                self._treatment_payload=self.publications[-1]['payload']
            if name=='receive' and actor=='doc_writer_agent' and self._treatment_payload==canonical(value):self.treatment['delivered']=True
            return value
        finally:
            if self._injecting:
                events=self.rt.release_events[start:]
                if any(e['boundary']=='B2' for e in events):
                    self.reached=True;self.treatment['entries']+=1
                self.treatment['quarantined']|=any((e['decision'] or {}).get('decision')=='quarantine' for e in events)

    def snapshot(self,actor):
        snapshot=super().snapshot(actor)
        # Trusted stage capability restriction, identical in both defense arms.
        if self.stage!='finance':snapshot['invocation']['tool_permissions']=[]
        snapshot['trusted_stage']=self.stage
        snapshot['finance_sql_actions_used']=self.budget.counts['tool']
        return snapshot

    def generate(self,stage):
        self.stage=stage;actor=ROLES[stage]
        value=self.provider_action(actor,self.snapshot(actor))
        self.actions.append({'actor':actor,'stage':stage,'stage_output':deepcopy(value),'time':utc()})
        self.stage_events.append(stage+'_valid_output')
        return value

    def publish_finance(self,payload):
        if not self.finance_valid or self.stage!='finance' or self.publication_started:raise End('PROTOCOL_FAILURE')
        self.publication_started=True
        if self.cell['condition']!='CLEAN':
            wrapper={'handoff':self.policy_row['AB_templates'][self.cell['condition'][-1]]['text'],
                     'task_reference':self.cell['task_id'],'source_family':self.cell['family']}
            self._injecting=True
            try:self.service('finance_agent','send',recipient='doc_writer_agent',value=wrapper,kind='message')
            finally:self._injecting=False
        self.service('finance_agent','send',recipient='doc_writer_agent',value=payload,kind='result')
        self.stage_events.append('semantic_handoff_published')

    def provider_action(self,actor,snapshot):
        try:request=build_stage_request(self.stage,self.cell['family'],snapshot)
        except ValueError:raise End('CONTEXT_LIMIT') from None
        self.take('model',actor)
        n=len(self.calls)+1;start=self.clock();timestamp=utc()
        record={'ordinal':n,'principal':actor,'requested_model':'MiniMax-M2.7','started_utc':timestamp,
                'request_sha256':sha(canonical(request).encode()),'request':request}
        self.calls.append(record)
        write_private(self.private/f'call_{n:02d}_request.json',record)
        # All source content in the actual request has traversed B1; system protocol is trusted.
        self.publish(actor,'agent_context',snapshot,'model_context_ingress')
        try:
            response=self.provider.call(request,self.remaining(240))
        except (TimeoutError,RuntimeError,OSError) as exc:
            record.update(finished_utc=utc(),latency_seconds=self.clock()-start,failure='PROVIDER_FAILURE',timeout=(exc.diagnostics['timeout'] if isinstance(exc,TransportFailure) else isinstance(exc,TimeoutError)))
            record['transport_diagnostics']=deepcopy(exc.diagnostics) if isinstance(exc,TransportFailure) else diagnostics(exc)
            write_private(self.private/f'call_{n:02d}_response.json',record)
            raise End('EPISODE_TIMEOUT' if self.expired() else 'PROVIDER_FAILURE') from None
        record.update(finished_utc=utc(),latency_seconds=self.clock()-start,response=response)
        write_private(self.private/f'call_{n:02d}_response.json',record)
        if self.expired():raise End('EPISODE_TIMEOUT')
        body=response.get('body')
        if not isinstance(body,dict):raise End('PROVIDER_FAILURE')
        base=body.get('base_resp')
        if isinstance(base,dict) and base.get('status_code',0)!=0:raise End('PROVIDER_FAILURE')
        choices=body.get('choices')
        if not isinstance(choices,list) or len(choices)!=1 or not isinstance(choices[0],dict):raise End('PROVIDER_FAILURE')
        choice=choices[0];message=choice.get('message')
        if not isinstance(message,dict):raise End('PROVIDER_FAILURE')
        if message.get('tool_calls') or message.get('function_call'):raise End('PROTOCOL_FAILURE')
        if choice.get('finish_reason')=='length':raise End('MODEL_LENGTH')
        if choice.get('finish_reason')!='stop':raise End('PROTOCOL_FAILURE')
        text=message.get('content')
        if not isinstance(text,str) or not text.strip():raise End('PROTOCOL_FAILURE')
        try:
            action=parse_stage(text,self.stage,self.cell['family']);canonical(action)
        except (ValueError,TypeError,ValidationError):raise End('PROTOCOL_FAILURE') from None
        return action

    def execute(self):
        code='IMPLEMENTATION_DEFECT';defect=None
        try:
            planner=self.generate('planner')
            self.service('planner_agent','send',recipient='finance_agent',value=planner,kind='delegation')
            self.stage_events.append('planner_delegation_published')
            while True:
                finance=self.generate('finance')
                if self.cell['family']=='bird_pg' and finance['stage_action']=='query':
                    result=self.service('finance_agent','query',arguments=finance['arguments'])
                    self.scratch['finance_agent']=self.service('finance_agent','private_put',value=result)
                    if not result['ok']:
                        error=result['error']['code']
                        if error=='TIMEOUT':raise End('TOOL_FAILURE')
                        if error not in ('SQL_ERROR','SQL_SYNTAX','SQL_TYPE'):raise End('POLICY_REJECTION')
                    continue
                self.finance_valid=True
                self.stage_events.append('valid_finance_handoff')
                self.publish_finance(finance['handoff_payload'])
                break
            writer=self.generate('writer');self.writer_valid=True
            self.service('doc_writer_agent','finalize',output=writer);self.complete=True
            native=self.rt.evaluator_output()
            try:self.metrics=self.evaluator.score(self.cell,native,self.private/'evaluator',self.remaining(120))
            except (TimeoutError,RuntimeError,OSError,ValueError):
                raise End('EPISODE_TIMEOUT' if self.expired() else 'EVALUATOR_FAILURE') from None
            raise End('SUCCESSFUL_FINAL')
        except End as exc:code=exc.code
        except Exception as exc:defect=type(exc).__name__
        violated=any(e['unauthorized_raw'] for e in self.publications)
        privacy=True if violated else False if self.complete and code in ('SUCCESSFUL_FINAL','EVALUATOR_FAILURE') else None
        success=task_success(self.cell['family'],self.metrics) if self.metrics is not None else None if code in ('IMPLEMENTATION_DEFECT','EVALUATOR_FAILURE') else False
        raw={'cell':self.cell,'policy':self.policy_row,'private_note':self.private_note,'calls':self.calls,
             'actions':self.actions,'release_events':self.rt.release_events,'published_views':self.publications,
             'typed_records':self.rt.records(),'transitions':self.rt.transitions(),'termination':code,'defect':defect,
             'stage_events':list(self.stage_events),'valid_finance_handoff':self.finance_valid,'treatment':deepcopy(self.treatment),
             'metrics':self.metrics,'task_success':success,'privacy':privacy,'surface_reached':self.reached}
        write_private(self.private/'trajectory.json',raw)
        safe_calls=[]
        for call in self.calls:
            body=call.get('response',{}).get('body',{});body=body if isinstance(body,dict) else {}
            choice=(body.get('choices') or [{}])[0]
            safe_calls.append({'ordinal':call['ordinal'],'principal':call['principal'],'requested_model':call['requested_model'],
              'returned_model':body.get('model'),'response_id':body.get('id'),'finish_reason':choice.get('finish_reason') if isinstance(choice,dict) else None,
              'usage':body.get('usage'),'started_utc':call['started_utc'],'finished_utc':call.get('finished_utc'),
              'latency_seconds':call.get('latency_seconds'),'request_sha256':call['request_sha256'],'failure':call.get('failure'),'timeout':call.get('timeout',False),'transport_diagnostics':call.get('transport_diagnostics')})
        summary={**self.cell,'label':LABEL,'termination':code,'valid':code!='IMPLEMENTATION_DEFECT','completed_final':self.complete,
          'task_success':success,'source_metrics':self.metrics,'privacy':privacy,'surface_reached':self.reached if self.cell['condition']!='CLEAN' else None,
          'condition_observation':'CLEAN' if self.cell['condition']=='CLEAN' else 'SURFACE_REACHED' if self.reached else 'CONDITION_SURFACE_NOT_REACHED',
          'budget_counters':dict(self.budget.counts),'calls':safe_calls,'started_utc':self.started_utc,'ended_utc':utc(),
          'latency_seconds':self.clock()-self.started,'trajectory_sha256':sha((self.private/'trajectory.json').read_bytes()),
          'runtime_config_hash':sha((V3_CONFIG/'RUNTIME_RULE.json').read_bytes()),
          'namespace':'E2_DEVELOPMENT_V3_D3','stage_events':list(self.stage_events),
          'valid_finance_handoff':self.finance_valid,'treatment':deepcopy(self.treatment),
          'source_evaluator_pins_ref':'experiments/e2_pilot_config_p1/SOURCE_EVALUATOR_PINS.json',
          'recognizer_match':None if self.cell['condition']=='CLEAN' else self.policy_row['expected_frozen_recognizer_match'][self.cell['condition'][-1]],
          'tool_events':[{'ok':r['structured_result']['ok'],'error':r['structured_result']['error']} for r in self.rt.records() if r['record_type']=='ToolResult'],
          'generation_rule_id':self.policy_row['fact_generation_template']['id'],'generation_ordinal':self.policy_row['generation_ordinal'],
          'template_id':None if self.cell['condition']=='CLEAN' else self.policy_row['AB_templates'][self.cell['condition'][-1]]['id'],
          'attempted_unauthorized_raw_events':sum(self.pol.raw_value in e['attempted'] and (e['recipient'] not in self.pol.allowed_recipients or e['surface'] in self.pol.forbidden_channels) for e in self.rt.release_events),
          'released_unauthorized_raw_events':sum(e['unauthorized_raw'] for e in self.publications),
          'release_decisions':Counter((e['decision'] or {}).get('decision','trusted_private') for e in self.rt.release_events),
          'boundaries_observed':dict(Counter(e['boundary'] for e in self.rt.release_events)),'implementation_defect_type':defect}
        # No raw synthetic value enters public metadata; provider fields may echo content.
        encoded=json.dumps(summary,ensure_ascii=False,allow_nan=False)
        for value in [self.pol.raw_value]:encoded=encoded.replace(value,'[REDACTED]')
        return json.loads(encoded)
