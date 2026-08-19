#!/usr/bin/env python3
"""Run the deterministic synthetic MAS matrix without provider calls."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from itertools import product
from pathlib import Path
from typing import Any

from src.runtime.minimax_client import MiniMaxClient
from src.runtime.orchestrator import run_and_write


STATUS_SCHEMA_VERSION = "flowfence_mas_p1_sweep_status_v1"


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if value.lower() == "null":
        return None
    try:
        return int(value)
    except ValueError:
        return value.strip("'\"")


def load_matrix_yaml(path: Path) -> dict[str, Any]:
    config: dict[str, Any] = {}
    current_key: str | None = None
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("-"):
            if current_key is None:
                raise ValueError(f"List item without key in {path} line {line_number}: {line}")
            config.setdefault(current_key, []).append(parse_scalar(stripped[1:].strip()))
            continue
        if ":" not in stripped:
            raise ValueError(f"Unsupported YAML syntax in {path} line {line_number}: {line}")
        key, value = stripped.split(":", 1)
        current_key = key.strip()
        if value.strip():
            config[current_key] = parse_scalar(value)
            current_key = None
        else:
            config[current_key] = []
    return config


def as_list(config: dict[str, Any], key: str) -> list[Any]:
    value = config.get(key)
    if isinstance(value, list):
        return value
    if value is None:
        raise ValueError(f"Missing matrix key: {key}")
    return [value]


def run_name(task_id: str, topology: str, attack: str, defense: str, seed: int) -> str:
    return f"mas_p1__{task_id}__{topology}__{attack}__{defense}__seed{seed}"


def expand_runs(config: dict[str, Any]) -> list[dict[str, Any]]:
    if config.get("provider") != "minimax":
        raise ValueError("P1 deterministic MAS sweep requires provider: minimax")
    provider_calls_enabled = bool(config.get("provider_calls_enabled"))
    no_llm_api_required = bool(config.get("no_llm_api_required"))
    if no_llm_api_required and provider_calls_enabled:
        raise ValueError("no_llm_api_required=true forbids provider_calls_enabled=true")
    agent_backend = str(config.get("agent_backend", "scripted_deterministic"))
    if provider_calls_enabled and agent_backend != "minimax_final_writer":
        raise ValueError("provider_calls_enabled=true requires agent_backend: minimax_final_writer")
    if not provider_calls_enabled and agent_backend != "scripted_deterministic":
        raise ValueError("provider_calls_enabled=false requires agent_backend: scripted_deterministic")

    task_id = str(config["task_id"])
    runs: list[dict[str, Any]] = []
    for topology, attack, defense, seed in product(
        as_list(config, "topology"),
        as_list(config, "attack"),
        as_list(config, "defense"),
        as_list(config, "seed"),
    ):
        seed_int = int(seed)
        row = {
            "run_name": run_name(task_id, str(topology), str(attack), str(defense), seed_int),
            "task_file": str(config["task_file"]),
            "task_id": task_id,
            "topology": str(topology),
            "attack": str(attack),
            "defense": str(defense),
            "agent_backend": agent_backend,
            "provider": "minimax",
            "provider_calls_enabled": provider_calls_enabled,
            "no_llm_api_required": no_llm_api_required,
            "seed": seed_int,
            "output_root": str(config.get("output_root", "results/mas_synthetic_p1")),
            "temperature": config.get("temperature", 0.0),
            "max_tokens": config.get("max_tokens", 256),
            "timeout_seconds": config.get("timeout_seconds", 60),
        }
        runs.append(row)
    return runs


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_status(path: Path, status: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(status, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run deterministic MAS P1 sweep without provider calls.")
    parser.add_argument("--config", required=True, type=Path, help="Matrix config path.")
    parser.add_argument("--output-root", type=Path, help="Override output root.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing run directories.")
    parser.add_argument("--max-runs", type=int, help="Run only the first N expanded configs.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned runs and do not execute.")
    parser.add_argument("--status-path", type=Path, help="Status JSON path.")
    parser.add_argument("--allow-provider-calls", action="store_true", help="Allow MiniMax provider calls for smoke configs.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        matrix = load_matrix_yaml(args.config)
        runs = expand_runs(matrix)
    except Exception as exc:
        print(f"ERROR: invalid matrix config {args.config}: {exc}", file=sys.stderr)
        return 2

    if args.max_runs is not None:
        runs = runs[: args.max_runs]
    output_root = args.output_root or Path(str(matrix.get("output_root", "results/mas_synthetic_p1")))
    status_path = args.status_path or Path("artifacts/mas_p1_deterministic_matrix/status.json")
    provider_calls_enabled = bool(matrix.get("provider_calls_enabled"))

    print(f"Expected runs: {len(runs)}")
    if provider_calls_enabled and not args.allow_provider_calls:
        print("ERROR: provider_calls_enabled=true requires --allow-provider-calls before any MiniMax request", file=sys.stderr)
        return 2
    if provider_calls_enabled:
        client = MiniMaxClient(
            timeout_seconds=float(matrix.get("timeout_seconds", 60)),
            temperature=float(matrix.get("temperature", 0.0)),
            max_tokens=int(matrix.get("max_tokens", 256)),
        )
        if not client.available():
            print(
                "ERROR: MiniMax credentials unavailable; missing: " + ", ".join(client.missing_variables()),
                file=sys.stderr,
            )
            return 2

    if args.dry_run:
        for row in runs:
            print(row["run_name"])
        return 0

    started_at = utc_now()
    status: dict[str, Any] = {
        "schema_version": STATUS_SCHEMA_VERSION,
        "matrix_config": str(args.config),
        "output_root": str(output_root),
        "expected_runs": len(runs),
        "completed_runs": 0,
        "skipped_runs": 0,
        "failed_runs": 0,
        "current_run": None,
        "started_at": started_at,
        "updated_at": started_at,
        "provider": matrix.get("provider"),
        "provider_calls_enabled": provider_calls_enabled,
        "no_llm_api_required": bool(matrix.get("no_llm_api_required")),
        "failures": [],
    }
    write_status(status_path, status)

    for row in runs:
        run_dir = output_root / row["run_name"]
        status["current_run"] = row["run_name"]
        status["updated_at"] = utc_now()
        write_status(status_path, status)
        if (run_dir / "metrics.json").exists() and not args.force:
            status["skipped_runs"] += 1
            status["updated_at"] = utc_now()
            write_status(status_path, status)
            continue
        try:
            if args.force and run_dir.exists():
                shutil.rmtree(run_dir)
            run_and_write(row, run_dir, overwrite=args.force, repo_root=Path.cwd())
            status["completed_runs"] += 1
        except Exception as exc:
            status["failed_runs"] += 1
            status["failures"].append({"run_name": row["run_name"], "error": str(exc)})
        status["updated_at"] = utc_now()
        write_status(status_path, status)

    status["current_run"] = None
    status["updated_at"] = utc_now()
    write_status(status_path, status)
    if status["failed_runs"]:
        print(json.dumps(status, indent=2, sort_keys=True), file=sys.stderr)
        return 1
    print(json.dumps(status, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
