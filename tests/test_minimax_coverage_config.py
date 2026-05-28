import subprocess
import sys
import tempfile
import unittest
import os
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
COVERAGE_CONFIG = REPO_ROOT / "configs" / "experiment" / "mas_p1_minimax_coverage.yaml"
COVERAGE_3SEED_CONFIG = REPO_ROOT / "configs" / "experiment" / "mas_p1_minimax_coverage_3seed.yaml"


def run_count(config: dict) -> int:
    total = 1
    for key in ["topology", "attack", "defense", "seed"]:
        total *= len(config[key])
    return total


class MiniMaxCoverageConfigTest(unittest.TestCase):
    def test_coverage_config_shape(self):
        self.assertTrue(COVERAGE_CONFIG.exists())
        config = yaml.safe_load(COVERAGE_CONFIG.read_text(encoding="utf-8"))
        self.assertEqual(config["provider"], "minimax")
        self.assertTrue(config["provider_calls_enabled"])
        self.assertEqual(config["agent_backend"], "minimax_final_writer")
        self.assertEqual(run_count(config), 84)
        self.assertEqual(config["topology"], ["chain_4", "star_4", "blackboard_4"])
        self.assertEqual(
            config["attack"],
            [
                "none",
                "summary_poisoning_direct",
                "summary_poisoning_indirect",
                "workspace_poisoning_direct",
                "workspace_poisoning_indirect",
                "comm_hijack_direct",
                "comm_hijack_indirect",
            ],
        )
        self.assertEqual(config["defense"], ["none", "static_acl", "prompt_filter", "flowfence_lite"])
        self.assertEqual(config["seed"], [1])

    def test_coverage_3seed_config_shape(self):
        self.assertTrue(COVERAGE_3SEED_CONFIG.exists())
        config = yaml.safe_load(COVERAGE_3SEED_CONFIG.read_text(encoding="utf-8"))
        self.assertEqual(config["provider"], "minimax")
        self.assertTrue(config["provider_calls_enabled"])
        self.assertEqual(config["agent_backend"], "minimax_final_writer")
        self.assertEqual(config["topology"], ["chain_4", "star_4", "blackboard_4"])
        self.assertEqual(
            config["attack"],
            [
                "none",
                "summary_poisoning_direct",
                "summary_poisoning_indirect",
                "workspace_poisoning_direct",
                "workspace_poisoning_indirect",
                "comm_hijack_direct",
                "comm_hijack_indirect",
            ],
        )
        self.assertEqual(config["defense"], ["none", "static_acl", "prompt_filter", "flowfence_lite"])
        self.assertEqual(config["seed"], [1, 2, 3])
        self.assertEqual(run_count(config), 252)

    def test_sweep_refuses_provider_calls_without_allow_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ)
            env["PYTHONPATH"] = str(REPO_ROOT)
            result = subprocess.run(
                [
                    sys.executable,
                    "src/runner/sweep_mas.py",
                    "--config",
                    str(COVERAGE_CONFIG),
                    "--output-root",
                    str(Path(tmp) / "coverage_safety"),
                    "--max-runs",
                    "1",
                ],
                cwd=REPO_ROOT,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--allow-provider-calls", result.stderr + result.stdout)

    def test_no_non_minimax_provider_names_in_configs(self):
        forbidden = ["openai", "anthropic", "gemini", "qwen", "vllm"]
        for path in [COVERAGE_CONFIG, COVERAGE_3SEED_CONFIG]:
            text = path.read_text(encoding="utf-8").lower()
            for name in forbidden:
                self.assertNotIn(name, text)


if __name__ == "__main__":
    unittest.main()
