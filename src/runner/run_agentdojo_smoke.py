import argparse
import json
import os
import sys
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

import yaml

from src.common.provider_loader import apply_openai_compatible_env


def _load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def _as_rate(values: dict[tuple[str, str], bool]) -> float | None:
    if not values:
        return None
    return sum(bool(value) for value in values.values()) / len(values)


def _as_tuple(config: dict, plural_key: str, singular_key: str) -> tuple[str, ...]:
    values = config.get(plural_key)
    if values is None:
        values = [config[singular_key]]
    if isinstance(values, str):
        values = [values]
    return tuple(values)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a minimal AgentDojo smoke workflow")
    parser.add_argument("--config", default="configs/experiment/agentdojo_smoke.yaml")
    parser.add_argument("--run-name", default=None)
    args = parser.parse_args()

    repo_root = Path.cwd()
    config_path = repo_root / args.config
    config = _load_yaml(config_path)
    run_name = args.run_name or config["run_name"]
    user_tasks = _as_tuple(config, "user_tasks", "user_task")
    injection_tasks = _as_tuple(config, "injection_tasks", "injection_task")

    results_root = repo_root / config.get("results_root", "results")
    run_dir = results_root / run_name
    run_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "runner": "src/runner/run_agentdojo_smoke.py",
        "config": args.config,
        "run_name": run_name,
        "agentdojo_root": config["agentdojo_root"],
        "provider_profile": config["provider_profile"],
        "suite": config["suite"],
        "user_tasks": list(user_tasks),
        "injection_tasks": list(injection_tasks),
        "attack": config["attack"],
        "defense": config.get("defense"),
        "model_name_alias": config.get("model_name_alias"),
    }
    _write_text(run_dir / "manifest.json", json.dumps(manifest, indent=2))
    _write_text(run_dir / "resolved_config.yaml", yaml.safe_dump(dict(config), sort_keys=False))

    agentdojo_root = repo_root / config["agentdojo_root"]
    sys.path.insert(0, str(agentdojo_root / "src"))
    sys.path.insert(0, str(repo_root))

    env = apply_openai_compatible_env(
        env={},
        env_path=str(repo_root / config["provider_env"]),
        profile=config["provider_profile"],
    )
    for key, value in env.items():
        if value is not None:
            os.environ[key] = value

    from agentdojo.models import ModelsEnum
    from agentdojo.models import MODEL_NAMES
    from agentdojo.scripts.benchmark import benchmark_suite
    from agentdojo.task_suite.load_suites import get_suite

    if config.get("model_name_alias"):
        MODEL_NAMES[env["OPENAI_MODEL"]] = config["model_name_alias"]

    suite = get_suite(config.get("benchmark_version", "v1.2.2"), config["suite"])
    model = ModelsEnum(config["model"])
    logdir = run_dir / "agentdojo_runs"
    stdout_path = run_dir / "stdout.log"
    stderr_path = run_dir / "stderr.log"

    return_code = 0
    error_message = None
    results = None

    with stdout_path.open("w", encoding="utf-8") as stdout_file, stderr_path.open("w", encoding="utf-8") as stderr_file:
        try:
            with redirect_stdout(stdout_file), redirect_stderr(stderr_file):
                results = benchmark_suite(
                    suite=suite,
                    model=model,
                    logdir=logdir,
                    force_rerun=bool(config.get("force_rerun", False)),
                    benchmark_version=config.get("benchmark_version", "v1.2.2"),
                    user_tasks=user_tasks,
                    injection_tasks=injection_tasks,
                    attack=config.get("attack"),
                    defense=config.get("defense"),
                )
        except Exception as exc:  # noqa: BLE001
            return_code = 1
            error_message = f"{type(exc).__name__}: {exc}"
            stderr_file.write(error_message + "\n")

    metrics = {
        "status": "ok" if return_code == 0 else "failed",
        "return_code": return_code,
        "provider_profile": config["provider_profile"],
        "resolved_model_name": env["OPENAI_MODEL"],
        "suite": config["suite"],
        "user_tasks": list(user_tasks),
        "injection_tasks": list(injection_tasks),
        "attack": config["attack"],
        "defense": config.get("defense"),
        "model_name_alias": config.get("model_name_alias"),
    }

    if results is not None:
        metrics["utility_rate"] = _as_rate(results["utility_results"])
        metrics["security_rate"] = _as_rate(results["security_results"])
        metrics["injection_task_utility_rate"] = _as_rate(results["injection_tasks_utility_results"])
        metrics["utility_results"] = {
            f"{user_task}|{injection_task}": value
            for (user_task, injection_task), value in results["utility_results"].items()
        }
        metrics["security_results"] = {
            f"{user_task}|{injection_task}": value
            for (user_task, injection_task), value in results["security_results"].items()
        }
        metrics["injection_tasks_utility_results"] = results["injection_tasks_utility_results"]
    if error_message is not None:
        metrics["error"] = error_message

    _write_text(run_dir / "metrics.json", json.dumps(metrics, indent=2))
    _write_text(run_dir / "status.txt", ("success" if return_code == 0 else f"failed:{return_code}") + "\n")
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
