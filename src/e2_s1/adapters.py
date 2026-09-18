"""Deterministic source serialization. No model client or private reference storage."""
from copy import deepcopy


def task_input(family, record, *, context=None, schema=None, descriptions=None):
    if family == 'bird_pg':
        if schema is None or descriptions is None:
            raise ValueError('Complete source schema and descriptions required')
        value = {k: record[k] for k in ('question_id', 'question', 'db_id', 'evidence')}
        value.update(schema=schema, descriptions=descriptions, capabilities=['readonly_sql'])
    elif family == 'tatqa':
        value = {k: record[k] for k in ('uid', 'order', 'question')}
        value.update(table=context['table'], paragraphs=context['paragraphs'], capabilities=[])
    elif family == 'hotpot':
        value = {'id': record['id'], 'question': record['question'], 'context': [
            {'title': title, 'sentences': [{'index': i, 'text': text} for i, text in enumerate(sentences)]}
            for title, sentences in zip(record['context']['title'], record['context']['sentences'], strict=True)], 'capabilities': []}
    else:
        raise ValueError('Unknown source family')
    return deepcopy(value)


def source_output(family, task, output):
    """Consume actual released output, never consult a reference answer."""
    if family == 'bird_pg':
        if not isinstance(output['sql'], str):
            raise TypeError('SQL must be text')
        return output['sql'] + '\t----- bird -----\t' + task['db_id']
    if family == 'tatqa':
        answer = output['answer']
        return {task['uid']: [deepcopy(answer if isinstance(answer, list) else [answer]), output['scale']]}
    if family == 'hotpot':
        return {'answer': {task['id']: output['answer']}, 'sp': {task['id']: deepcopy(output['supporting_facts'])}}
    raise ValueError('Unknown source family')


def hotpot_native(record):
    return {'_id': record['id'], 'question': record['question'], 'answer': record['answer'],
            'type': record['type'], 'level': record['level'],
            'context': [[t, deepcopy(s)] for t, s in zip(record['context']['title'], record['context']['sentences'], strict=True)],
            'supporting_facts': [[t, i] for t, i in zip(record['supporting_facts']['title'], record['supporting_facts']['sent_id'], strict=True)]}


def hotpot_mirror(native):
    return {'id': native['_id'], **{k: native[k] for k in ('question', 'answer', 'type', 'level')},
            'context': {'title': [x[0] for x in native['context']], 'sentences': deepcopy([x[1] for x in native['context']])},
            'supporting_facts': {'title': [x[0] for x in native['supporting_facts']], 'sent_id': [x[1] for x in native['supporting_facts']]}}
