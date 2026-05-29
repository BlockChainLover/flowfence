import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPORT_SCRIPT = REPO_ROOT / "scripts" / "export_paper_tables.py"
REVIEW_SCRIPT = REPO_ROOT / "scripts" / "review_paper_tables.py"


class ReviewPaperTablesTest(unittest.TestCase):
    def export_tables(self, output_dir: Path) -> None:
        result = subprocess.run(
            [sys.executable, str(EXPORT_SCRIPT), "--output-dir", str(output_dir)],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def review_tables(self, tables_dir: Path, output_dir: Path, strict: bool = False) -> subprocess.CompletedProcess:
        cmd = [
            sys.executable,
            str(REVIEW_SCRIPT),
            "--tables-dir",
            str(tables_dir),
            "--output-dir",
            str(output_dir),
        ]
        if strict:
            cmd.append("--strict")
        return subprocess.run(cmd, cwd=REPO_ROOT, text=True, capture_output=True, check=False)

    def test_review_exported_tables(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            tables_dir = tmp_path / "tables"
            review_dir = tmp_path / "review"
            self.export_tables(tables_dir)

            result = self.review_tables(tables_dir, review_dir)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

            expected = [
                "table_review_report.json",
                "table_review_report.md",
                "table_issues.jsonl",
                "README.md",
            ]
            for name in expected:
                self.assertTrue((review_dir / name).exists(), name)

            report = json.loads((review_dir / "table_review_report.json").read_text(encoding="utf-8"))
            self.assertIn("issue_counts", report)
            self.assertEqual(report["issue_counts"]["ERROR"], 0)
            for table in [
                "table_1_p0_agentpoison",
                "table_2_p1_synthetic",
                "table_3_minimax_postfix_smoke",
                "table_3_minimax_3seed_coverage",
                "table_4_claims_matrix",
                "table_5_evidence_boundaries",
                "table_6_minimax_3seed_seed_stability",
                "table_7_nonoracle_heldout_validation",
                "table_8_nonoracle_mechanism_ablation",
            ]:
                self.assertIn(table, report["tables_reviewed"])

            outputs = "\n".join(path.read_text(encoding="utf-8") for path in review_dir.iterdir() if path.is_file())
            for marker in [
                "$4800",
                "supplier breach investigation",
                "CUST-8831-PRIVATE",
                "sk-internal-demo-token",
            ]:
                self.assertNotIn(marker, outputs)

    def test_raw_secret_triggers_error_without_leaking_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            tables_dir = tmp_path / "tables"
            review_dir = tmp_path / "review"
            self.export_tables(tables_dir)
            with (tables_dir / "table_7_nonoracle_heldout_validation.md").open("a", encoding="utf-8") as f:
                f.write("\nSYNTHETIC SECRET: $4800\n")

            result = self.review_tables(tables_dir, review_dir, strict=True)
            self.assertNotEqual(result.returncode, 0)
            report = json.loads((review_dir / "table_review_report.json").read_text(encoding="utf-8"))
            self.assertGreater(report["issue_counts"]["ERROR"], 0)
            outputs = "\n".join(path.read_text(encoding="utf-8") for path in review_dir.iterdir() if path.is_file())
            self.assertNotIn("$4800", outputs)
            self.assertIn("raw_secret_absent", outputs)

    def test_non_minimax_supported_claim_triggers_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            tables_dir = tmp_path / "tables"
            review_dir = tmp_path / "review"
            self.export_tables(tables_dir)

            claims_csv = tables_dir / "table_4_claims_matrix.csv"
            with claims_csv.open(encoding="utf-8", newline="") as f:
                rows = list(csv.DictReader(f))
                headers = rows[0].keys()
            for row in rows:
                if row["claim"] == "Non-MiniMax generalization":
                    row["supported_status"] = "supported"
                    row["ready_for_paper"] = "yes"
            with claims_csv.open("w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=headers, lineterminator="\n")
                writer.writeheader()
                writer.writerows(rows)

            result = self.review_tables(tables_dir, review_dir, strict=True)
            self.assertNotEqual(result.returncode, 0)
            report = json.loads((review_dir / "table_review_report.json").read_text(encoding="utf-8"))
            self.assertTrue(report["unsupported_claim_overmarked"])

    def test_arbitrary_attack_robustness_supported_claim_triggers_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            tables_dir = tmp_path / "tables"
            review_dir = tmp_path / "review"
            self.export_tables(tables_dir)

            claims_csv = tables_dir / "table_4_claims_matrix.csv"
            with claims_csv.open(encoding="utf-8", newline="") as f:
                rows = list(csv.DictReader(f))
                headers = rows[0].keys()
            for row in rows:
                if row["claim"] == "Arbitrary attack robustness":
                    row["supported_status"] = "supported"
                    row["ready_for_paper"] = "yes"
            with claims_csv.open("w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=headers, lineterminator="\n")
                writer.writeheader()
                writer.writerows(rows)

            result = self.review_tables(tables_dir, review_dir, strict=True)
            self.assertNotEqual(result.returncode, 0)
            report = json.loads((review_dir / "table_review_report.json").read_text(encoding="utf-8"))
            self.assertTrue(report["unsupported_claim_overmarked"])

    def test_new_table_value_mismatch_triggers_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            tables_dir = tmp_path / "tables"
            review_dir = tmp_path / "review"
            self.export_tables(tables_dir)

            coverage_csv = tables_dir / "table_3_minimax_3seed_coverage.csv"
            with coverage_csv.open(encoding="utf-8", newline="") as f:
                rows = list(csv.DictReader(f))
                headers = rows[0].keys()
            for row in rows:
                if row["group"] == "aggregate_252run":
                    row["completed_runs"] = "251"
            with coverage_csv.open("w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=headers, lineterminator="\n")
                writer.writeheader()
                writer.writerows(rows)

            result = self.review_tables(tables_dir, review_dir, strict=True)
            self.assertNotEqual(result.returncode, 0)
            report = json.loads((review_dir / "table_review_report.json").read_text(encoding="utf-8"))
            self.assertTrue(report["table_values_inconsistent"])

    def test_nonoracle_table_value_mismatch_triggers_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            tables_dir = tmp_path / "tables"
            review_dir = tmp_path / "review"
            self.export_tables(tables_dir)

            table_csv = tables_dir / "table_7_nonoracle_heldout_validation.csv"
            with table_csv.open(encoding="utf-8", newline="") as f:
                rows = list(csv.DictReader(f))
                headers = rows[0].keys()
            for row in rows:
                if row["group"] == "targeted_minimax_nonoracle":
                    row["completed_runs"] = "71"
            with table_csv.open("w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=headers, lineterminator="\n")
                writer.writeheader()
                writer.writerows(rows)

            result = self.review_tables(tables_dir, review_dir, strict=True)
            self.assertNotEqual(result.returncode, 0)
            report = json.loads((review_dir / "table_review_report.json").read_text(encoding="utf-8"))
            self.assertTrue(report["table_values_inconsistent"])


if __name__ == "__main__":
    unittest.main()
