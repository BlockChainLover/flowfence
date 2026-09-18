"""Non-model deterministic interface prototype; trusted services, JSON actions only.

No Python sandbox, provider, external connector, or evaluator reference access.
"""
import json
from copy import deepcopy
from src.defenses.mas_flowfence import inspect_mas_event
from src.e2_s1.frozen_r2 import inspect_r2_event
from src.runtime.topology import Topology

PRINCIPALS=('planner_agent','finance_agent','doc_writer_agent')
BOUNDARIES={
 'T01':('B1','B3'), 'T02':(), 'T03':('B1',), 'T04':('B1',),
 'T05':('B2','B1'), 'T06':('B2','B3','B4'), 'T07':('B2','B3','B1'),
 'T08':('B2',), 'T09':('B2','B1'), 'T10':('B2','B3','B1'), 'T11':('B1',),
 'T12':('B3','B1'), 'T13':('B3',), 'T14':('B3','B7'), 'T15':('B3','B4'),
 'T16':('B5','B3','B1'), 'T17':('B5','B1'), 'T18':('B4','B6'),
 'T19':('B6','B3'), 'T20':('B1','B2','B3'), 'T21':('B7',), 'T22':('B7',), 'T23':()}

class Rejected(Exception):
    pass

class InterfaceRuntime:
    """All emitted values are detached. Runtime does not accept gold/evaluator stores."""
    def __init__(self, family, release_mode, policies=()):
        if release_mode not in ('ifc_safeview','flowfence_lite_nonoracle_r2'):
            raise ValueError('Unsupported frozen arm')
        self.family=family; self.mode=release_mode;self.policies=deepcopy(list(policies))
        self.__handles={p:object() for p in PRINCIPALS}
        self.__state={};self.__private={p:None for p in PRINCIPALS};self.__pending={}
        self.__proposal_counter=0;self.__revision=0;self.__queue=[];self.__final=None;self.audit=[]
        self.topology=Topology('e2_fixed', {p:set(PRINCIPALS)-{p} for p in PRINCIPALS})
    def handle(self, principal):
        return self.__handles[principal]
    def configuration(self):
        return {'principals':PRINCIPALS,'routing':'FIFO; all directed internal edges',
                'family':self.family,'tools':['readonly_sql'] if self.family=='bird_pg' else [],
                'state_api':['read','prepare','commit','private'], 'failure':'typed rejection; no automatic retry',
                'model_budget':0,'evaluator':'separate original scorer','roles':'one coordinator, two generic workers'}
    def identity(self, handle):
        for p,h in self.__handles.items():
            if h is handle:return p
        raise Rejected('unauthorized_handle')
    def install_private(self, principal, value):
        # Trusted initialization; deliberately absent from dispatch/action grammar.
        self.__private[principal]=deepcopy(value)
    def release(self,boundary,actor,recipient,payload):
        surface='final_output' if boundary=='B7' else ('internal_message' if boundary in ('B1','B2') else 'shared_raw')
        content=json.dumps(payload,ensure_ascii=False,sort_keys=True)
        kwargs=dict(defense_mode=self.mode,event_type='runtime_release',actor_id=actor,recipient_id=recipient,
                    channel=surface,target_zone=surface,content=content,topology=self.topology,
                    secret_policies=self.policies,attack_annotation=None)
        self.audit.append({'boundary':boundary,'actor':actor,'recipient':recipient,'surface':surface})
        result=inspect_r2_event(**kwargs)
        if result.decision['decision']=='block':raise Rejected('blocked')
        try:return json.loads(result.content)
        except (ValueError,TypeError):raise Rejected('invalid_released_json')
    def dispatch(self,handle,transition,payload=None,*,recipient=None,revision=None):
        actor=self.identity(handle)
        if transition not in BOUNDARIES or transition in ('T02','T23'):raise Rejected('trusted_or_unknown_transition')
        recipient=recipient or actor
        if recipient not in PRINCIPALS:raise Rejected('unknown_recipient')
        if transition=='T11':
            if recipient!=actor:raise Rejected('private_owner')
            payload=deepcopy(self.__private[actor])
        if transition=='T12':
            if revision!=self.__revision:raise Rejected('stale_revision')
            payload=deepcopy(self.__state)
        if transition=='T09':
            if not self.__queue or self.__queue[0][0]!=actor:raise Rejected('empty_or_wrong_delivery')
            payload=deepcopy(self.__queue[0][1])
        if transition=='T19':
            if revision!=self.__revision:raise Rejected('stale_revision')
            key=payload
            if key not in self.__pending or self.__pending[key][0]!=actor:raise Rejected('unknown_proposal')
            payload=deepcopy(self.__pending[key][1])
        value=deepcopy(payload)
        for boundary in BOUNDARIES[transition]:value=self.release(boundary,actor,recipient,value)
        if transition in ('T01','T13'):
            # Publication prepares an atomic state replacement; commit is separately mediated.
            if not isinstance(value,dict):raise Rejected('invalid_state')
            self.__proposal_counter+=1;key=self.__proposal_counter;self.__pending[key]=(actor,deepcopy(value));return key
        if transition=='T18':
            if not isinstance(value,dict):raise Rejected('invalid_effect')
            self.__proposal_counter+=1;key=self.__proposal_counter;self.__pending[key]=(actor,deepcopy(value));return key
        if transition=='T19':
            if not isinstance(value,dict):raise Rejected('invalid_state')
            self.__state=deepcopy(value);self.__revision+=1;del self.__pending[key]
        if transition in ('T05','T08','T10'):self.__queue.append((recipient,deepcopy(value)))
        if transition=='T09':self.__queue.pop(0)
        if transition in ('T14','T21','T22'):self.__final=deepcopy(value)
        return deepcopy(value)
    def evaluator_output(self):
        # Trusted outgoing port; it accepts no evaluator-private input.
        return deepcopy(self.__final)
