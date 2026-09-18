"""Deterministic trusted-services runtime. No provider or arbitrary-code capability.

Model-side capabilities are bound Session methods / JSON proposals. Python reflection,
malicious trusted services and OS/timing channels are outside the declared threat model.
"""
from dataclasses import dataclass, asdict
from copy import deepcopy
import json
from src.e2_s1.frozen_r2 import inspect_r2_event
from src.runtime.topology import Topology
from src.e2_s1.adapters import source_output

PRINCIPALS=('planner_agent','finance_agent','doc_writer_agent')
REGISTERED_RECIPIENTS=PRINCIPALS+('readonly_sql',)

class Rejected(Exception):pass

def wire(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,allow_nan=False)

def detached(value):return json.loads(wire(value))

@dataclass(frozen=True)
class Envelope:
    artifact_id:str
    producer_principal:str
    owner_principal:str
    task_family_id:str
    category:str
    payload_json:str
    parent_artifacts:tuple
    audience:tuple
    surface:str
    tool_identity:str|None
    authorization:tuple

@dataclass(frozen=True)
class Object:
    kind:str
    owner:str
    audience:tuple
    revision:int
    artifact:Envelope

@dataclass(frozen=True)
class Proposal:
    actor:str
    object_id:str
    base_revision:int
    artifact:Envelope
    audience:tuple

class Runtime:
    def __init__(self,family,task,arm,*,broker=None,policies=(),max_actions=1000):
        if family not in ('bird_pg','tatqa','hotpot'):raise ValueError('family')
        if arm not in ('ifc_safeview','flowfence_lite_nonoracle_r2'):raise ValueError('arm')
        self.__family=family;self.__arm=arm;self.__task=detached(task);self.__broker=broker
        self.__policies=deepcopy(list(policies));self.__max_actions=max_actions;self.__actions=0
        self.__handles={p:object() for p in PRINCIPALS};self.__objects={};self.__object_ids={};self.__proposals={}
        self.__messages={p:[] for p in PRINCIPALS};self.__histories={p:[] for p in PRINCIPALS}
        self.__counter=0;self.__stopped=False;self.__final=None;self.__audit=[];self.__transitions=[]
        self.__records=[];self.__last_tool_result=None;self.__visible={p:set() for p in PRINCIPALS}
        self.__topology=Topology('e2_fixed',{p:set(PRINCIPALS)-{p} for p in PRINCIPALS})
        a=self.__make('runtime','TASK_STATE',task,PRINCIPALS,'shared_raw')
        a=self.__release_all(a,'B3');a=self.__release_all(a,'B6')
        self.__objects['task']=Object('task_state','runtime',PRINCIPALS,0,a)
        self.__mark('T01');self.__record_state('task')
    def session(self,principal):
        """Trusted launcher issues capabilities; never exposed in actor JSON grammar."""
        return Session(self,self.__handles[principal])
    def configuration(self):
        return {'principals':list(PRINCIPALS),'family':self.__family,'graph':{p:sorted(set(PRINCIPALS)-{p}) for p in PRINCIPALS},
          'tools':['readonly_sql'] if self.__family=='bird_pg' else [],'budget':self.__max_actions,
          'scheduling':'FIFO','retry':'explicit bounded action; no uncertain external retry','evaluator':'trusted outgoing port only',
          'provider':'minimax','model_profile':'NON_GENERATING_CERTIFICATION','role_template':'coordinator and two generic workers'}
    def audit(self,include_payload=False):return detached(self.__audit if include_payload else [{k:v for k,v in e.items() if k!='payload_json'} for e in self.__audit])
    def transitions(self):return list(self.__transitions)
    def records(self):return detached(self.__records)
    def __mark(self,t):self.__transitions.append(t)
    def __id(self,prefix):self.__counter+=1;return f'{prefix}{self.__counter}'
    def __auth(self,actor):
        permissions=(['source_read','message','own_state','final'] if actor in PRINCIPALS else ['execute_source_select','publish_result'] if actor=='readonly_sql' else ['initialize_task'] if actor=='runtime' else None)
        if permissions is None:raise Rejected('UNREGISTERED_PRODUCER')
        return {'issued_by':'runtime','grant_id':'grant:'+actor,'principal':actor,'permissions':permissions}
    def __actor(self,handle):
        for p,h in self.__handles.items():
            if h is handle:return p
        raise Rejected('UNAUTHORIZED_HANDLE')
    def __check(self,h):
        actor=self.__actor(h)
        if self.__stopped:raise Rejected('STOPPED')
        if self.__actions>=self.__max_actions:
            self.__terminate(actor,'budget');raise Rejected('BUDGET')
        self.__actions+=1;return actor
    def __make(self,producer,category,value,audience,surface,parents=(),tool=None):
        if category not in ('TASK_STATE','RUNTIME_SHARED','TOOL_RUNTIME','TRUSTED_PRIVATE'):raise Rejected('PRIVATE_PROVENANCE_DENIED')
        if not audience or any(p not in REGISTERED_RECIPIENTS for p in audience):raise Rejected('AUDIENCE')
        if category=='RUNTIME_SHARED' and producer in self.__visible:parents=tuple(sorted(set(parents)|self.__visible[producer]))
        art=Envelope(self.__id('artifact:'),producer,producer,self.__family,category,wire(value),tuple(parents),tuple(audience),surface,tool,tuple(self.__auth(producer)['permissions']))
        self.__records.append({'record_type':'ArtifactRecord','artifact':{'artifact_id':art.artifact_id,'producer_principal':producer,'owner_principal':producer,'task_family_id':self.__family,'category':category,'payload_ref':art.artifact_id+':payload','parent_artifacts':list(parents),'audience':list(audience)}})
        return art
    def __release(self,a,recipient,boundary):
        if recipient not in a.audience:raise Rejected('AUDIENCE')
        surface='final_output' if boundary=='B7' else a.surface
        self.__audit.append({'boundary':boundary,'artifact':a.artifact_id,'producer':a.producer_principal,'recipient':recipient,'category':a.category,'surface':surface,'tool':a.tool_identity,'authorization':list(a.authorization),'parents':list(a.parent_artifacts),'payload_json':a.payload_json})
        # Authorized private initialization is trusted self-context, not an untrusted publication.
        if a.category=='TRUSTED_PRIVATE' and boundary in ('B1','B3') and recipient==a.owner_principal:
            if boundary=='B1':self.__visible[recipient].add(a.artifact_id)
            return a
        result=inspect_r2_event(defense_mode=self.__arm,event_type='runtime_release',actor_id=a.producer_principal,
          recipient_id=recipient,channel=surface,target_zone=surface,content=a.payload_json,
          topology=self.__topology,secret_policies=self.__policies,attack_annotation=None)
        if result.decision['decision']=='block':raise Rejected('RELEASE_BLOCKED')
        try:value=json.loads(result.content);wire(value)
        except (ValueError,TypeError):raise Rejected('INVALID_RELEASE') from None
        released=a if wire(value)==a.payload_json else self.__make(a.producer_principal,'RUNTIME_SHARED' if a.category=='TRUSTED_PRIVATE' else a.category,value,a.audience,a.surface,parents=(a.artifact_id,),tool=a.tool_identity)
        if boundary=='B1' and recipient in self.__visible:self.__visible[recipient].add(released.artifact_id)
        return released
    def __release_all(self,a,boundary):
        for recipient in a.audience:a=self.__release(a,recipient,boundary)
        return a
    def __record_state(self,key):
        o=self.__objects[key]
        self.__records.append({'record_type':'StateObject','object_id':self.__object_ids.setdefault(key,self.__id('object:')),'kind':{'task_state':'TASK_STATE','private_memory':'PRIVATE_MEMORY','shared_artifact':'SHARED_ARTIFACT','final_output':'SHARED_ARTIFACT'}[o.kind],'owner_principal':o.owner,'audience':list(o.audience),'revision':o.revision,'artifact_ref':o.artifact.artifact_id})
    def install_private(self,principal,value):
        """Trusted setup port, absent from actor API and action grammar."""
        if principal not in PRINCIPALS:raise Rejected('PRINCIPAL')
        if self.__actions:raise Rejected('INITIALIZATION_CLOSED')
        a=self.__make(principal,'TRUSTED_PRIVATE',value,[principal],'internal_message')
        self.__objects['private:'+principal]=Object('private_memory',principal,(principal,),0,a);self.__mark('T02');self.__record_state('private:'+principal)
    def _context(self,h,keys=('task',)):
        actor=self.__check(h);values=[];parts=[]
        for key in keys:
            o=self.__objects.get(key)
            if o is None or actor not in o.audience:raise Rejected('UNAUTHORIZED_READ')
            a=self.__release(o.artifact,actor,'B1');values.append(json.loads(a.payload_json))
            parts.append({'artifact_ref':a.artifact_id,'category':a.category,'source_principal':a.producer_principal,'provenance_ref':a.artifact_id})
        envelope={'record_type':'ModelInvocation','recipient_principal':actor,'sender_principal':None,'authorization_context':self.__auth(actor),'task_family_id':self.__family,'tool_permissions':self.configuration()['tools'],'provider':'minimax','model_profile_ref':'NON_GENERATING_CERTIFICATION','context':parts}
        self.__records.append(envelope);self.__mark('T03');return {'invocation':detached(envelope),'values':values}
    def _invoke(self,h,keys=('task',),*,mock_error=False):
        value=self._context(h,keys);self.__mark('T04')
        if mock_error:
            self.__mark('T20');raise Rejected('MOCK_MODEL_ERROR')
        return value  # No provider or arbitrary callback can receive hidden state.
    def _private_put(self,h,value):
        actor=self.__check(h);key='scratch:'+actor;a=self.__make(actor,'RUNTIME_SHARED',value,[actor],'internal_message')
        self.__objects[key]=Object('private_memory',actor,(actor,),self.__objects[key].revision+1 if key in self.__objects else 0,a);self.__mark('T11');self.__record_state(key);return key
    def _read(self,h,key,revision):
        actor=self.__check(h);o=self.__objects.get(key)
        if o is None or actor not in o.audience:raise Rejected('UNAUTHORIZED_READ')
        if revision!=o.revision:raise Rejected('STALE_READ')
        self.__records.append({'record_type':'StateRead','actor_principal':actor,'object_id':self.__object_ids.setdefault(key,self.__id('object:')),'expected_revision':revision,'purpose':'source_task','authorization_context':self.__auth(actor)})
        a=self.__release(o.artifact,actor,'B3');a=self.__release(a,actor,'B1');self.__mark('T11' if o.kind=='private_memory' else 'T12');return {'revision':o.revision,'value':json.loads(a.payload_json)}
    def _prepare(self,h,key,revision,operations,audience):
        actor=self.__check(h)
        if not audience or any(p not in PRINCIPALS for p in audience):raise Rejected('AUDIENCE')
        if not isinstance(key,str) or not key.startswith('shared:'):raise Rejected('STATE_NAMESPACE')
        # User-defined object keys are carried in the released payload, never trusted metadata IDs.
        current=self.__objects.get(key)
        if current and current.owner!=actor:raise Rejected('UNAUTHORIZED_WRITE')
        if (current.revision if current else 0)!=revision:raise Rejected('STALE_WRITE')
        value=json.loads(current.artifact.payload_json)['data'] if current else {}
        if not isinstance(value,dict):raise Rejected('STATE_SCHEMA')
        for op in detached(operations):
            if set(op)-{'op','key','value'} or op.get('op') not in ('set','delete') or not isinstance(op.get('key'),str):raise Rejected('OPERATION_SCHEMA')
            if set(op)!=({'op','key','value'} if op['op']=='set' else {'op','key'}):raise Rejected('OPERATION_SCHEMA')
            if op['op']=='set':value[op['key']]=op['value']
            else:value.pop(op['key'],None)
        a=self.__make(actor,'RUNTIME_SHARED',{'object_key':key,'data':value},audience,'shared_raw',parents=[current.artifact.artifact_id] if current else [])
        a=self.__release_all(a,'B3');a=self.__release_all(a,'B4');a=self.__release_all(a,'B6')
        released=json.loads(a.payload_json)
        if not isinstance(released,dict) or released.get('object_key')!=key or not isinstance(released.get('data'),dict):raise Rejected('INVALID_RELEASE_SCHEMA')
        pid=self.__id('proposal:');self.__proposals[pid]=Proposal(actor,key,revision,a,tuple(audience));self.__mark('T13');self.__mark('T18')
        self.__records.append({'record_type':'StateProposal','proposal_id':pid,'actor_principal':actor,'object_id':self.__object_ids.setdefault(key,self.__id('object:')),'base_revision':max(0,revision),'operations':[{'op':'set','path':[],'value_ref':a.artifact_id+':payload'}],'audience':list(audience),'parent_artifacts':list(a.parent_artifacts),'authorization_context':self.__auth(actor)})
        self.__records.append({'record_type':'PreparedEffect','effect_id':pid+':effect','call_id':pid,'actor_principal':actor,'sink_principal':'state_service','effect_kind':'atomic_state_replace','complete_request_ref':a.artifact_id+':payload','affected_state_refs':[self.__object_ids[key]],'audience':list(audience),'retry_class':'NEVER','authorization_context':self.__auth(actor)})
        return pid
    def _commit(self,h,pid):
        actor=self.__check(h);p=self.__proposals.get(pid)
        if p is None or p.actor!=actor:raise Rejected('UNAUTHORIZED_PROPOSAL')
        current=self.__objects.get(p.object_id)
        if (current.revision if current else 0)!=p.base_revision:raise Rejected('STALE_WRITE')
        a=self.__release_all(p.artifact,'B6');a=self.__release_all(a,'B3');v=json.loads(a.payload_json)
        if v.get('object_key')!=p.object_id or not isinstance(v.get('data'),dict):raise Rejected('INVALID_RELEASE_SCHEMA')
        self.__objects[p.object_id]=Object('shared_artifact',actor,p.audience,p.base_revision+1,a);del self.__proposals[pid];self.__mark('T19');self.__record_state(p.object_id);return p.base_revision+1
    def _send(self,h,recipient,value,kind='message'):
        actor=self.__check(h)
        if recipient not in PRINCIPALS or recipient==actor:raise Rejected('ROUTE')
        if kind not in ('message','delegation','summary','result','next_step'):raise Rejected('MESSAGE_KIND')
        a=self.__make(actor,'RUNTIME_SHARED',value,[recipient],'internal_message')
        a=self.__release(a,recipient,'B2');a=self.__release(a,recipient,'B3');a=self.__release(a,recipient,'B6')
        self.__messages[recipient].append(a);self.__mark({'message':'T08','delegation':'T05','summary':'T07','result':'T10','next_step':'T06'}[kind]);return a.artifact_id
    def _receive(self,h):
        actor=self.__check(h)
        if not self.__messages[actor]:raise Rejected('EMPTY_QUEUE')
        a=self.__messages[actor][0];a=self.__release(a,actor,'B2');a=self.__release(a,actor,'B1');a=self.__release(a,actor,'B3');a=self.__release(a,actor,'B6')
        self.__messages[actor].pop(0);self.__histories[actor].append(a);self.__mark('T09');return json.loads(a.payload_json)
    def _history(self,h):
        actor=self.__check(h);out=[]
        for a in self.__histories[actor]:out.append(json.loads(self.__release(self.__release(a,actor,'B3'),actor,'B1').payload_json))
        self.__mark('T12');return out
    def _query(self,h,arguments):
        actor=self.__check(h)
        if self.__family!='bird_pg' or self.__broker is None:raise Rejected('TOOL_UNAVAILABLE')
        a=self.__make(actor,'RUNTIME_SHARED',arguments,[actor,'readonly_sql'],'shared_raw',tool='readonly_sql')
        a=self.__release(a,actor,'B3');a=self.__release(a,'readonly_sql','B4');args=json.loads(a.payload_json)
        if not isinstance(args,dict) or set(args)!={'sql'} or not isinstance(args['sql'],str):raise Rejected('ARGUMENT_SCHEMA')
        call=self.__id('call:');self.__mark('T15')
        self.__records.append({'record_type':'ToolCall','call_id':call,'calling_principal':actor,'tool_name':'readonly_sql','arguments_ref':a.artifact_id+':payload','argument_schema_ref':'sql_string_only','authorization_context':self.__auth(actor),'state_reads':['task'],'state_writes':[],'external_effect_kinds':[],'result_audience':[actor],'publication_target':'tool_result','structured_arguments':args})
        # Broker is a trusted read-only computation returning a detached private draft.
        draft=self.__broker.execute(self.__task['db_id'],args)
        result=self.__make('readonly_sql','TOOL_RUNTIME',draft,[actor],'shared_raw',parents=[a.artifact_id],tool='readonly_sql')
        result=self.__release(result,actor,'B5');result=self.__release(result,actor,'B3');result=self.__release(result,actor,'B6');result=self.__release(result,actor,'B1')
        released=json.loads(result.payload_json)
        if not isinstance(released,dict) or set(released)!={'ok','columns','rows','error'} or not isinstance(released['ok'],bool):raise Rejected('RESULT_SCHEMA')
        self.__histories[actor].append(result);self.__last_tool_result=result;self.__mark('T16' if released['ok'] else 'T17')
        error=None if released['ok'] else {'code':released['error']['code'],'message_ref':result.artifact_id+':payload','retry_class':released['error']['retry_class']}
        self.__records.append({'record_type':'ToolResult','call_id':call,'producing_tool':'readonly_sql','payload_ref':result.artifact_id+':payload','state_proposal_refs':[],'prepared_effect_refs':[],'result_audience':[actor],'error':error,'structured_result':released})
        return detached(released)
    def _finalize(self,h,output):
        actor=self.__check(h);a=self.__make(actor,'RUNTIME_SHARED',output,PRINCIPALS,'final_output')
        a=self.__release_all(a,'B7');released=json.loads(a.payload_json)
        # Strict native schema check is common to both arms, never a task-specific repair.
        if self.__family=='bird_pg':valid=isinstance(released,dict) and set(released)=={'sql'} and isinstance(released['sql'],str)
        elif self.__family=='tatqa':valid=isinstance(released,dict) and set(released)=={'answer','scale'} and isinstance(released['scale'],str) and all(type(x) in (str,int,float) for x in (released['answer'] if isinstance(released['answer'],list) else [released['answer']]))
        else:valid=isinstance(released,dict) and set(released)=={'answer','supporting_facts'} and isinstance(released['answer'],str) and isinstance(released['supporting_facts'],list) and all(isinstance(x,list) and len(x)==2 and isinstance(x[0],str) and type(x[1]) is int for x in released['supporting_facts'])
        if not valid:raise Rejected('FINAL_SCHEMA')
        source_output(self.__family,self.__task,released)
        self.__final=a;self.__objects['final']=Object('final_output',actor,PRINCIPALS,0,a);self.__mark('T22');return detached(released)
    def _export(self,h,key,revision):
        value=self._read(h,key,revision);actor=self.__actor(h)
        o=self.__objects[key];a=self.__release(o.artifact,actor,'B7');self.__mark('T14');return json.loads(a.payload_json)
    def __terminate(self,actor,reason):
        if reason not in ('normal','budget','error','protocol'):raise Rejected('TERMINATION_REASON')
        a=self.__make(actor,'RUNTIME_SHARED',{'stop':reason},PRINCIPALS,'final_output');self.__release_all(a,'B7');self.__stopped=True;self.__mark('T21')
    def _stop(self,h,reason):
        if self.__stopped:raise Rejected('STOPPED')
        self.__terminate(self.__actor(h),reason)
    def evaluator_output(self):
        """Trusted read-only outgoing port. No evaluator inputs/callbacks enter runtime."""
        if self.__final is None:raise Rejected('NO_FINAL')
        self.__mark('T23');return source_output(self.__family,self.__task,json.loads(self.__final.payload_json))
    def _propose(self,h,action):
        # Actor JSON cannot request category/provenance, tools results, evaluator input,
        # private initialization, diagnostics, shell, web, or arbitrary external effects.
        allowed={'read':('key','revision'),'send':('recipient','value','kind'),'query':('arguments',),'finalize':('output',),'prepare':('key','revision','operations','audience'),'commit':('pid',),'private_put':('value',),'context':('keys',),'invoke':('keys',),'receive':(),'history':(),'export':('key','revision'),'stop':('reason',)}
        name=action.get('action') if isinstance(action,dict) else None
        if name not in allowed or set(action)!={'action',*allowed[name]}:raise Rejected('ACTION_SCHEMA')
        self.__mark('T06')
        return getattr(self,'_'+name)(h,**{k:action[k] for k in allowed[name]})

class Session:
    __slots__=('__runtime','__handle')
    def __init__(self,runtime,handle):self.__runtime=runtime;self.__handle=handle
    def context(self,keys=('task',)):return self.__runtime._context(self.__handle,keys)
    def invoke(self,keys=('task',),mock_error=False):return self.__runtime._invoke(self.__handle,keys,mock_error=mock_error)
    def private_put(self,value):return self.__runtime._private_put(self.__handle,value)
    def read(self,key,revision):return self.__runtime._read(self.__handle,key,revision)
    def prepare(self,key,revision,operations,audience=PRINCIPALS):return self.__runtime._prepare(self.__handle,key,revision,operations,audience)
    def commit(self,pid):return self.__runtime._commit(self.__handle,pid)
    def send(self,recipient,value,kind='message'):return self.__runtime._send(self.__handle,recipient,value,kind)
    def receive(self):return self.__runtime._receive(self.__handle)
    def history(self):return self.__runtime._history(self.__handle)
    def query(self,arguments):return self.__runtime._query(self.__handle,arguments)
    def finalize(self,output):return self.__runtime._finalize(self.__handle,output)
    def export(self,key,revision):return self.__runtime._export(self.__handle,key,revision)
    def stop(self,reason='normal'):return self.__runtime._stop(self.__handle,reason)
    def propose(self,action):return self.__runtime._propose(self.__handle,action)
