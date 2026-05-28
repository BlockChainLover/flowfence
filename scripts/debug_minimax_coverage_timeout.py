#!/usr/bin/env python3
"""Diagnose the timed-out MiniMax MAS coverage run using high-level artifacts."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from itertools import product
from pathlib import Path
from typing import Any

import yaml


RAW_SECRET_MARKERS = [
    "$4800",
    "supplier breach investigation",
    "CUST-8831-PRIVATE",
    "sk-internal-demo-token",
]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def read_config(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else [value]


def run_name(task_id: str, topology: str, attack: str, defense: str, seed: int) -> str:
    return f"mas_p1__{task_id}__{topology}__{attack}__{defense}__seed{seed}"


def expand_expected(config: dict[str, Any]) -> list[dict[str, Any]]:
    task_id = str(config["task_id"])
    runs = []
    for topology, attack, defense, seed in product(
        as_list(config["topology"]),
        as_list(config["attack"]),
        as_list(config["defense"]),
        as_list(config["seed"]),
    ):
        seed_int = int(seed)
        name = run_name(task_id, str(topology), str(attack), str(defense), seed_int)
        runs.append(
            {
                "run_name": name,
                "task_id": task_id,
                "topology": str(topology),
                "attack": str(attack),
                "defense": str(defense),
                "seed": seed_int,
            }
        )
    return runs


def parse_run_name(name: str) -> dict[str, Any] | None:
    parts = name.split("__")
    if len(parts) != 6 or parts[0] != "mas_p1":
        return None
    seed_text = parts[5]
    if not seed_text.startswith("seed"):
        return None
    try:
        seed = int(seed_text.removeprefix("seed"))
    except ValueError:
        return None
    return {
        "run_name": name,
        "task_id": parts[1],
        "topology": parts[2],
        "attack": parts[3],
        "defense": parts[4],
        "seed": seed,
    }


def completed_from_runs_root(runs_root: Path) -> set[str]:
    if not runs_root.exists():
        return set()
    return {metrics_path.parent.name for metrics_path in runs_root.rglob("metrics.json")}


def redact_text(text: str) -> str:
    out = text
    for marker in RAW_SECRET_MARKERS:
        out = out.replace(marker, "[REDACTED_SYNTHETIC_SECRET]")
    return out


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(redact_text(json.dumps(payload, indent=2, sort_keys=True) + "\n"), encoding="utf-8")


def diagnose(args: argparse.Namespace) -> int:
    artifact_dir = Path(args.coverage_artifact_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = artifact_dir / "run_manifest.json"
    summary_path = artifact_dir / "coverage_summary.json"
    failure_path = artifact_dir / "failure_breakdown.jsonl"
    manifest = read_json(manifest_path) if manifest_path.exists() else {}
    summary = read_json(summary_path) if summary_path.exists() else {}
    failures = read_jsonl(failure_path)
    config = read_config(Path(args.matrix_config))
    expected_runs = expand_expected(config)
    expected_by_name = {row["run_name"]: row for row in expected_runs}

    recorded_failed = manifest.get("failed_runs") or []
    recorded_failed_names = [str(row.get("run_name")) for row in recorded_failed if row.get("run_name")]
    timeout_name = recorded_failed_names[0] if recorded_failed_names else None

    completed_names: set[str] = set()
    runs_root_available = False
    if args.remote_runs_root:
        runs_root = Path(args.remote_runs_root)
        completed_names = completed_from_runs_root(runs_root)
        runs_root_available = runs_root.exists()
    missing_names = sorted(set(expected_by_name) - completed_names) if completed_names else []

    failed_name = timeout_name or (missing_names[0] if len(missing_names) == 1 else None)
    failed_config = expected_by_name.get(failed_name or "")
    if failed_config is None and failed_name:
        failed_config = parse_run_name(failed_name)

    failure_type = "unknown"
    appears_transient = False
    if recorded_failed:
        category = str(recorded_failed[0].get("error_category") or recorded_failed[0].get("error") or "")
        if "timeout" in category.lower():
            failure_type = "minimax_read_timeout"
            appears_transient = True
        elif category:
            failure_type = category

    diagnosis = {
        "schema_version": "flowfence_minimax_timeout_diagnosis_v1",
        "expected_run_count": len(expected_runs),
        "completed_run_count": summary.get("completed_run_count") or manifest.get("completed_run_count"),
        "failed_run_count": summary.get("failed_run_count") or manifest.get("failed_run_count"),
        "runs_root_available": runs_root_available,
        "completed_run_dirs_with_metrics": len(completed_names) if completed_names else None,
        "missing_runs_from_runs_root": missing_names,
        "recorded_failed_runs": recorded_failed,
        "failed_run": failed_config,
        "failure_type": failure_type,
        "appears_transient": appears_transient,
        "provider": manifest.get("provider", "minimax"),
        "provider_calls_enabled": manifest.get("provider_calls_enabled", True),
        "agent_backend": manifest.get("agent_backend", "minimax_final_writer"),
        "failure_breakdown_rows_inspected": len(failures),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "notes": "Diagnosis uses committed high-level artifacts and optional metrics.json presence only; raw traces and provider outputs are not read.",
    }

    debug_summary = {
        "schema_version": "flowfence_minimax_timeout_debug_summary_v1",
        "status": "failed_run_identified" if failed_config else "failed_run_unknown",
        "expected_run_count": len(expected_runs),
        "completed_before_retry": manifest.get("completed_run_count"),
        "failed_before_retry": manifest.get("failed_run_count"),
        "failed_run_name": failed_name,
        "failure_type": failure_type,
        "appears_transient": appears_transient,
        "recommended_retry": "rerun same sweep without --force so completed metrics.json runs are skipped" if failed_config else "manual inspection required",
        "raw_outputs_committed": False,
        "generated_at": diagnosis["generated_at"],
    }

    md_lines = [
        "# MiniMax Coverage Timeout Debug Summary",
        "",
        f"- Status: `{debug_summary['status']}`",
        f"- Expected runs: `{len(expected_runs)}`",
        f"- Completed before retry: `{debug_summary['completed_before_retry']}`",
        f"- Failed before retry: `{debug_summary['failed_before_retry']}`",
        f"- Failed run: `{failed_name or 'unknown'}`",
        f"- Failure type: `{failure_type}`",
        f"- Appears transient: `{str(appears_transient).lower()}`",
        "",
        "## Failed Configuration",
        "",
    ]
    if failed_config:
        for key in ["topology", "attack", "defense", "seed"]:
            md_lines.append(f"- {key}: `{failed_config.get(key)}`")
    else:
        md_lines.append("- Failed configuration could not be identified from available high-level artifacts.")
    md_lines.extend(
        [
            "",
            "## Privacy Boundary",
            "",
            "Raw traces, raw provider outputs, prompts, policy JSONL, event JSONL, and individual metrics are not written by this script.",
            "",
        ]
    )

    write_json(output_dir / "failed_run_diagnosis.json", diagnosis)
    write_json(output_dir / "debug_summary.json", debug_summary)
    (output_dir / "debug_summary.md").write_text(redact_text("\n".join(md_lines)), encoding="utf-8")

    if args.strict and not failed_config:
        raise SystemExit("failed run could not be identified")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Diagnose a MiniMax coverage timeout from high-level artifacts.")
    parser.add_argument("--coverage-artifact-dir", default="artifacts/minimax_p1_coverage_3seed")
    parser.add_argument("--remote-runs-root")
    parser.add_argument("--matrix-config", default="configs/experiment/mas_p1_minimax_coverage_3seed.yaml")
    parser.add_argument("--output-dir", default="artifacts/minimax_p1_coverage_3seed_debug")
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    raise SystemExit(diagnose(parse_args()))
