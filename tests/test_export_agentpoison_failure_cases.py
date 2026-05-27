import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPORTER = REPO_ROOT / "scripts" / "export_agentpoison_failure_cases.py"
FORBIDDEN_TRAJ = "SYNTHETIC_RAW_TRAJECTORY_SHOULD_NOT_APPEAR"


def event(
    *,
    case_id: str,
    task_type: str,
    event_id: str,
    step_idx: int,
    decision: str,
    contains_poison: bool,
    detected: bool,
    exposed: bool,
    fired: bool,
    attack_manifested: bool = False,
) -> dict:
    return {
        "schema_version": "flowfence_event_v1",
        "event_id": event_id,
        "run_id": "synthetic_run",
        "case_id": case_id,
        "task_type": task_type,
        "step_idx": step_idx,
        "event_type": "MEMORY_READ",
        "channel": "retrieval_memory",
        "actor_id": "agent",
        "object_id": f"obj:{event_id}",
        "causal_parents": [],
        "payload_sha256": "abc",
        "payload_preview_redacted": f"preview for {case_id}",
        "contains_poison": contains_poison,
        "defense": {
            "decision": decision,
            "risk_score": 1.0 if fired else 0.0,
            "reason_codes": ["synthetic_reason"] if fired else [],
            "lease_signal": "synthetic",
            "defense_fired": fired,
            "rewritten_content_preview_redacted": "rewritten preview",
            "hard_blocker": fired,
        },
        "exposure": {
            "poisoned_content_detected": detected,
            "poisoned_content_exposed": exposed,
            "raw_poisoned_retrieval": contains_poison,
            "attack_manifested": attack_manifested,
            "safe_trace_redacted": False,
        },
        "metadata": {
            "safe_note": "metadata only",
        },
    }


def final_event(case_id: str, task_type: str) -> dict:
    return {
        "schema_version": "flowfence_event_v1",
        "event_id": f"{case_id}:final",
        "run_id": "synthetic_run",
        "case_id": case_id,
        "task_type": task_type,
        "step_idx": 2,
        "event_type": "FINAL_OUTPUT",
        "channel": "final_output",
        "actor_id": "agent",
        "object_id": f"answer:{case_id}",
        "causal_parents": [],
        "payload_sha256": "def",
        "payload_preview_redacted": "final output preview",
        "contains_poison": False,
        "defense": {},
        "exposure": {
            "poisoned_content_detected": False,
            "poisoned_content_exposed": False,
            "raw_poisoned_retrieval": False,
            "attack_manifested": False,
            "safe_trace_redacted": False,
        },
        "metadata": {},
    }


class ExportAgentPoisonFailureCasesTest(unittest.TestCase):
    def test_exporter_writes_reports_and_filters_detection_success(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            run_dir = tmp_path / "converted"
            out_dir = tmp_path / "report"
            run_dir.mkdir()
            events = [
                event(
                    case_id="benign_overblocked",
                    task_type="benign",
                    event_id="e1",
                    step_idx=1,
                    decision="quarantine",
                    contains_poison=False,
                    detected=False,
                    exposed=False,
                    fired=True,
                ),
                final_event("benign_overblocked", "benign"),
                event(
                    case_id="adv_exposed",
                    task_type="adv",
                    event_id="e2",
                    step_idx=1,
                    decision="allow",
                    contains_poison=True,
                    detected=False,
                    exposed=True,
                    fired=False,
                ),
                final_event("adv_exposed", "adv"),
                event(
                    case_id="adv_contained",
                    task_type="adv",
                    event_id="e3",
                    step_idx=1,
                    decision="quarantine",
                    contains_poison=True,
                    detected=True,
                    exposed=False,
                    fired=True,
                ),
                final_event("adv_contained", "adv"),
            ]
            safe_events = json.loads(json.dumps(events))
            for item in safe_events:
                item["exposure"]["safe_trace_redacted"] = True
                item["metadata"]["note"] = "safe"
            decisions = [
                {
                    "schema_version": "flowfence_policy_decision_v1",
                    "decision_id": "d1",
                    "event_id": "e1",
                    "run_id": "synthetic_run",
                    "case_id": "benign_overblocked",
                    "task_type": "benign",
                    "step_idx": 1,
                    "defense_mode": "synthetic",
                    "decision": "quarantine",
                    "risk_score": 1.0,
                    "reason_codes": ["synthetic_reason"],
                    "lease_signal": "synthetic",
                    "actions": ["quarantine"],
                    "metadata": {},
                }
            ]
            for path, rows in (
                (run_dir / "events.full.jsonl", events),
                (run_dir / "events.safe.jsonl", safe_events),
                (run_dir / "policy_decisions.jsonl", decisions),
            ):
                path.write_text("\n".join(json.dumps(row) for row in rows) + "\n")

            subprocess.run(
                [
                    sys.executable,
                    str(EXPORTER),
                    "--run-dir",
                    str(run_dir),
                    "--output-dir",
                    str(out_dir),
                    "--include-benign",
                ],
                cwd=REPO_ROOT,
                check=True,
                text=True,
                capture_output=True,
            )
            jsonl_path = out_dir / "agentpoison_failure_cases.jsonl"
            md_path = out_dir / "agentpoison_failure_cases.md"
            summary_path = out_dir / "agentpoison_failure_cases_summary.json"
            self.assertTrue(jsonl_path.exists())
            self.assertTrue(md_path.exists())
            self.assertTrue(summary_path.exists())
            rows = [json.loads(line) for line in jsonl_path.read_text().splitlines()]
            self.assertEqual(len(rows), 2)
            by_case = {row["case_id"]: row for row in rows}
            self.assertEqual(by_case["benign_overblocked"]["record_type"], "false_positive")
            self.assertEqual(by_case["benign_overblocked"]["failure_type"], "overblocking")
            self.assertEqual(by_case["adv_exposed"]["record_type"], "adversarial_failure")
            self.assertNotIn("adv_contained", by_case)
            md_text = md_path.read_text()
            self.assertIn("## Summary Counts", md_text)
            self.assertIn("## False Positives", md_text)
            self.assertIn("## Adversarial Failures", md_text)
            combined = jsonl_path.read_text() + md_text
            self.assertNotIn(FORBIDDEN_TRAJ, combined)
            self.assertNotIn('"traj"', combined)
            self.assertNotIn('"raw_observation"', combined)


if __name__ == "__main__":
    unittest.main()
