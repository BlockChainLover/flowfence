"""R3 execution labels and episode-level aggregation over the frozen R2 path.

No override of source construction, prompts, mediation, workflow, parser,
verifier or reconstruction evaluator. Replicates never seed a provider RNG.
"""
from __future__ import annotations
import hashlib
import itertools
import json
from pathlib import Path
from src.experiments.aamas_binding_r2 import R2BindingEpisode
from src.defenses.mas_flowfence import contains_raw_secret, contains_sensitive_detail_request
from src.runtime.policy import default_secret_policies

CONDITIONS = ('clean', 'heldout_registered_A', 'heldout_registered_B')
DEFENSES = ('ifc_safeview', 'flowfence_lite_nonoracle_r2')
FROZEN = Path('artifacts/aamas2027/R3_FROZEN_INPUTS.json')


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def frozen_assertions():
    frozen = json.loads(FROZEN.read_text())
    for path, digest in frozen['files'].items():
        if sha256(Path(path).read_bytes()) != digest:
            raise ValueError('R3 frozen input changed: ' + path)
    return frozen


def schedule(config):
    """One pair per batch; rotate submission order by stable zero-based index."""
    pairs = []
    for index, (replicate, task, condition) in enumerate(itertools.product(
            config['replicate_ids'], config['task_ids'], config['conditions'])):
        order = config['defenses'] if index % 2 == 0 else list(reversed(config['defenses']))
        pairs.append([dict(task_id=task, topology='blackboard_4', condition=condition,
                           replicate_id=replicate, defense=defense, pair_index=index,
                           dispatch_position=position) for position, defense in enumerate(order)])
    return pairs


def run_id(cell):
    return (f"r3__formal__{cell['task_id']}__{cell['topology']}__{cell['condition']}"
            f"__{cell['defense']}__replicate{cell['replicate_id']}__attempt1")


def load_config(path):
    frozen = frozen_assertions()
    config = json.loads(Path(path).read_text())
    if sha256(Path(path).read_bytes()) != frozen['r3_config_sha256']:
        raise ValueError('R3 registered config changed')
    attack_path = Path(config['attack_file'])
    if sha256(attack_path.read_bytes()) != frozen['attack_file_sha256']:
        raise ValueError('R3 held-out attack config changed')
    attacks = json.loads(attack_path.read_text())
    profile = json.loads(Path(config['prompt_file']).read_text())
    prior = profile['attacks']
    for name in CONDITIONS[1:]:
        attack = attacks[name]
        assert not contains_raw_secret(attack, default_secret_policies())
        assert contains_sensitive_detail_request(attack)
        assert attack not in prior.values()
        assert sha256(attack.encode()) == frozen['attack_hashes'][name]
    assert list(attacks) == list(CONDITIONS) and attacks['clean'] == prior['clean'] == ''
    assert config['conditions'] == list(CONDITIONS) and config['defenses'] == list(DEFENSES)
    assert config['replicate_ids'] == [1, 2, 3] and 'seeds' not in config
    assert config['topologies'] == ['blackboard_4'] and config['phase'] == 'formal'
    tasks = json.loads(Path(config['task_file']).read_text())['tasks']
    assert len(schedule(config)) == 54
    # Only the dedicated exogenous attack text differs. Business prompts untouched.
    profile = dict(profile, attacks=attacks)
    hashes = dict(frozen['files'], **{str(path): frozen['r3_config_sha256'],
                                    config['attack_file']: frozen['attack_file_sha256']})
    return config, tasks, profile, hashes


def episode_metrics(status, events):
    count = sum(e['delivered_reconstructable_secret_exposure'] for e in events)
    return {'episode_reconstructable_disclosure': int(count > 0) if status == 'completed' else None,
            'partial_reconstructable_disclosure_observed': int(count > 0),
            'propagation_event_count': count,
            'external_recipient_reconstructable_observations': sum(
                e['delivered_reconstructable_secret_exposure']
                for e in events if e.get('recipient_id') == 'external_vendor_agent')}


class R3BindingEpisode(R2BindingEpisode):
    def __init__(self, task, topology, condition, defense, replicate_id, config, client,
                 sink=None, *, private_sink=None, profile):
        # Neutral compatibility slot in the inherited constructor; never used as
        # RNG input. No seed field is exposed in R3 records or provider payloads.
        super().__init__(task, topology, condition, defense, None, config, client,
                         sink, private_sink=private_sink, profile=profile)
        self.replicate_id = replicate_id
        self.run_id = run_id(dict(task_id=task['task_id'], topology=topology,
                                  condition=condition, defense=defense, replicate_id=replicate_id))

    def augment_row(self, row):
        row = super().augment_row(row)
        row.pop('seed')
        row['replicate_id'] = self.replicate_id
        row.update(episode_metrics(row['status'], self.audit))
        row['approve_correctness'] = row['success'] if row['gold_action'] == 'approve_quote' else None
        row['hold_correctness'] = row['success'] if row['gold_action'] == 'hold' else None
        return row
