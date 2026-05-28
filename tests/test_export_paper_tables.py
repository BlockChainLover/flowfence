import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "export_paper_tables.py"


class ExportPaperTablesTest(unittest.TestCase):
    def run_export(self, output_dir: Path, strict: bool = False) -> subprocess.CompletedProcess:
        cmd = [sys.executable, str(SCRIPT), "--output-dir", str(output_dir)]
        if strict:
            cmd.append("--strict")
        return subprocess.run(cmd, cwd=REPO_ROOT, text=True, capture_output=True, check=False)

    def test_export_outputs_expected_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "paper_tables"
            result = self.run_export(output_dir)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

            expected = [
                "paper_tables_summary.json",
                "paper_tables_summary.md",
                "table_1_p0_agentpoison.csv",
                "table_1_p0_agentpoison.md",
                "table_2_p1_synthetic.csv",
                "table_2_p1_synthetic.md",
                "table_3_minimax_postfix_smoke.csv",
                "table_3_minimax_postfix_smoke.md",
                "table_4_claims_matrix.csv",
                "table_4_claims_matrix.md",
                "table_5_evidence_boundaries.csv",
                "table_5_evidence_boundaries.md",
                "README.md",
            ]
            for name in expected:
                self.assertTrue((output_dir / name).exists(), name)

            summary = json.loads((output_dir / "paper_tables_summary.json").read_text(encoding="utf-8"))
            self.assertIn("generated_tables", summary)
            self.assertIn("warnings", summary)

            for csv_name in [name for name in expected if name.endswith(".csv")]:
                with (output_dir / csv_name).open(encoding="utf-8", newline="") as f:
                    rows = list(csv.reader(f))
                self.assertGreaterEqual(len(rows), 2, csv_name)
                self.assertTrue(rows[0], csv_name)

            md_text = (output_dir / "table_3_minimax_postfix_smoke.md").read_text(encoding="utf-8")
            self.assertIn("# Table 3: P1 MiniMax Post-Fix Smoke", md_text)
            self.assertIn("flowfence_lite_subset", md_text)
            self.assertIn("prompt_filter_subset", md_text)

            boundary_text = (output_dir / "table_5_evidence_boundaries.md").read_text(encoding="utf-8")
            self.assertIn("Not yet done: non-MiniMax providers", boundary_text)
            self.assertIn("unsupported", boundary_text.lower())

            all_output = "\n".join(path.read_text(encoding="utf-8") for path in output_dir.iterdir() if path.is_file())
            forbidden = [
                "$4800",
                "supplier breach investigation",
                "CUST-8831-PRIVATE",
                "sk-internal-demo-token",
            ]
            for marker in forbidden:
                self.assertNotIn(marker, all_output)

    def test_help_and_strict_mode(self):
        help_result = subprocess.run(
            [sys.executable, str(SCRIPT), "--help"],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(help_result.returncode, 0)
        self.assertIn("--output-dir", help_result.stdout)

        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "strict_tables"
            strict_result = self.run_export(output_dir, strict=True)
            self.assertEqual(strict_result.returncode, 0, strict_result.stderr + strict_result.stdout)


if __name__ == "__main__":
    unittest.main()
