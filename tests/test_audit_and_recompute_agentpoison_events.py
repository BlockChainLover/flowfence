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
AUDIT = REPO_ROOT / "scripts" / "audit_events.py"
RECOMPUTE = REPO_ROOT / "scripts" / "recompute_agentpoison_metrics_from_events.py"
POISON_PAYLOAD = "SYNTHETIC_RAW_POISON_PAYLOAD_DO_NOT_EXPOSE"


class AuditAndRecomputeAgentPoisonEventsTest(unittest.TestCase):
    def _converted_tempdir(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        tmp = tempfile.TemporaryDirectory()
        tmp_path = Path(tmp.name)
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
        return tmp, out_dir

    def test_audit_and_recompute_pass_on_fixture_conversion(self) -> None:
        tmp, out_dir = self._converted_tempdir()
        with tmp:
            audit_result = subprocess.run(
                [sys.executable, str(AUDIT), "--run-dir", str(out_dir), "--trigger-string", POISON_PAYLOAD],
                cwd=REPO_ROOT,
                check=True,
                text=True,
                capture_output=True,
            )
            self.assertIn("AUDIT PASS", audit_result.stdout)

            recompute_result = subprocess.run(
                [sys.executable, str(RECOMPUTE), "--run-dir", str(out_dir), "--pretty"],
                cwd=REPO_ROOT,
                check=True,
                text=True,
                capture_output=True,
            )
            metrics_path = out_dir / "metrics.recomputed.audit.json"
            self.assertTrue(metrics_path.exists())
            metrics = json.loads(metrics_path.read_text())
            json.loads(recompute_result.stdout)
            for key in (
                "case_count",
                "event_count",
                "memory_read_event_count",
                "exposed_poisoned_retrieval_case_rate",
                "defense_intervention_event_rate",
                "quarantine_count",
            ):
                self.assertIn(key, metrics)
            self.assertNotIn(POISON_PAYLOAD, (out_dir / "events.safe.jsonl").read_text())

    def test_audit_fails_when_required_event_field_is_missing(self) -> None:
        tmp, out_dir = self._converted_tempdir()
        with tmp:
            full_path = out_dir / "events.full.jsonl"
            rows = [json.loads(line) for line in full_path.read_text().splitlines()]
            rows[0].pop("event_id", None)
            full_path.write_text("\n".join(json.dumps(row) for row in rows) + "\n")
            result = subprocess.run(
                [sys.executable, str(AUDIT), "--run-dir", str(out_dir)],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("AUDIT FAIL", result.stdout)


if __name__ == "__main__":
    unittest.main()
