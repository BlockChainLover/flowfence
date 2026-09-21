"""C0 offline-only lossless serialization candidate; not bound to any live runner."""
from copy import deepcopy
from src.e2_live.pilot import canonical,load,CONFIG
from src.e2_live.v3 import V3_CONFIG,stage_schema

FORMAT='BIRD_RELEASED_CONTEXT_SINGLE_COPY_V1'


def messages(stage,snapshot):
    text=(V3_CONFIG/'prompts/common.txt').read_text()+'\n'+(V3_CONFIG/f'prompts/{stage}.txt').read_text()
    text+='\nSTAGE_SCHEMA\n'+canonical(stage_schema(stage,'bird_pg'))
    if stage=='finance':text+='\nREADONLY_SQL_CONTRACT\n'+canonical(load(CONFIG/'FAMILY_PROFILES.json')['bird_pg']['tools'][0]['arguments'])
    return [{'role':'system','content':text},{'role':'user','content':canonical(snapshot)}]


def wire_bytes(stage,snapshot):return len(canonical(messages(stage,snapshot)).encode('utf-8'))
def size(value):return len(canonical(value).encode('utf-8'))


def pack(snapshot):
    """Intern only byte-identical, already released top-level context values.

    Per-invocation pool; no runtime/state/provider access and no external lookup.
    Header and occurrence order remain intact. No semantic or provenance field is dropped.
    """
    header=deepcopy({k:v for k,v in snapshot.items() if k not in ('values','history')})
    pool=[];positions={}
    def ref(value):
        key=canonical(value)
        if key not in positions:
            positions[key]=len(pool);pool.append(deepcopy(value))
        return positions[key]
    return {'representation':FORMAT,'header':header,'released_value_pool':pool,
            'values_pool_indices':[ref(v) for v in snapshot['values']],
            'history_pool_indices':[ref(v) for v in snapshot['history']]}


def unpack(packet):
    if set(packet)!={'representation','header','released_value_pool','values_pool_indices','history_pool_indices'} or packet['representation']!=FORMAT:raise ValueError('FORMAT')
    pool=packet['released_value_pool']
    def value(index):
        if type(index) is not int or not 0<=index<len(pool):raise ValueError('UNRELEASED_REFERENCE')
        return deepcopy(pool[index])
    result=deepcopy(packet['header'])
    if 'values' in result or 'history' in result:raise ValueError('HEADER_COLLISION')
    result['values']=[value(i) for i in packet['values_pool_indices']]
    result['history']=[value(i) for i in packet['history_pool_indices']]
    return result


def semantic_items(snapshot):
    return sorted({canonical(v) for v in snapshot['values']+snapshot['history']})


def duplicate_stats(snapshot):
    seen=set();duplicate=0;occurrences=0
    for value in snapshot['values']+snapshot['history']:
        key=canonical(value)
        if key in seen:duplicate+=len(key.encode());occurrences+=1
        seen.add(key)
    return {'duplicate_value_occurrences':occurrences,'duplicate_value_json_bytes':duplicate,'unique_released_values':len(seen)}
