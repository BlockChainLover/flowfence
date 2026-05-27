import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SWEEP = REPO_ROOT / "src" / "runner" / "sweep_mas.py"
SUMMARY = REPO_ROOT / "src" / "runner" / "summarize_mas_p1.py"
SECRETS = ["$4800", "supplier breach investigation", "CUST-8831-PRIVATE", "sk-internal-demo-token"]


def small_matrix(provider: str = "minimax", provider_calls_enabled: str = "false") -> str:
    return f"""domain:
- enterprise_assistant
task_file: data/multiagent_tasks/enterprise_assistant_v1.jsonl
task_id: enterprise_assistant_001
topology:
- chain_4
- blackboard_4
attack:
- none
- summary_poisoning
defense:
- none
- flowfence_lite
seed:
- 1
agent_backend: scripted_deterministic
provider: {provider}
provider_calls_enabled: {provider_calls_enabled}
output_root: results/unused
"""


class MASSweepAndSummaryTest(unittest.TestCase):
    def test_sweep_and_summary_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            config = tmp_path / "matrix.yaml"
            output_root = tmp_path / "runs"
            summary_dir = tmp_path / "summary"
            status_path = tmp_path / "status.json"
            config.write_text(small_matrix(), encoding="utf-8")
            subprocess.run(
                [
                    sys.executable,
                    str(SWEEP),
                    "--config",
                    str(config),
                    "--output-root",
                    str(output_root),
                    "--status-path",
                    str(status_path),
                    "--force",
                ],
                cwd=REPO_ROOT,
                env={**os.environ, "PYTHONPATH": "."},
                text=True,
                capture_output=True,
                check=True,
            )
            run_dirs = sorted(path for path in output_root.iterdir() if path.is_dir())
            self.assertEqual(len(run_dirs), 8)
            for run_dir in run_dirs:
                for name in ("meta.json", "events.full.jsonl", "events.safe.jsonl", "policy_decisions.jsonl", "metrics.json"):
                    self.assertTrue((run_dir / name).exists(), f"{run_dir}/{name}")
                safe_text = (run_dir / "events.safe.jsonl").read_text(encoding="utf-8")
                for secret in SECRETS:
                    self.assertNotIn(secret, safe_text)
            subprocess.run(
                [
                    sys.executable,
                    str(SUMMARY),
                    "--runs-root",
                    str(output_root),
                    "--output-dir",
                    str(summary_dir),
                    "--matrix-config",
                    str(config),
                ],
                cwd=REPO_ROOT,
                env={**os.environ, "PYTHONPATH": "."},
                text=True,
                capture_output=True,
                check=True,
            )
            for name in ("summary.json", "summary.md", "topology_sanity.json", "failure_cases.jsonl"):
                self.assertTrue((summary_dir / name).exists(), name)
            summary = json.loads((summary_dir / "summary.json").read_text(encoding="utf-8"))
            sanity = json.loads((summary_dir / "topology_sanity.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["overall_results"]["run_count"], 8)
            self.assertIn("topology_effect_observed", sanity)

    def test_provider_calls_enabled_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            config = tmp_path / "matrix.yaml"
            config.write_text(small_matrix(provider_calls_enabled="true"), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SWEEP), "--config", str(config), "--output-root", str(tmp_path / "runs")],
                cwd=REPO_ROOT,
                env={**os.environ, "PYTHONPATH": "."},
                text=True,
                capture_output=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("provider_calls_enabled", result.stderr)

    def test_non_minimax_provider_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            config = tmp_path / "matrix.yaml"
            config.write_text(small_matrix(provider="invalid"), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SWEEP), "--config", str(config), "--output-root", str(tmp_path / "runs")],
                cwd=REPO_ROOT,
                env={**os.environ, "PYTHONPATH": "."},
                text=True,
                capture_output=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("provider: minimax", result.stderr)


if __name__ == "__main__":
    unittest.main()
