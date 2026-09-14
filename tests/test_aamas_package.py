"""Reporting must use raw evidence and packaging must exclude private artifacts."""
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.package_aamas2027 import allowed_artifact, build_bundle, compare_pairs, generate_reports, llm_evidence, table_groups
from src.runtime.policy import default_secret_policies


def write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row) + "\n" for row in rows))


def episode(defense="ifc_safeview", **changes):
    row = dict(run_id="run_" + defense, task_id="task_1", scenario_id="enterprise_assistant_001",
               topology="chain_4", condition="clean", attack="none", seed=1, defense=defense,
               status="complete", success=True, privacy_safe_success=True, raw_exposure=0,
               external_exposure=0, exposure_recipient_pairs=0, intervention_count=1,
               blocks=0, rewrites=1, quarantines=0, llm_calls=0, input_tokens=0, output_tokens=0)
    return {**row, **changes}


class AamasPackageTests(unittest.TestCase):
    def test_reports_rebuild_from_raw_not_existing_summary(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "artifacts/aamas2027"
            folder = root / "E0_equal_capability/formal"
            write_jsonl(folder / "episodes.jsonl", [episode(), episode("flowfence_lite_nonoracle", intervention_count=2)])
            (folder / "summary.json").write_text(json.dumps({"episode_count": 99999, "success": 0}))
            report = generate_reports(root)
            self.assertEqual(report["counts"]["E0"]["episodes"], 2)
            table = json.loads((root / "tables/table_a_deterministic.json").read_text())
            self.assertTrue(all(row["success"] == 1 for row in table))
            pair = next(r for r in report["e0_pairs"] if r["metric"] == "intervention_count")
            self.assertEqual((pair["better"], pair["tie"], pair["worse"]), (0, 0, 1))
            self.assertNotIn("99999", (root / "PAPER_INTEGRATION.md").read_text())

    def test_dry_run_never_becomes_formal_llm_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_jsonl(root / "episodes.jsonl", [episode(agent_backend="deterministic_wiring_fixture", model_version="dry-run-fixture", llm_calls=3)])
            (root / "registration.json").write_text(json.dumps({"dry_run": True}))
            report = llm_evidence(root)
            self.assertEqual(report["episodes"], 0)
            self.assertEqual(report["llm_calls"], 0)
            self.assertEqual(report["diagnostic_fixture_rows"], 1)

    def test_all_api_attempts_counted_but_retry_does_not_replace_first_result(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first = episode(status="failed", success=False, attempt=1, llm_calls=1)
            retry = episode(run_id="retry", status="completed", success=True, attempt=2, retry_of=first["run_id"], llm_calls=1)
            write_jsonl(root / "episodes.jsonl", [first, retry])
            write_jsonl(root / "call_attempts.jsonl", [dict(call_id="call1", status="started"), dict(call_id="call1", status="failed"), dict(call_id="call2", status="started"), dict(call_id="call2", status="completed")])
            report = llm_evidence(root)
            self.assertEqual(report["llm_calls"], 2)
            self.assertEqual(report["primary_episodes"], 1)
            self.assertFalse(report["primary"][0]["success"])
            self.assertEqual(report["failed_call_attempts"], 1)
            self.assertEqual(report["linked_retry_episodes"], 1)

    def test_incomplete_privacy_is_unavailable_not_zero_leakage_win(self):
        rows = [episode(raw_exposure=2), episode("flowfence_lite_nonoracle", status="failed", success=False, privacy_safe_success=False, privacy_measurement_complete=False)]
        summary = {r["metric"]: r for r in compare_pairs(rows, ("task_id", "topology", "condition", "seed"))}
        self.assertEqual(summary["raw_exposure"]["unavailable"], 1)
        self.assertEqual(summary["raw_exposure"]["better"], 0)
        self.assertEqual(summary["success"]["worse"], 1)

    def test_all_forbidden_api_attempts_are_blocked_and_measurements_unavailable(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            rows = [episode(status="failed", error_type="HTTP_403", success=False, privacy_safe_success=False,
                            privacy_measurement_complete=False, llm_calls=1)]
            write_jsonl(root / "episodes.jsonl", rows)
            evidence = llm_evidence(root)
            self.assertEqual(evidence["status"], "BLOCKED")
            grouped = table_groups(rows, ("defense",), ("success", "raw_exposure", "intervention_count"))[0]
            self.assertEqual(grouped["success"], 0)
            self.assertEqual(grouped["privacy_complete_episodes"], 0)
            self.assertIsNone(grouped["raw_exposure"])
            self.assertIsNone(grouped["intervention_count"])

    def test_complete_registered_execution_retains_failure_and_partial_measurement(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            config = {"task_ids": ["task_1", "task_2"], "topologies": ["chain_4"],
                      "conditions": ["clean"], "defenses": ["ifc_safeview"], "seeds": [1]}
            (root / "registration.json").write_text(json.dumps({"dry_run": False, "config": config}))
            successful = episode(status="completed", llm_calls=3)
            failed = episode(run_id="run_failed", task_id="task_2", status="failed", success=False,
                             privacy_safe_success=False, privacy_measurement_complete=False, llm_calls=1)
            write_jsonl(root / "episodes.jsonl", [successful])
            self.assertEqual(llm_evidence(root)["status"], "PARTIAL")
            write_jsonl(root / "episodes.jsonl", [successful, failed])
            evidence = llm_evidence(root)
            self.assertEqual(evidence["status"], "COMPLETE")
            self.assertEqual(evidence["expected_primary_episodes"], 2)
            self.assertEqual(evidence["registered_terminal_episodes"], 2)
            self.assertEqual(evidence["completed_model_episodes"], 1)
            self.assertEqual(evidence["failed_episodes"], 1)
            self.assertEqual(evidence["measurement_coverage"], 0.5)

    def test_audit_storage_uses_actual_serialized_record_bytes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            row = episode()
            write_jsonl(root / "episodes.jsonl", [row])
            write_jsonl(root / "events.jsonl", [{"run_id": row["run_id"], "event_id": "event_1"}])
            evidence = llm_evidence(root)
            self.assertEqual(evidence["audit_storage_total_bytes"], sum(p.stat().st_size for p in root.glob("*.jsonl")))

    def test_final_review_and_inference_artifacts_allowed_but_private_not(self):
        for relative in ("E1_llm_agents/formal/summary_with_intervals.json", "logs/pilot_audit.json", "logs/full_regression.xml", "E1_llm_agents/E1_INDEPENDENT_REVIEW.md"):
            self.assertTrue(allowed_artifact(Path(relative)))
        self.assertFalse(allowed_artifact(Path("E1_llm_agents/formal/full_response.json")))

    def test_bundle_includes_replay_dependency_and_excludes_private_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            root = repo / "artifacts/aamas2027"
            root.mkdir(parents=True)
            (root / "MANIFEST.json").write_text("{}")
            (root / "TEST_REPORT.md").write_text("1 passed, 0 failed, 0 skipped")
            dependency = repo / "src/runtime/policy.py"
            dependency.parent.mkdir(parents=True)
            dependency.write_text("# Public synthetic fixture: " + default_secret_policies()[0].raw_value)
            for relative in ("src/experiments/aamas_paired.py", "scripts/summarize_aamas_llm_agents.py", "configs/experiment/aamas2027/e1_second_model_kimi.json"):
                path = repo / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("{}" if path.suffix == ".json" else "# Reproduction dependency\n")
            write_jsonl(root / "E1_llm_agents/formal/episodes.jsonl", [episode()])
            for relative in (".env", "E1_llm_agents/formal/full_response.json", "E1_llm_agents/formal/private_prompt.txt", "private/secret.json", "unrelated_wine_archive.zip"):
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("private content must never enter ZIP")
            target = repo / "bundle.zip"
            result = build_bundle(repo, root, target)
            with zipfile.ZipFile(target) as archive:
                names = archive.namelist()
                self.assertIn("src/runtime/policy.py", names)
                self.assertIn("src/experiments/aamas_paired.py", names)
                self.assertIn("scripts/summarize_aamas_llm_agents.py", names)
                self.assertIn("configs/experiment/aamas2027/e1_second_model_kimi.json", names)
                self.assertIn("artifacts/aamas2027/E1_llm_agents/formal/episodes.jsonl", names)
                self.assertFalse(any("full_response" in n or "private" in n or n.endswith(".env") or "wine_archive" in n for n in names))
                self.assertEqual(result["files"], len(names))

    def test_raw_protected_value_in_safe_result_rejects_bundle_without_echo(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            root = repo / "artifacts/aamas2027"
            root.mkdir(parents=True)
            (root / "MANIFEST.json").write_text("{}")
            (root / "TEST_REPORT.md").write_text("tests passed")
            secret = default_secret_policies()[0].raw_value
            write_jsonl(root / "E1_llm_agents/formal/events.jsonl", [{"unsafe_text": secret}])
            with self.assertRaises(ValueError) as raised:
                build_bundle(repo, root, repo / "bundle.zip")
            self.assertNotIn(secret, str(raised.exception))
            self.assertFalse((repo / "bundle.zip").exists())


if __name__ == "__main__":
    unittest.main()
