import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "debug_minimax_coverage_timeout.py"
CONFIG = REPO_ROOT / "configs" / "experiment" / "mas_p1_minimax_coverage_3seed.yaml"
FAILED_RUN = "mas_p1__enterprise_assistant_001__chain_4__summary_poisoning_direct__prompt_filter__seed1"


def write_artifacts(root: Path, include_failed: bool = True) -> None:
    root.mkdir(parents=True)
    manifest = {
        "schema_version": "test",
        "expected_run_count": 252,
        "completed_run_count": 251,
        "failed_run_count": 1,
        "provider": "minimax",
        "provider_calls_enabled": True,
        "agent_backend": "minimax_final_writer",
    }
    if include_failed:
        manifest["failed_runs"] = [{"run_name": FAILED_RUN, "error_category": "minimax_read_timeout"}]
    (root / "run_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    (root / "coverage_summary.json").write_text(
        json.dumps({"expected_run_count": 252, "completed_run_count": 251, "failed_run_count": 1}),
        encoding="utf-8",
    )
    (root / "failure_breakdown.jsonl").write_text("", encoding="utf-8")


class DebugMiniMaxCoverageTimeoutTest(unittest.TestCase):
    def run_debug(self, artifact_dir: Path, output_dir: Path, strict: bool = False) -> subprocess.CompletedProcess:
        cmd = [
            sys.executable,
            str(SCRIPT),
            "--coverage-artifact-dir",
            str(artifact_dir),
            "--matrix-config",
            str(CONFIG),
            "--output-dir",
            str(output_dir),
        ]
        if strict:
            cmd.append("--strict")
        return subprocess.run(cmd, cwd=REPO_ROOT, text=True, capture_output=True, check=False)

    def test_identifies_failed_run_from_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            artifact_dir = tmp_path / "artifacts"
            output_dir = tmp_path / "debug"
            write_artifacts(artifact_dir)

            result = self.run_debug(artifact_dir, output_dir, strict=True)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            for name in ["debug_summary.json", "debug_summary.md", "failed_run_diagnosis.json"]:
                self.assertTrue((output_dir / name).exists(), name)

            diagnosis = json.loads((output_dir / "failed_run_diagnosis.json").read_text(encoding="utf-8"))
            self.assertEqual(diagnosis["failed_run"]["run_name"], FAILED_RUN)
            self.assertEqual(diagnosis["failed_run"]["topology"], "chain_4")
            self.assertEqual(diagnosis["failed_run"]["attack"], "summary_poisoning_direct")
            self.assertEqual(diagnosis["failed_run"]["defense"], "prompt_filter")
            self.assertEqual(diagnosis["failed_run"]["seed"], 1)
            self.assertEqual(diagnosis["failure_type"], "minimax_read_timeout")
            self.assertTrue(diagnosis["appears_transient"])

            outputs = "\n".join(path.read_text(encoding="utf-8") for path in output_dir.iterdir())
            for marker in ["$4800", "supplier breach investigation", "CUST-8831-PRIVATE", "sk-internal-demo-token"]:
                self.assertNotIn(marker, outputs)

    def test_unknown_failed_run_is_graceful(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            artifact_dir = tmp_path / "artifacts"
            output_dir = tmp_path / "debug"
            write_artifacts(artifact_dir, include_failed=False)

            result = self.run_debug(artifact_dir, output_dir)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            summary = json.loads((output_dir / "debug_summary.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["status"], "failed_run_unknown")
            strict_result = self.run_debug(artifact_dir, tmp_path / "strict_debug", strict=True)
            self.assertNotEqual(strict_result.returncode, 0)

    def test_help(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "--help"], cwd=REPO_ROOT, text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 0)
        self.assertIn("--coverage-artifact-dir", result.stdout)


if __name__ == "__main__":
    unittest.main()
