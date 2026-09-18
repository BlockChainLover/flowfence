"""Generic-boundary probes and evidence validation; no provider calls."""
import builtins
import json
from pathlib import Path
import tempfile
import unittest

from src.experiments.aamas_gate_ac import ReleaseAdapter,DEFENSES
from src.experiments.aamas_gate_ae import ContextBoundaryProbe,workspace_publication_probe
from src.runtime.events import SecretPolicy


class GenericBoundaryTests(unittest.TestCase):
    def test_explicit_recipient_and_missing_identity(self):
        p=SecretPolicy('test','owner','SYNTHETIC-PRIVATE-123','P2',['owner'],'none',['shared_doc'])
        for defense in DEFENSES:
            ad=ReleaseAdapter(defense,[p],['owner','worker']);seen=[]
            gateway=ContextBoundaryProbe(ad,lambda **kw:seen.append(kw))
            with self.assertRaises(RuntimeError):gateway(messages=[])
            with gateway.scope('worker'):
                gateway(messages=[{'role':'user','content':p.raw_value}])
            self.assertNotIn(p.raw_value,json.dumps(seen[-1]))
            with gateway.scope('owner'):
                gateway(messages=[{'role':'user','content':p.raw_value}])
            self.assertIn(p.raw_value,json.dumps(seen[-1]))
            self.assertIsNone(gateway.principal.get())

    def test_generic_json_chunk_publication_and_clean_equivalence(self):
        p=SecretPolicy('test','owner','SYNTHETIC-PRIVATE-123','P2',['owner'],'none',['shared_doc'])
        for defense in DEFENSES:
            ad=ReleaseAdapter(defense,[p],['owner','worker'])
            with tempfile.TemporaryDirectory() as tmp:
                path=Path(tmp)/'artifact.json';before=builtins.open
                ordinary={'public':[1,2,3]}
                with open(path,'w') as f:json.dump(ordinary,f,indent=2)
                expected=path.read_bytes()
                with workspace_publication_probe(tmp,lambda s:ad.release(s,'owner','shared','shared_doc','WORKSPACE_WRITE')):
                    with open(path,'w') as f:json.dump(ordinary,f,indent=2)
                    self.assertEqual(path.read_bytes(),expected)
                    with open(path,'w') as f:json.dump({'protected':p.raw_value},f)
                self.assertNotIn(p.raw_value,path.read_text())
                self.assertIs(builtins.open,before)

    def test_recorded_transition_evidence(self):
        root=Path(__file__).resolve().parents[1]
        report=json.loads((root/'artifacts/aamas2027_gate_ae/AUDIT.json').read_text())
        self.assertEqual(len(report['certification']),300)
        for record in report['transition_pairs']:
            self.assertTrue(all(v for k,v in record.items() if k.startswith('same_')),record['transition'])
        self.assertEqual(len({r['transition'] for r in report['transition_pairs']}),22)
        for probe in report['boundary_probes']:
            self.assertTrue(probe['session_outer_scope_misattribution'])
            self.assertTrue(all(probe['direct_storage'].values()))
            self.assertTrue(probe['explicit_recipient_gateway_safe'])
            self.assertTrue(probe['outgoing_raw_absent'])
        for record in report['topology']:
            if record['reply_model_calls']:
                self.assertEqual(record['reply_schema_impossible_required_fields'],['target_agent_id'])
        self.assertEqual(report['formal_model_runs'],0)
        self.assertEqual(report['development_model_runs'],0)
        self.assertEqual(report['network_attempts'],0)


if __name__=='__main__':unittest.main()
