import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "export_redacted_case_studies.py"
SYNTHETIC_MARKERS = (
    "$4800",
    "supplier breach investigation",
    "CUST-8831-PRIVATE",
    "sk-internal-demo-token",
)
FORBIDDEN_OUTPUT_PHRASES = (
    "raw provider output",
    "full raw prompt",
    "events.full.jsonl content",
)


class ExportRedactedCaseStudiesTest(unittest.TestCase):
    def run_export(self, output_dir: Path, *extra_args: str) -> subprocess.CompletedProcess[str]:
        cmd = [
            sys.executable,
            str(SCRIPT),
            "--output-dir",
            str(output_dir),
            "--summary-root",
            str(REPO_ROOT / "artifacts"),
            *extra_args,
        ]
        return subprocess.run(cmd, cwd=REPO_ROOT, text=True, capture_output=True, check=True)

    def assert_outputs_are_redacted(self, output_dir: Path) -> None:
        for path in output_dir.rglob("*"):
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            for marker in SYNTHETIC_MARKERS:
                self.assertNotIn(marker, text, path)
            lowered = text.lower()
            for phrase in FORBIDDEN_OUTPUT_PHRASES:
                self.assertNotIn(phrase, lowered, path)

    def test_exports_four_summary_only_case_studies(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "case_studies"
            result = self.run_export(output_dir)

            self.assertIn("Wrote 4 redacted case studies", result.stdout)
            expected_files = {
                "README.md",
                "redacted_case_studies.md",
                "redacted_case_studies.json",
                "case_1_no_defense_workspace_leak.md",
                "case_2_prompt_filter_paraphrase_failure.md",
                "case_3_flowfence_safe_view.md",
                "case_4_nonoracle_heldout_prevention.md",
                "case_study_traceability.md",
                "case_study_review_notes.md",
            }
            self.assertEqual(expected_files, {p.name for p in output_dir.iterdir()})

            payload = json.loads((output_dir / "redacted_case_studies.json").read_text())
            self.assertEqual(4, payload["case_count"])
            self.assertFalse(payload["safe_trace_snippets_used"])
            self.assertEqual("safe trace snippets not requested", payload["safe_trace_status"])

            combined = (output_dir / "redacted_case_studies.md").read_text()
            self.assertIn("Case 1: No-defense workspace propagation leaks raw private context", combined)
            self.assertIn("Case 2: Prompt-filter misses paraphrased shared-state exfiltration", combined)
            self.assertIn("Case 3: FlowFence rewrites or quarantines risky shared-state content", combined)
            self.assertIn("Case 4: Non-oracle FlowFence contains held-out paraphrase without attack labels", combined)
            self.assertIn("MiniMax-backed multi-agent synthetic-runtime coverage experiment", combined)
            self.assertIn("targeted MiniMax-backed synthetic-runtime validation", combined)

            traceability = (output_dir / "case_study_traceability.md").read_text()
            self.assertIn("case_1_no_defense_workspace_propagation", traceability)
            self.assertIn("case_4_nonoracle_flowfence_heldout_paraphrase", traceability)
            self.assert_outputs_are_redacted(output_dir)

    def test_safe_trace_previews_are_redacted_and_truncated(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            runs_root = tmp_path / "runs"
            run_dir = runs_root / "example_run"
            run_dir.mkdir(parents=True)
            (run_dir / "meta.json").write_text('{"run_name": "example"}', encoding="utf-8")
            (run_dir / "metrics.json").write_text('{"task_success": true}', encoding="utf-8")
            (run_dir / "events.safe.jsonl").write_text(
                json.dumps(
                    {
                        "event_type": "safe_preview",
                        "safe_preview": (
                            "Do not expose $4800, supplier breach investigation, "
                            "CUST-8831-PRIVATE, or sk-internal-demo-token in final text."
                        ),
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            output_dir = tmp_path / "case_studies"
            self.run_export(
                output_dir,
                "--runs-root",
                str(runs_root),
                "--include-safe-trace-snippets",
                "--max-events",
                "1",
                "--max-preview-chars",
                "40",
            )

            payload = json.loads((output_dir / "redacted_case_studies.json").read_text())
            self.assertTrue(payload["safe_trace_snippets_used"])
            snippets = payload["cases"][0]["safe_trace_snippets"]
            self.assertEqual(1, len(snippets))
            self.assertLessEqual(len(snippets[0]["preview"]), 40)
            self.assertIn("[REDACTED_NUMERIC_LIMIT]", snippets[0]["preview"])
            self.assert_outputs_are_redacted(output_dir)

    def test_help(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--help"],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertIn("--output-dir", result.stdout)
        self.assertIn("--include-safe-trace-snippets", result.stdout)


if __name__ == "__main__":
    unittest.main()
