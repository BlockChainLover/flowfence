import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
DETERMINISTIC_CONFIG = REPO_ROOT / "configs" / "experiment" / "mas_p1_nonoracle_heldout_deterministic.yaml"
TARGETED_CONFIG = REPO_ROOT / "configs" / "experiment" / "mas_p1_minimax_nonoracle_heldout_targeted.yaml"


def run_count(config: dict) -> int:
    total = 1
    for key in ["topology", "attack", "defense", "seed"]:
        total *= len(config[key])
    return total


class NonOracleHeldoutConfigTest(unittest.TestCase):
    def test_deterministic_config(self):
        config = yaml.safe_load(DETERMINISTIC_CONFIG.read_text(encoding="utf-8"))
        self.assertEqual(run_count(config), 540)
        self.assertEqual(config["provider"], "minimax")
        self.assertFalse(config["provider_calls_enabled"])
        self.assertEqual(config["agent_backend"], "scripted_deterministic")
        self.assertEqual(config["seed"], [1, 2, 3])
        self.assertIn("flowfence_lite_nonoracle", config["defense"])
        self.assertIn("flowfence_lite_nonoracle_no_semantic_patterns", config["defense"])

    def test_targeted_minimax_config(self):
        config = yaml.safe_load(TARGETED_CONFIG.read_text(encoding="utf-8"))
        self.assertEqual(run_count(config), 72)
        self.assertEqual(config["provider"], "minimax")
        self.assertTrue(config["provider_calls_enabled"])
        self.assertEqual(config["agent_backend"], "minimax_final_writer")
        self.assertEqual(
            config["attack"],
            ["summary_poisoning_paraphrase", "workspace_poisoning_paraphrase", "comm_hijack_paraphrase"],
        )
        self.assertIn("flowfence_lite_nonoracle", config["defense"])
        self.assertNotIn("flowfence_lite", [d for d in config["defense"] if d != "flowfence_lite_nonoracle"])

    def test_no_other_provider_names(self):
        forbidden = ["openai", "anthropic", "gemini", "qwen", "vllm"]
        text = (DETERMINISTIC_CONFIG.read_text(encoding="utf-8") + TARGETED_CONFIG.read_text(encoding="utf-8")).lower()
        for provider in forbidden:
            self.assertNotIn(provider, text)


if __name__ == "__main__":
    unittest.main()
