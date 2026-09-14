import copy
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from src.defenses.mas_flowfence import inspect_mas_event
from src.experiments.aamas_equal import EqualMediationRunner, aggregate_events, execute_episode, paired_summary, validate_config
from src.runtime.policy import default_secret_policies
from src.runtime.topology import get_topology


class EqualCapabilityTests(unittest.TestCase):
    def inspect(self, mode="ifc_safeview", content=None, **changes):
        args = dict(defense_mode=mode, event_type="SEND_MESSAGE", actor_id="finance_agent",
                    recipient_id="finance_agent", channel="internal_message", target_zone="internal_message",
                    content=content or "Budget " + default_secret_policies()[0].raw_value,
                    topology=get_topology("blackboard_4"), secret_policies=default_secret_policies(),
                    attack_annotation={"applied": True})
        return inspect_mas_event(**{**args, **changes})

    def test_authorized_raw_allowed_despite_attack_labels_and_fanout(self):
        result = self.inspect()
        self.assertEqual(result.decision["decision"], "allow")
        self.assertEqual(result.decision["risk_score"], 0)
        self.assertFalse(result.decision["oracle_annotation_used"])
        self.assertNotIn("features", result.policy_decision["metadata"])

    def test_all_real_event_types_enforce_recipient_policy(self):
        for event in ["MEMORY_WRITE", "MEMORY_READ", "WORKSPACE_WRITE", "WORKSPACE_READ", "SEND_MESSAGE", "TOOL_CALL", "FINAL_OUTPUT"]:
            result=self.inspect(event_type=event, recipient_id="external_vendor_agent")
            self.assertEqual(result.decision["decision"], "rewrite_safe_view")
            self.assertNotIn(default_secret_policies()[0].raw_value,result.content)

    def test_forbidden_channel_overrides_authorized_reader(self):
        self.assertEqual(self.inspect(channel="shared_doc").decision["decision"], "rewrite_safe_view")

    def test_absent_recipient_fails_closed_for_raw(self):
        self.assertEqual(self.inspect(recipient_id=None).decision["decision"], "rewrite_safe_view")

    def test_shared_generator_and_validator_rejection(self):
        for mode in ["ifc_safeview", "flowfence_lite_nonoracle"]:
            with patch("src.defenses.mas_flowfence.validate_safe_view", return_value=False):
                result=self.inspect(mode, recipient_id="external_vendor_agent")
                self.assertEqual(result.decision["decision"], "block")
            with patch("src.defenses.mas_flowfence.coarse_safe_view", return_value="approved public view") as generator:
                result=self.inspect(mode, recipient_id="external_vendor_agent")
                self.assertEqual(result.content,"approved public view")
                generator.assert_called_once()

    def test_baseline_does_not_inspect_semantic_or_topology_features(self):
        class NoTopology:
            def fanout(self, actor): raise AssertionError("IFC accessed topology")
            @property
            def is_blackboard_enabled(self): raise AssertionError("IFC accessed topology")
        with patch("src.defenses.mas_flowfence.contains_sensitive_detail_request", side_effect=AssertionError("semantic risk used")):
            result=self.inspect(content="preserve exact operational details",topology=NoTopology())
        self.assertEqual(result.decision["decision"],"allow")

    def config(self, defense="ifc_safeview"):
        config=json.loads(Path("configs/experiment/aamas2027/e0_equal.json").read_text())
        config.update(topology="blackboard_4",attack="workspace_poisoning_indirect",seed=1,defense=defense,run_name="unit")
        return config

    def test_same_inputs_registry_and_final_rule(self):
        a,b=EqualMediationRunner(self.config()),EqualMediationRunner(self.config("flowfence_lite_nonoracle"))
        self.assertEqual(a._shared_seed_content(),b._shared_seed_content())
        self.assertEqual(a.secrets,b.secrets)
        self.assertEqual(a._safe_vendor_update(),b._safe_vendor_update())
        self.assertEqual(a._leaky_vendor_update(),b._leaky_vendor_update())
        ar,ae=a.run_equal();br,be=b.run_equal()
        self.assertEqual(ar['success'],br['success'])
        self.assertEqual(ar['raw_exposure'],0)
        self.assertEqual(br['raw_exposure'],0)
        self.assertTrue(all(not e['oracle_annotation_used'] for e in ae+be))

    def test_postmediation_untruncated_measurement_and_recomputation(self):
        runner=EqualMediationRunner(self.config("none"))
        secret=runner.secrets[0]
        runner.deliver("x"*500+secret.raw_value,event_type="SEND_MESSAGE",channel="external_message",actor="finance_agent",recipient="external_vendor_agent")
        self.assertEqual(aggregate_events(runner.audit)['raw_exposure'],1)
        encoded=json.dumps(runner.audit)
        self.assertNotIn(secret.raw_value,encoded)
        runner=EqualMediationRunner(self.config())
        row,events=runner.run_equal()
        for k,v in aggregate_events(events).items(): self.assertEqual(row[k],v)
        self.assertTrue(all(e['exposed_secret_ids']==[] for e in events))

    def test_config_rejects_live_and_unknown_defense(self):
        config=json.loads(Path("configs/experiment/aamas2027/e0_equal.json").read_text())
        validate_config(config)
        for change in [{"provider_calls_enabled":True},{"defense":["weakened_ifc"]},{"seed":[1,1]}]:
            with self.assertRaises(ValueError):validate_config({**config,**change})

    def test_seed_pairs_not_counted_as_independent_tasks(self):
        rows=[]
        for mode in ["ifc_safeview","flowfence_lite_nonoracle"]:
            for seed in [1,2,3]:
                config=self.config(mode);config['seed']=seed
                row,_=EqualMediationRunner(config).run_equal();rows.append(row)
        summary=paired_summary(rows)
        self.assertEqual(summary['matched_groups'],3)
        self.assertEqual(summary['independent_task_count'],1)

    def test_failed_episode_is_retained_without_exception_message_payload(self):
        with patch('src.experiments.aamas_equal.inspect_mas_event',side_effect=RuntimeError('sensitive exception text')):
            row,events=execute_episode(self.config())
        self.assertEqual(row['status'],'failed')
        self.assertEqual(row['error_type'],'RuntimeError')
        self.assertNotIn('sensitive exception text',json.dumps(row))

    def test_duplicate_dimensions_rejected(self):
        config=json.loads(Path("configs/experiment/aamas2027/e0_equal.json").read_text())
        for key in ['topology','attack','defense']:
            changed=copy.deepcopy(config);changed[key].append(changed[key][0])
            with self.assertRaises(ValueError):validate_config(changed)


if __name__ == "__main__":unittest.main()
