#!/usr/bin/env python3
"""Run deterministic synthetic multi-agent propagation scenarios."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from src.runtime.orchestrator import run_and_write


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


def load_simple_yaml(path: Path) -> dict[str, Any]:
    config: dict[str, Any] = {}
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            raise ValueError(f"Unsupported YAML syntax in {path} line {line_number}: {line}")
        key, value = stripped.split(":", 1)
        config[key.strip()] = parse_scalar(value)
    return config


def resolve_output_dir(config: dict[str, Any], output_dir: Path | None) -> Path:
    if output_dir is not None:
        return output_dir
    root = Path(str(config.get("output_root", "results/mas_synthetic")))
    return root / str(config["run_name"])


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run local deterministic synthetic MAS propagation runtime.")
    parser.add_argument("--config", required=True, type=Path, help="YAML config path.")
    parser.add_argument("--output-dir", type=Path, help="Override output directory.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite a non-empty output directory.")
    parser.add_argument("--print-metrics", action="store_true", help="Print metrics JSON to stdout.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    config = load_simple_yaml(args.config)
    if config.get("provider_calls_enabled") is True and config.get("agent_backend") != "minimax_final_writer":
        print("ERROR: provider_calls_enabled=true requires agent_backend=minimax_final_writer", file=sys.stderr)
        return 2
    if config.get("provider") != "minimax":
        print("ERROR: MAS runtime configs must use provider=minimax", file=sys.stderr)
        return 2
    output_dir = resolve_output_dir(config, args.output_dir)
    metrics = run_and_write(config, output_dir, overwrite=args.overwrite, repo_root=Path.cwd())
    if args.print_metrics:
        print(json.dumps(metrics, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
