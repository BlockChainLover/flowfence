import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE = REPO_ROOT / "tests" / "fixtures" / "agentpoison_case_result_minimal.json"
CONVERTER = REPO_ROOT / "scripts" / "convert_agentpoison_to_events.py"
POISON_PAYLOAD = "SYNTHETIC_RAW_POISON_PAYLOAD_DO_NOT_EXPOSE"


class ConvertAgentPoisonToEventsTest(unittest.TestCase):
    def test_converter_outputs_event_traces(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            run_dir = tmp_path / "run"
            out_dir = tmp_path / "events"
            run_dir.mkdir()
            shutil.copy(FIXTURE, run_dir / "case_results.json")

            subprocess.run(
                [
                    sys.executable,
                    str(CONVERTER),
                    "--run-dir",
                    str(run_dir),
                    "--output-dir",
                    str(out_dir),
                ],
                cwd=REPO_ROOT,
                check=True,
                text=True,
                capture_output=True,
            )

            events_full_path = out_dir / "events.full.jsonl"
            events_safe_path = out_dir / "events.safe.jsonl"
            decisions_path = out_dir / "policy_decisions.jsonl"
            metrics_path = out_dir / "metrics.recomputed.json"
            for path in (events_full_path, events_safe_path, decisions_path, metrics_path):
                self.assertTrue(path.exists(), path)

            events_full = [json.loads(line) for line in events_full_path.read_text().splitlines()]
            events_safe = [json.loads(line) for line in events_safe_path.read_text().splitlines()]
            decisions = [json.loads(line) for line in decisions_path.read_text().splitlines()]
            metrics = json.loads(metrics_path.read_text())

            self.assertTrue(any(event["event_type"] == "MEMORY_READ" for event in events_full))
            self.assertGreaterEqual(len(decisions), 1)
            self.assertGreaterEqual(len(events_safe), 1)
            self.assertNotIn(POISON_PAYLOAD, events_safe_path.read_text())
            self.assertIn("exposed_poisoned_retrieval_case_rate", metrics)


if __name__ == "__main__":
    unittest.main()
