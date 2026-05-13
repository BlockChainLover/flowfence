import argparse
import csv
import json
import os
import subprocess
import sys
from pathlib import Path

import yaml

from src.common.provider_loader import apply_openai_compatible_env


def _load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def _build_metrics(csv_path: Path) -> dict:
    if not csv_path.exists():
        return {"status": "missing_results_csv"}

    rows = list(csv.DictReader(csv_path.open("r", encoding="utf-8")))
    total = len(rows)
    if total == 0:
        return {"status": "empty_results_csv", "rows": 0}

    def _rate(field: str) -> float:
        return sum(int(row[field]) for row in rows) / total

    return {
        "status": "ok",
        "rows": total,
        "attack_success_rate": _rate("Attack Successful"),
        "original_task_success_rate": _rate("Original Task Successful"),
        "refuse_rate": _rate("Refuse Result"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a minimal ASB smoke workflow")
    parser.add_argument("--config", default="configs/experiment/asb_smoke.yaml")
    parser.add_argument("--run-name", default=None)
    args = parser.parse_args()

    repo_root = Path.cwd()
    config_path = repo_root / args.config
    config = _load_yaml(config_path)
    run_name = args.run_name or config["run_name"]

    results_root = repo_root / config.get("results_root", "results")
    run_dir = results_root / run_name
    run_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "runner": "src/runner/run_asb_smoke.py",
        "config": args.config,
        "run_name": run_name,
        "asb_root": config["asb_root"],
        "provider_profile": config["provider_profile"],
        "judge_profile": config.get("judge_profile", config["provider_profile"]),
    }
    _write_text(run_dir / "manifest.json", json.dumps(manifest, indent=2))

    resolved_config = dict(config)
    _write_text(run_dir / "resolved_config.yaml", yaml.safe_dump(resolved_config, sort_keys=False))

    env = apply_openai_compatible_env(
        env=os.environ.copy(),
        env_path=str(repo_root / config["provider_env"]),
        profile=config["provider_profile"],
        judge_profile=config.get("judge_profile"),
    )

    resolved_model = env["OPENAI_MODEL"]
    env["PYTHONPATH"] = str(repo_root / config["asb_root"])

    asb_root = repo_root / config["asb_root"]
    result_csv = run_dir / "asb_results.csv"

    mode_to_flag = {
        "direct_prompt_injection": "--direct_prompt_injection",
        "observation_prompt_injection": "--observation_prompt_injection",
        "memory_attack": "--memory_attack",
        "clean": "--clean",
    }
    attack_mode = config["attack_mode"]
    if attack_mode not in mode_to_flag:
        raise ValueError(f"Unsupported attack_mode: {attack_mode}")

    tool_path_map = {
        "test": "data/attack_tools_test.jsonl",
        "all": "data/all_attack_tools.jsonl",
        "agg": "data/all_attack_tools_aggressive.jsonl",
        "non-agg": "data/all_attack_tools_non_aggressive.jsonl",
    }
    attacker_tools_path = config.get("attacker_tools_path")
    if attacker_tools_path is None:
        attack_tool = config["attack_tool"]
        if attack_tool not in tool_path_map:
            raise ValueError(f"Unsupported attack_tool: {attack_tool}")
        attacker_tools_path = tool_path_map[attack_tool]

    cmd = [
        sys.executable,
        "main_attacker.py",
        "--llm_name",
        resolved_model,
        "--use_backend",
        "openai_api",
        "--attack_type",
        config["attack_type"],
        "--attacker_tools_path",
        attacker_tools_path,
        "--tasks_path",
        config.get("tasks_path", "data/agent_task_test.jsonl"),
        "--tools_info_path",
        config.get("tools_info_path", "data/all_normal_tools.jsonl"),
        "--task_num",
        str(config["task_num"]),
        "--max_new_tokens",
        str(config.get("max_new_tokens", 256)),
        "--res_file",
        str(result_csv),
        mode_to_flag[attack_mode],
    ]

    defense_type = config.get("defense_type")
    if defense_type:
        cmd.extend(["--defense_type", defense_type])

    if config.get("write_db"):
        cmd.append("--write_db")
    if config.get("read_db"):
        cmd.append("--read_db")

    stdout_path = run_dir / "stdout.log"
    stderr_path = run_dir / "stderr.log"

    with stdout_path.open("w", encoding="utf-8") as stdout_file, stderr_path.open("w", encoding="utf-8") as stderr_file:
        completed = subprocess.run(
            cmd,
            cwd=asb_root,
            env=env,
            stdout=stdout_file,
            stderr=stderr_file,
            text=True,
        )

    status = "success" if completed.returncode == 0 else f"failed:{completed.returncode}"
    _write_text(run_dir / "status.txt", status + "\n")

    metrics = _build_metrics(result_csv)
    metrics["return_code"] = completed.returncode
    metrics["model_name"] = resolved_model
    metrics["provider_profile"] = config["provider_profile"]
    _write_text(run_dir / "metrics.json", json.dumps(metrics, indent=2))

    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
