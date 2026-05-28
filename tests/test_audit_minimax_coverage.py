import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "audit_minimax_coverage.py"
CONFIG = REPO_ROOT / "configs" / "experiment" / "mas_p1_minimax_coverage.yaml"


def write_run(root: Path, topology: str, attack: str, defense: str, seed: int, metrics: dict) -> None:
    run_name = f"run__{topology}__{attack}__{defense}__seed{seed}"
    run_dir = root / run_name
    run_dir.mkdir(parents=True)
    meta = {
        "run_id": run_name,
        "topology": topology,
        "attack": attack,
        "defense": defense,
        "seed": seed,
        "provider": "minimax",
        "provider_calls_enabled": True,
        "agent_backend": "minimax_final_writer",
    }
    (run_dir / "meta.json").write_text(json.dumps(meta), encoding="utf-8")
    (run_dir / "metrics.json").write_text(json.dumps(metrics), encoding="utf-8")


class AuditMiniMaxCoverageTest(unittest.TestCase):
    def run_audit(self, runs_root: Path, summary_dir: Path, output_dir: Path, strict: bool = False) -> subprocess.CompletedProcess:
        cmd = [
            sys.executable,
            str(SCRIPT),
            "--runs-root",
            str(runs_root),
            "--summary-dir",
            str(summary_dir),
            "--matrix-config",
            str(CONFIG),
            "--output-dir",
            str(output_dir),
        ]
        if strict:
            cmd.append("--strict")
        return subprocess.run(cmd, cwd=REPO_ROOT, text=True, capture_output=True, check=False)

    def test_audit_outputs_and_classification(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            runs_root = tmp_path / "runs"
            summary_dir = tmp_path / "summary"
            output_dir = tmp_path / "audit"
            summary_dir.mkdir()
            write_run(
                runs_root,
                "chain_4",
                "summary_poisoning_indirect",
                "flowfence_lite",
                1,
                {"task_success": True, "unauthorized_raw_leakage": 0, "external_leakage": 0, "cascade_size": 2, "cascade_depth": 1, "privilege_reach": 0},
            )
            write_run(
                runs_root,
                "chain_4",
                "summary_poisoning_indirect",
                "prompt_filter",
                1,
                {"task_success": False, "unauthorized_raw_leakage": 3, "external_leakage": 1, "cascade_size": 5, "cascade_depth": 3, "privilege_reach": 5},
            )
            write_run(
                runs_root,
                "chain_4",
                "summary_poisoning_indirect",
                "none",
                1,
                {"task_success": True, "unauthorized_raw_leakage": 2, "external_leakage": 1, "cascade_size": 4, "cascade_depth": 3, "privilege_reach": 3},
            )

            result = self.run_audit(runs_root, summary_dir, output_dir)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

            expected = [
                "coverage_summary.json",
                "coverage_summary.md",
                "coverage_by_defense.csv",
                "coverage_by_defense.md",
                "coverage_by_topology.csv",
                "coverage_by_topology.md",
                "coverage_by_attack.csv",
                "coverage_by_attack.md",
                "coverage_by_attack_defense.csv",
                "coverage_by_attack_defense.md",
                "coverage_by_seed.csv",
                "coverage_by_seed.md",
                "flowfence_clean_matrix.csv",
                "flowfence_clean_matrix.md",
                "failure_breakdown.jsonl",
            ]
            for name in expected:
                self.assertTrue((output_dir / name).exists(), name)

            summary = json.loads((output_dir / "coverage_summary.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["flowfence_clean_run_count"], 1)
            self.assertEqual(summary["flowfence_total_run_count"], 1)
            self.assertEqual(summary["provider"], "minimax")
            self.assertTrue(summary["provider_calls_enabled"])

            with (output_dir / "coverage_by_defense.csv").open(encoding="utf-8", newline="") as f:
                rows = list(csv.DictReader(f))
            self.assertTrue(rows)
            with (output_dir / "coverage_by_seed.csv").open(encoding="utf-8", newline="") as f:
                seed_rows = list(csv.DictReader(f))
            self.assertEqual(seed_rows[0]["seed"], "1")
            self.assertEqual(seed_rows[0]["flowfence_unauthorized_raw_leakage_mean"], "0.0")
            with (output_dir / "flowfence_clean_matrix.csv").open(encoding="utf-8", newline="") as f:
                clean_rows = list(csv.DictReader(f))
            self.assertEqual(clean_rows[0]["clean"], "True")

            failures = [json.loads(line) for line in (output_dir / "failure_breakdown.jsonl").read_text(encoding="utf-8").splitlines()]
            self.assertTrue(any(row["failure_type"] == "prompt_filter_indirect_failure" for row in failures))

            outputs = "\n".join(path.read_text(encoding="utf-8") for path in output_dir.iterdir() if path.is_file())
            for marker in ["$4800", "supplier breach investigation", "CUST-8831-PRIVATE", "sk-internal-demo-token"]:
                self.assertNotIn(marker, outputs)

    def test_multi_seed_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            runs_root = tmp_path / "runs"
            summary_dir = tmp_path / "summary"
            output_dir = tmp_path / "audit"
            summary_dir.mkdir()
            for seed in [1, 2]:
                write_run(
                    runs_root,
                    "blackboard_4",
                    "workspace_poisoning_indirect",
                    "flowfence_lite",
                    seed,
                    {"task_success": True, "unauthorized_raw_leakage": 0, "external_leakage": 0, "cascade_size": 3, "cascade_depth": 1, "privilege_reach": 0},
                )
                write_run(
                    runs_root,
                    "blackboard_4",
                    "workspace_poisoning_indirect",
                    "prompt_filter",
                    seed,
                    {"task_success": seed == 1, "unauthorized_raw_leakage": seed, "external_leakage": 1, "cascade_size": 7, "cascade_depth": 3, "privilege_reach": 5},
                )

            result = self.run_audit(runs_root, summary_dir, output_dir)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

            with (output_dir / "coverage_by_seed.csv").open(encoding="utf-8", newline="") as f:
                seed_rows = list(csv.DictReader(f))
            self.assertEqual([row["seed"] for row in seed_rows], ["1", "2"])
            self.assertTrue(all(row["flowfence_task_success_rate"] == "1.0" for row in seed_rows))

            with (output_dir / "flowfence_clean_matrix.csv").open(encoding="utf-8", newline="") as f:
                clean_rows = list(csv.DictReader(f))
            self.assertEqual(len(clean_rows), 2)
            self.assertTrue(all(row["clean"] == "True" for row in clean_rows))

    def test_missing_runs_root_handled_non_strict_and_strict(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            missing_root = tmp_path / "missing"
            summary_dir = tmp_path / "summary"
            output_dir = tmp_path / "audit"
            summary_dir.mkdir()
            result = self.run_audit(missing_root, summary_dir, output_dir)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertTrue((output_dir / "coverage_summary.json").exists())
            strict_result = self.run_audit(missing_root, summary_dir, tmp_path / "strict_audit", strict=True)
            self.assertNotEqual(strict_result.returncode, 0)

    def test_help(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "--help"], cwd=REPO_ROOT, text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 0)
        self.assertIn("--runs-root", result.stdout)


if __name__ == "__main__":
    unittest.main()
