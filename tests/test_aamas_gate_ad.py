"""Deterministic boundary tests; no benchmark or provider dependency."""
import io
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest

from src.experiments.aamas_gate_ac import ReleaseAdapter, DEFENSES
from src.experiments.aamas_gate_ad import coding_write_boundary
from src.runtime.events import SecretPolicy


class WriteBoundaryTests(unittest.TestCase):
    def test_whole_artifact_and_split_writes(self):
        policy = SecretPolicy('fixture', 'owner', 'SYNTHETIC-PRIVATE-123', 'P2', ['owner'],
                              'none', ['shared_doc'])
        for defense in DEFENSES:
            adapter = ReleaseAdapter(defense, [policy], ['owner', 'peer'])
            module = SimpleNamespace()
            with tempfile.TemporaryDirectory() as tmp:
                target = Path(tmp)/'solution.py'
                with coding_write_boundary(module, tmp, lambda s: adapter.release(s, 'owner', 'shared', 'shared_doc', 'WORKSPACE_WRITE')):
                    with module.open(target, 'w') as f:
                        f.write('# SYNTHETIC-')
                        f.write('PRIVATE-123')
                        f.flush()
                        self.assertNotIn(policy.raw_value, target.read_text())
                    self.assertNotIn(policy.raw_value, target.read_text())
                self.assertNotIn('open', module.__dict__)
                self.assertTrue(adapter.events)

    def test_clean_content_and_failure_restore(self):
        for defense in DEFENSES:
            adapter = ReleaseAdapter(defense, [], ['owner'])
            module = SimpleNamespace()
            with tempfile.TemporaryDirectory() as tmp:
                target = Path(tmp)/'solution.py'
                with coding_write_boundary(module, tmp, lambda s: adapter.release(s, 'owner', 'shared', 'shared_doc')):
                    with module.open(target, 'w') as f:
                        self.assertEqual(f.write('print(1)\n'), 9)
                    with module.open(target) as f:
                        self.assertEqual(f.read(), 'print(1)\n')
                self.assertEqual(target.read_bytes(), b'print(1)\n')
                with self.assertRaises(RuntimeError):
                    with coding_write_boundary(module, tmp, lambda s:s):
                        raise RuntimeError('fixture')
                self.assertNotIn('open', module.__dict__)


if __name__ == '__main__':
    unittest.main()
