import unittest

from src.defenses.mas_flowfence import inspect_mas_event
from src.runtime.policy import default_secret_policies
from src.runtime.topology import get_topology


class NonOracleFlowFenceTest(unittest.TestCase):
    def inspect(self, applied: bool, mode: str = "flowfence_lite_nonoracle"):
        return inspect_mas_event(
            defense_mode=mode,
            event_type="MEMORY_WRITE",
            actor_id="planner_agent",
            recipient_id="doc_writer_agent",
            channel="shared_raw",
            target_zone="shared_raw",
            content="Project note: delivery remains active. No unsafe text here.",
            topology=get_topology("blackboard_4"),
            secret_policies=default_secret_policies(),
            attack_annotation={"applied": applied, "attack_id": "summary_poisoning_direct", "attack_mode": "direct"},
        )

    def test_nonoracle_ignores_attack_annotation_applied(self):
        false_result = self.inspect(False)
        true_result = self.inspect(True)
        self.assertEqual(false_result.decision["decision"], true_result.decision["decision"])
        self.assertEqual(false_result.decision["risk_score"], true_result.decision["risk_score"])
        self.assertFalse(true_result.decision["oracle_annotation_used"])
        self.assertFalse(true_result.policy_decision["metadata"]["oracle_annotation_used"])

    def test_default_flowfence_uses_attack_annotation(self):
        false_result = self.inspect(False, mode="flowfence_lite")
        true_result = self.inspect(True, mode="flowfence_lite")
        self.assertNotEqual(false_result.decision["decision"], true_result.decision["decision"])
        self.assertTrue(true_result.decision["oracle_annotation_used"])

    def test_no_semantic_pattern_ablation_metadata(self):
        result = self.inspect(True, mode="flowfence_lite_nonoracle_no_semantic_patterns")
        self.assertFalse(result.decision["oracle_annotation_used"])
        self.assertFalse(result.decision["semantic_patterns_enabled"])
        self.assertFalse(result.policy_decision["metadata"]["semantic_patterns_enabled"])


if __name__ == "__main__":
    unittest.main()
