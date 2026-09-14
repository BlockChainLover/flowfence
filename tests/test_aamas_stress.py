import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.experiments.aamas_stress import (
    DEFENSES, TRANSFORMATIONS, budget_policy, evaluate_recipient_histories,
    histogram_quantile, load_config, mediate, reconstruct_history, run_overhead,
    run_semantic, summarize, transformation_payloads,
)
from src.runtime.policy import default_secret_policies


class AamasStressTests(unittest.TestCase):
    def test_formal_configuration_validation(self):
        config = load_config(Path("configs/experiment/aamas2027/e2_overhead.json"))
        self.assertEqual([1000, 10000, 100000], config["event_counts"])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            for field, value in [("event_counts", [0]), ("repetitions", 4), ("warmup_events", 0), ("defenses", ["none"])]:
                path.write_text(json.dumps({**config, field: value}))
                with self.assertRaises(ValueError):
                    load_config(path)

    def test_semantic_configuration_validation(self):
        config = load_config(Path("configs/experiment/aamas2027/e3_semantic_stress.json"))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            for field, value in [("transformations", ["T1_formatting"]), ("task_ids", ["a", "a"]), ("public_threshold_usd", 5000)]:
                path.write_text(json.dumps({**config, field: value}))
                with self.assertRaises(ValueError):
                    load_config(path)

    def test_off_control_never_calls_detector(self):
        with patch("src.experiments.aamas_stress.inspect_mas_event", side_effect=AssertionError("off called inspector")):
            result = mediate("none", {"content": "unchanged"})
        self.assertEqual(result.content, "unchanged")
        self.assertEqual(result.decision["decision"], "allow")

    def test_histogram_quantiles_are_exact_linear_interpolation(self):
        histogram = {10: 1, 20: 2, 30: 1}
        self.assertEqual(20, histogram_quantile(histogram, .5))
        self.assertAlmostEqual(28.5, histogram_quantile(histogram, .95))
        self.assertEqual(10, histogram_quantile(histogram, 0))
        self.assertEqual(30, histogram_quantile(histogram, 1))

    def test_all_formatting_recipes_are_reconstructable_and_not_exact(self):
        policy = budget_policy()
        for index in range(4):
            _, fragments = transformation_payloads("T1_formatting", index)
            self.assertNotIn(policy.raw_value, " ".join(fragments))
            self.assertEqual(["external_vendor_agent"], evaluate_recipient_histories(
                {"external_vendor_agent": fragments}, policy=policy))

    def test_split_disclosure_requires_same_recipient_observation_history(self):
        _, fragments = transformation_payloads("T2_split_history", 0)
        policy = budget_policy()
        self.assertFalse(evaluate_recipient_histories({"external_vendor_agent": fragments[:1]}, policy=policy))
        self.assertFalse(evaluate_recipient_histories({"external_vendor_agent": fragments[1:]}, policy=policy))
        self.assertFalse(evaluate_recipient_histories({"external_vendor_agent": fragments[:1], "another_unauthorized": fragments[1:]}, policy=policy))
        self.assertEqual(["external_vendor_agent"], evaluate_recipient_histories({"external_vendor_agent": fragments}, policy=policy))
        self.assertFalse(evaluate_recipient_histories({"finance_agent": fragments}, policy=policy))

    def test_derived_disclosure_needs_public_threshold(self):
        _, fragments = transformation_payloads("T3_public_threshold", 0)
        self.assertFalse(reconstruct_history(fragments))
        self.assertEqual(["external_vendor_agent"], evaluate_recipient_histories(
            {"external_vendor_agent": fragments}, policy=budget_policy(), public_threshold=4000))
        self.assertFalse(evaluate_recipient_histories(
            {"external_vendor_agent": fragments}, policy=budget_policy(), public_threshold=3000))

    def test_overhead_smoke_real_serialization_and_rebuildable_histograms(self):
        config = {"topology": "blackboard_4", "event_counts": [8, 16], "defenses": list(DEFENSES),
                  "repetitions": 1, "warmup_events": 8, "reference_task_events": 24}
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            rows = run_overhead(config, out)
            self.assertEqual(6, len(rows))
            rebuilt = summarize([json.loads(line) for line in (out / "episodes.jsonl").read_text().splitlines()], "E2")
            self.assertEqual(summarize(rows, "E2"), rebuilt)
            for row in rows:
                self.assertEqual(row["event_count"], sum(frequency for _, frequency in row["latency_histogram_ns"]))
                self.assertEqual(row["timed_ns"], sum(ns * frequency for ns, frequency in row["latency_histogram_ns"]))
            fixtures = (out / "serialized_audit_fixtures.jsonl").read_bytes()
            fixture_rows = [json.loads(line) for line in fixtures.splitlines()]
            for defense in DEFENSES:
                actual_bytes = sum(len(line) + 1 for line in fixtures.splitlines() if json.loads(line)["run_id"] == f"e2_{defense}")
                measured = next(row["audit_total_bytes"] for row in rows if row["defense"] == defense and row["event_count"] == 8)
                self.assertEqual(actual_bytes, measured)
            self.assertIn("flowfence_event_v1", {row["schema_version"] for row in fixture_rows})
            self.assertIn("flowfence_policy_decision_v1", {row["schema_version"] for row in fixture_rows})
            for secret in default_secret_policies():
                self.assertNotIn(secret.raw_value.encode(), fixtures)

    def test_semantic_matched_inputs_no_new_detector_and_no_payload_in_safe_log(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            task_path = out / "tasks.json"
            task_path.write_text(json.dumps({"tasks": [{"task_id": "e1_enterprise_01"}]}))
            config = {"task_config": str(task_path), "task_ids": ["e1_enterprise_01"],
                      "transformations": list(TRANSFORMATIONS), "defenses": list(DEFENSES), "public_threshold_usd": 4000}
            from src.experiments import aamas_stress
            original = aamas_stress.mediate
            seen = {defense: [] for defense in DEFENSES}
            def record(defense, kwargs):
                seen[defense].append((kwargs["content"], kwargs["event_type"], kwargs["recipient_id"], kwargs["secret_policies"]))
                return original(defense, kwargs)
            with patch.object(aamas_stress, "mediate", side_effect=record):
                rows = run_semantic(config, out)
            self.assertEqual(9, len(rows))
            self.assertEqual(seen["none"], seen["ifc_safeview"])
            self.assertEqual(seen["none"], seen["flowfence_lite_nonoracle"])
            self.assertTrue(all(row["measured_unauthorized_disclosure"] for row in rows))
            self.assertTrue(all(row["success"] is None for row in rows))
            for filename in ["episodes.jsonl", "safe_probe_events.jsonl"]:
                saved = (out / filename).read_text()
                for secret in default_secret_policies():
                    self.assertNotIn(secret.raw_value, saved)
                for transformation in TRANSFORMATIONS:
                    _, fragments = transformation_payloads(transformation, 0)
                    for fragment in fragments:
                        # Full scalar fragments are not stored as string payloads.
                        self.assertNotIn(json.dumps(fragment), saved)


if __name__ == "__main__":
    unittest.main()
