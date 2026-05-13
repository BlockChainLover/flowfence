from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean
from typing import Any


DEFAULT_GROUPS = {
    "no_defense": ["overhead_agentpoison_fullreact_minimax27_triggerquery_nodefense_v1"],
    "quarantine_actioncanon": ["overhead_agentpoison_fullreact_minimax27_triggerquery_quarantine_actioncanon_v1"],
}


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _stats(values: list[float]) -> dict[str, float | None]:
    if not values:
        return {"mean": None, "min": None, "max": None}
    return {
        "mean": round(mean(values), 6),
        "min": round(min(values), 6),
        "max": round(max(values), 6),
    }


def _case_records(run_dir: Path) -> list[dict[str, Any]]:
    records = []
    for path in sorted((run_dir / "case_details").glob("case_*.json")):
        case = _load_json(path)
        overhead = case.get("overhead_measurement", {}) or {}
        if not overhead:
            raise ValueError(f"missing overhead_measurement in {path}")
        provider_usage_available = bool(overhead.get("provider_usage_available"))
        records.append(
            {
                "path": str(path),
                "task_type": case.get("task_type"),
                "wall_time_seconds": float(overhead.get("wall_time_seconds", 0.0)),
                "llm_call_wall_time_seconds": float(overhead.get("llm_call_wall_time_seconds", 0.0)),
                "llm_provider_request_seconds": float(overhead.get("llm_provider_request_seconds", 0.0)),
                "defense_wall_time_seconds": float(overhead.get("defense_wall_time_seconds", 0.0)),
                "llm_call_count": int(overhead.get("llm_call_count", 0)),
                "defense_inspection_count": int(overhead.get("defense_inspection_count", 0)),
                "provider_usage_available": provider_usage_available,
                "prompt_tokens": overhead.get("prompt_tokens"),
                "completion_tokens": overhead.get("completion_tokens"),
                "total_tokens": overhead.get("total_tokens"),
                "prompt_token_proxy": float(overhead.get("prompt_token_proxy", 0.0)),
                "completion_token_proxy": float(overhead.get("completion_token_proxy", 0.0)),
                "total_token_proxy": float(overhead.get("total_token_proxy", 0.0)),
            }
        )
    if not records:
        raise ValueError(f"no measured case records found under {run_dir}")
    return records


def _summarize_subset(records: list[dict[str, Any]]) -> dict[str, Any]:
    total_tokens = [float(r["total_tokens"]) for r in records if r["total_tokens"] is not None]
    return {
        "case_count": len(records),
        "provider_usage_case_count": sum(1 for r in records if r["provider_usage_available"]),
        "wall_time_seconds_per_case": _stats([r["wall_time_seconds"] for r in records]),
        "llm_call_wall_time_seconds_per_case": _stats([r["llm_call_wall_time_seconds"] for r in records]),
        "llm_provider_request_seconds_per_case": _stats([r["llm_provider_request_seconds"] for r in records]),
        "defense_wall_time_seconds_per_case": _stats([r["defense_wall_time_seconds"] for r in records]),
        "llm_call_count_per_case": _stats([r["llm_call_count"] for r in records]),
        "defense_inspection_count_per_case": _stats([r["defense_inspection_count"] for r in records]),
        "provider_total_tokens_per_case": _stats(total_tokens),
        "total_token_proxy_per_case": _stats([r["total_token_proxy"] for r in records]),
        "total_wall_time_seconds": round(sum(r["wall_time_seconds"] for r in records), 6),
        "total_llm_call_wall_time_seconds": round(sum(r["llm_call_wall_time_seconds"] for r in records), 6),
        "total_defense_wall_time_seconds": round(sum(r["defense_wall_time_seconds"] for r in records), 6),
        "total_llm_calls": sum(r["llm_call_count"] for r in records),
        "total_defense_inspections": sum(r["defense_inspection_count"] for r in records),
    }


def _summarize_run(results_root: Path, run_name: str) -> dict[str, Any]:
    run_dir = results_root / run_name
    status = (run_dir / "status.txt").read_text(encoding="utf-8").strip()
    records = _case_records(run_dir)
    by_task_type: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        by_task_type.setdefault(str(record["task_type"]), []).append(record)
    return {
        "run_name": run_name,
        "artifact": f"results/{run_name}/",
        "status": status,
        "overall": _summarize_subset(records),
        "by_task_type": {task: _summarize_subset(rows) for task, rows in sorted(by_task_type.items())},
    }


def _aggregate_runs(runs: list[dict[str, Any]], task_type: str | None = None) -> dict[str, Any]:
    subsets = []
    for run in runs:
        subsets.append(run["overall"] if task_type is None else run["by_task_type"][task_type])
    metric_names = [
        "wall_time_seconds_per_case",
        "llm_call_wall_time_seconds_per_case",
        "llm_provider_request_seconds_per_case",
        "defense_wall_time_seconds_per_case",
        "llm_call_count_per_case",
        "defense_inspection_count_per_case",
        "provider_total_tokens_per_case",
        "total_token_proxy_per_case",
    ]
    aggregate: dict[str, Any] = {
        "run_count": len(runs),
        "case_count_per_run": [subset["case_count"] for subset in subsets],
        "provider_usage_case_count_per_run": [subset["provider_usage_case_count"] for subset in subsets],
    }
    for metric_name in metric_names:
        aggregate[metric_name] = _stats(
            [
                subset[metric_name]["mean"]
                for subset in subsets
                if subset[metric_name]["mean"] is not None
            ]
        )
    for total_name in [
        "total_wall_time_seconds",
        "total_llm_call_wall_time_seconds",
        "total_defense_wall_time_seconds",
        "total_llm_calls",
        "total_defense_inspections",
    ]:
        aggregate[total_name] = _stats([subset[total_name] for subset in subsets])
    return aggregate


def _relative_to_baseline(groups: dict[str, Any], baseline_group: str = "no_defense") -> dict[str, Any]:
    baseline = groups[baseline_group]["aggregate"]["overall"]
    relative = {}
    for group_name, group_data in groups.items():
        if group_name == baseline_group:
            continue
        current = group_data["aggregate"]["overall"]
        group_relative = {}
        for metric_name in [
            "wall_time_seconds_per_case",
            "llm_call_wall_time_seconds_per_case",
            "llm_provider_request_seconds_per_case",
            "defense_wall_time_seconds_per_case",
            "llm_call_count_per_case",
            "provider_total_tokens_per_case",
            "total_token_proxy_per_case",
        ]:
            base_mean = baseline[metric_name]["mean"]
            cur_mean = current[metric_name]["mean"]
            if base_mean is None or cur_mean is None:
                group_relative[metric_name] = {
                    "baseline_mean": base_mean,
                    "current_mean": cur_mean,
                    "absolute_delta": None,
                    "percent_delta": None,
                }
                continue
            delta = cur_mean - base_mean
            pct = (delta / base_mean * 100.0) if base_mean else 0.0
            group_relative[metric_name] = {
                "baseline_mean": base_mean,
                "current_mean": cur_mean,
                "absolute_delta": round(delta, 6),
                "percent_delta": round(pct, 2),
            }
        relative[group_name] = group_relative
    return relative


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize measured overhead from instrumented AgentPoison full-ReAct runs")
    parser.add_argument("--results-root", default="results")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    results_root = Path(args.results_root)
    groups = {}
    for group_name, run_names in DEFAULT_GROUPS.items():
        runs = [_summarize_run(results_root, run_name) for run_name in run_names]
        groups[group_name] = {
            "runs": runs,
            "aggregate": {
                "overall": _aggregate_runs(runs),
                "benign": _aggregate_runs(runs, "benign"),
                "adv": _aggregate_runs(runs, "adv"),
            },
        }

    summary = {
        "status": "ok",
        "summary_date": "2026-05-06",
        "summary_id": "agentpoison_fullreact_minimax27_same_axis_measured_overhead",
        "scope_note": (
            "This artifact summarizes instrumented wall-clock overhead on a fixed 10-question same-axis slice. "
            "It is a runtime-feasibility slice, not a replacement for the 25-case efficacy matrix."
        ),
        "fixed_axis": {
            "task_manifest": "data/tasks/agentpoison_strategyqa_fullreact_overhead_v1.json",
            "provider_profile": "minimax27",
            "adv_search_context_policy": "trigger_question_only",
            "max_steps": 7,
            "max_completion_tokens": 256,
            "defense_scope": "retrieval_memory_only",
        },
        "metric_notes": {
            "wall_time_seconds_per_case": "End-to-end case wall time measured inside the runner.",
            "llm_call_wall_time_seconds_per_case": "Sum of instrumented LLM call wall times, including retry sleeps if any.",
            "llm_provider_request_seconds_per_case": "Sum of direct provider request durations, excluding retry sleep.",
            "defense_wall_time_seconds_per_case": "Time spent inside FlowFence-Lite retrieval-event inspection.",
            "provider_total_tokens_per_case": "Provider-reported usage when available; null if the provider does not return usage.",
            "total_token_proxy_per_case": "Fallback prompt/completion character count divided by 4.",
        },
        "groups": groups,
        "relative_to_no_defense": _relative_to_baseline(groups),
    }
    output_path = Path(args.output)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
