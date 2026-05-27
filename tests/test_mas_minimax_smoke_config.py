import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SWEEP = REPO_ROOT / "src" / "runner" / "sweep_mas.py"
SMOKE_CONFIG = REPO_ROOT / "configs" / "experiment" / "mas_p1_minimax_smoke.yaml"
SECRETS = ["$4800", "supplier breach investigation", "CUST-8831-PRIVATE", "sk-internal-demo-token"]


class FakeMiniMaxClient:
    def available(self) -> bool:
        return True

    def missing_variables(self) -> list[str]:
        return []

    def complete(self, prompt: str) -> dict[str, object]:
        from src.runtime.events import sha256_text

        text = (
            "Vendor-safe project update: delivery remains active; budget constraint exists; "
            "internal details withheld; customer identifier withheld; internal credential withheld."
        )
        return {
            "text": text,
            "provider": "minimax",
            "model": "fake-minimax",
            "prompt_sha256": sha256_text(prompt),
            "response_sha256": sha256_text(text),
            "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
            "latency_seconds": 0.0,
        }


class MASMiniMaxSmokeConfigTest(unittest.TestCase):
    def test_smoke_config_expands_to_18_runs(self) -> None:
        from src.runner.sweep_mas import expand_runs, load_matrix_yaml

        config = load_matrix_yaml(SMOKE_CONFIG)
        runs = expand_runs(config)
        self.assertEqual(config["provider"], "minimax")
        self.assertTrue(config["provider_calls_enabled"])
        self.assertEqual(config["agent_backend"], "minimax_final_writer")
        self.assertEqual(len(runs), 18)

    def test_sweep_requires_explicit_provider_call_flag(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [
                    sys.executable,
                    str(SWEEP),
                    "--config",
                    str(SMOKE_CONFIG),
                    "--output-root",
                    str(Path(tmp) / "runs"),
                    "--max-runs",
                    "1",
                ],
                cwd=REPO_ROOT,
                env={**os.environ, "PYTHONPATH": "."},
                text=True,
                capture_output=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("--allow-provider-calls", result.stderr)

    def test_provider_other_than_minimax_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "bad.yaml"
            config.write_text(
                """domain:
- enterprise_assistant
task_file: data/multiagent_tasks/enterprise_assistant_v1.jsonl
task_id: enterprise_assistant_001
topology:
- chain_4
attack:
- none
defense:
- none
seed:
- 1
agent_backend: minimax_final_writer
provider: invalid
provider_calls_enabled: true
output_root: results/unused
""",
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, str(SWEEP), "--config", str(config), "--output-root", str(Path(tmp) / "runs")],
                cwd=REPO_ROOT,
                env={**os.environ, "PYTHONPATH": "."},
                text=True,
                capture_output=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("provider: minimax", result.stderr)

    def test_fake_minimax_final_writer_outputs_safe_trace(self) -> None:
        from src.runtime.orchestrator import run_and_write

        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "run"
            config = {
                "run_name": "fake_minimax_smoke",
                "task_file": "data/multiagent_tasks/enterprise_assistant_v1.jsonl",
                "task_id": "enterprise_assistant_001",
                "topology": "chain_4",
                "attack": "summary_poisoning_indirect",
                "defense": "flowfence_lite",
                "seed": 1,
                "agent_backend": "minimax_final_writer",
                "provider": "minimax",
                "provider_calls_enabled": True,
                "temperature": 0.0,
                "max_tokens": 256,
                "timeout_seconds": 60,
            }
            run_and_write(config, output_dir, overwrite=True, repo_root=REPO_ROOT, minimax_client=FakeMiniMaxClient())
            for name in ("meta.json", "events.full.jsonl", "events.safe.jsonl", "policy_decisions.jsonl", "metrics.json"):
                self.assertTrue((output_dir / name).exists(), name)
            full_events = [
                json.loads(line)
                for line in (output_dir / "events.full.jsonl").read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            final_events = [event for event in full_events if event["event_type"] == "FINAL_OUTPUT"]
            self.assertEqual(len(final_events), 1)
            self.assertEqual(final_events[0]["metadata"]["provider"], "minimax")
            safe_text = (output_dir / "events.safe.jsonl").read_text(encoding="utf-8")
            for secret in SECRETS:
                self.assertNotIn(secret, safe_text)

    def test_missing_credentials_are_sanitized(self) -> None:
        from src.runtime.minimax_client import MiniMaxClient

        with patch.dict(os.environ, {}, clear=True):
            client = MiniMaxClient()
            self.assertFalse(client.available())
            self.assertEqual(client.missing_variables(), ["MINIMAX_API_KEY"])
            with self.assertRaisesRegex(RuntimeError, "MINIMAX_API_KEY"):
                client.complete("hello")


if __name__ == "__main__":
    unittest.main()
