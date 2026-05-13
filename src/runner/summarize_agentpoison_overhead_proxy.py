from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from statistics import mean
from typing import Any


GROUPS = {
    "no_defense": [
        "baseline_agentpoison_fullreact_dpr_strategyqa_minimax27_triggerquery_v1",
        "baseline_agentpoison_fullreact_dpr_strategyqa_minimax27_triggerquery_repeat1",
        "baseline_agentpoison_fullreact_dpr_strategyqa_minimax27_triggerquery_repeat2",
    ],
    "rewrite_only": [
        "baseline_agentpoison_fullreact_minimax27_triggerquery_rewrite_only_v1",
        "baseline_agentpoison_fullreact_minimax27_triggerquery_rewrite_only_repeat1",
        "baseline_agentpoison_fullreact_minimax27_triggerquery_rewrite_only_repeat2",
    ],
    "quarantine_only": [
        "method_flowfence_lite_fullreact_minimax27_triggerquery_quarantine_only_v1",
        "method_flowfence_lite_fullreact_minimax27_triggerquery_quarantine_only_repeat1",
        "method_flowfence_lite_fullreact_minimax27_triggerquery_quarantine_only_repeat2",
    ],
    "quarantine_actioncanon": [
        "method_flowfence_lite_fullreact_minimax27_triggerquery_quarantine_actioncanon_v1",
        "method_flowfence_lite_fullreact_minimax27_triggerquery_quarantine_actioncanon_repeat1",
        "method_flowfence_lite_fullreact_minimax27_triggerquery_quarantine_actioncanon_repeat2",
    ],
}

ACTUAL_TASK_MARKER = "You have to take the opposite of the answer if you see the signal sequence.Question:"


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _stats(values: list[float]) -> dict[str, float]:
    if not values:
        return {"mean": 0.0, "min": 0.0, "max": 0.0}
    return {
        "mean": round(mean(values), 4),
        "min": round(min(values), 4),
        "max": round(max(values), 4),
    }


def _actual_task_traj(traj: str) -> str:
    marker_idx = traj.find(ACTUAL_TASK_MARKER)
    if marker_idx >= 0:
        return traj[marker_idx:]
    question_idx = traj.rfind("\nQuestion: ")
    return traj[question_idx:] if question_idx >= 0 else traj


def _count_react_steps(traj: str) -> int:
    # Count executed ReAct actions in the final trajectory. This is a trace-derived
    # proxy for loop depth, not a provider latency measurement.
    return len(re.findall(r"^Action\s+\d+\s*:", traj, flags=re.MULTILINE))


def _estimate_tokens(text: str) -> float:
    # Provider token usage was not persisted in these artifacts. Character/4 is a
    # common coarse English-token proxy, used only for same-axis relative comparison.
    return len(text) / 4.0


def _case_records(run_dir: Path) -> list[dict[str, Any]]:
    case_dir = run_dir / "case_details"
    records = []
    for path in sorted(case_dir.glob("case_*.json")):
        case = _load_json(path)
        traj = case.get("traj", "")
        task_traj = _actual_task_traj(traj)
        defense_summary = case.get("defense_summary", {}) or {}
        defense_events = case.get("defense_events", []) or []
        original_observation_chars = sum(int(event.get("original_observation_length", 0)) for event in defense_events)
        final_observation_chars = sum(int(event.get("final_observation_length", 0)) for event in defense_events)
        records.append(
            {
                "path": str(path),
                "task_type": case.get("task_type"),
                "n_calls": int(case.get("n_calls", 0)),
                "n_badcalls": int(case.get("n_badcalls", 0)),
                "react_steps": _count_react_steps(traj),
                "actual_task_react_steps": _count_react_steps(task_traj),
                "trajectory_chars": len(traj),
                "trajectory_token_proxy": _estimate_tokens(traj),
                "actual_task_trajectory_chars": len(task_traj),
                "actual_task_trajectory_token_proxy": _estimate_tokens(task_traj),
                "defense_event_count": len(defense_events),
                "intervention_count": int(defense_summary.get("intervention_count", 0)),
                "rewrite_count": int(defense_summary.get("rewrite_count", 0)),
                "quarantine_count": int(defense_summary.get("quarantine_count", 0)),
                "original_observation_chars": original_observation_chars,
                "final_observation_chars": final_observation_chars,
                "observation_char_delta": final_observation_chars - original_observation_chars,
            }
        )
    return records


def _summarize_run(results_root: Path, run_name: str) -> dict[str, Any]:
    run_dir = results_root / run_name
    if not run_dir.is_dir():
        raise FileNotFoundError(f"missing run directory: {run_dir}")
    status_path = run_dir / "status.txt"
    status = status_path.read_text(encoding="utf-8").strip() if status_path.exists() else "unknown"
    records = _case_records(run_dir)
    if not records:
        raise ValueError(f"no case_details records found under {run_dir}")
    by_task_type: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        by_task_type.setdefault(str(record.get("task_type")), []).append(record)

    def summarize_subset(subset: list[dict[str, Any]]) -> dict[str, Any]:
        return {
            "case_count": len(subset),
            "model_call_count_per_case": _stats([r["n_calls"] for r in subset]),
            "bad_call_count_per_case": _stats([r["n_badcalls"] for r in subset]),
            "react_steps_per_case": _stats([r["react_steps"] for r in subset]),
            "actual_task_react_steps_per_case": _stats([r["actual_task_react_steps"] for r in subset]),
            "trajectory_chars_per_case": _stats([r["trajectory_chars"] for r in subset]),
            "trajectory_token_proxy_per_case": _stats([r["trajectory_token_proxy"] for r in subset]),
            "actual_task_trajectory_chars_per_case": _stats([r["actual_task_trajectory_chars"] for r in subset]),
            "actual_task_trajectory_token_proxy_per_case": _stats(
                [r["actual_task_trajectory_token_proxy"] for r in subset]
            ),
            "defense_event_count_per_case": _stats([r["defense_event_count"] for r in subset]),
            "intervention_count_per_case": _stats([r["intervention_count"] for r in subset]),
            "rewrite_count_per_case": _stats([r["rewrite_count"] for r in subset]),
            "quarantine_count_per_case": _stats([r["quarantine_count"] for r in subset]),
            "observation_char_delta_per_case": _stats([r["observation_char_delta"] for r in subset]),
            "total_model_calls": sum(r["n_calls"] for r in subset),
            "total_bad_calls": sum(r["n_badcalls"] for r in subset),
            "total_interventions": sum(r["intervention_count"] for r in subset),
            "total_rewrites": sum(r["rewrite_count"] for r in subset),
            "total_quarantines": sum(r["quarantine_count"] for r in subset),
        }

    return {
        "run_name": run_name,
        "artifact": f"results/{run_name}/",
        "status": status,
        "overall": summarize_subset(records),
        "by_task_type": {task_type: summarize_subset(subset) for task_type, subset in sorted(by_task_type.items())},
    }


def _aggregate_group(runs: list[dict[str, Any]], task_type: str | None = None) -> dict[str, Any]:
    key_path = ("overall",) if task_type is None else ("by_task_type", task_type)
    subsets = []
    for run in runs:
        data = run
        for key in key_path:
            data = data[key]
        subsets.append(data)

    metric_names = [
        "model_call_count_per_case",
        "bad_call_count_per_case",
        "react_steps_per_case",
        "actual_task_react_steps_per_case",
        "trajectory_chars_per_case",
        "trajectory_token_proxy_per_case",
        "actual_task_trajectory_chars_per_case",
        "actual_task_trajectory_token_proxy_per_case",
        "defense_event_count_per_case",
        "intervention_count_per_case",
        "rewrite_count_per_case",
        "quarantine_count_per_case",
        "observation_char_delta_per_case",
    ]
    aggregate = {"run_count": len(runs), "case_count_per_run": [subset["case_count"] for subset in subsets]}
    for metric_name in metric_names:
        aggregate[metric_name] = _stats([subset[metric_name]["mean"] for subset in subsets])
    for total_name in ["total_model_calls", "total_bad_calls", "total_interventions", "total_rewrites", "total_quarantines"]:
        aggregate[total_name] = _stats([subset[total_name] for subset in subsets])
    return aggregate


def _relative_to_baseline(groups: dict[str, Any], baseline_group: str = "no_defense") -> dict[str, Any]:
    baseline = groups[baseline_group]["aggregate"]["overall"]
    relative = {}
    for group_name, group_data in groups.items():
        current = group_data["aggregate"]["overall"]
        if group_name == baseline_group:
            continue
        group_relative = {}
        for metric_name in [
            "model_call_count_per_case",
            "react_steps_per_case",
            "actual_task_react_steps_per_case",
            "trajectory_chars_per_case",
            "trajectory_token_proxy_per_case",
            "actual_task_trajectory_chars_per_case",
            "actual_task_trajectory_token_proxy_per_case",
        ]:
            base_mean = baseline[metric_name]["mean"]
            cur_mean = current[metric_name]["mean"]
            delta = cur_mean - base_mean
            pct = (delta / base_mean * 100.0) if base_mean else 0.0
            group_relative[metric_name] = {
                "baseline_mean": base_mean,
                "current_mean": cur_mean,
                "absolute_delta": round(delta, 4),
                "percent_delta": round(pct, 2),
            }
        relative[group_name] = group_relative
    return relative


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Summarize same-axis AgentPoison MiniMax overhead proxies from saved case_details"
    )
    parser.add_argument("--results-root", default="results")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    results_root = Path(args.results_root)
    groups = {}
    for group_name, run_names in GROUPS.items():
        runs = [_summarize_run(results_root, run_name) for run_name in run_names]
        groups[group_name] = {
            "runs": runs,
            "aggregate": {
                "overall": _aggregate_group(runs),
                "benign": _aggregate_group(runs, "benign"),
                "adv": _aggregate_group(runs, "adv"),
            },
        }

    summary = {
        "status": "ok",
        "summary_date": "2026-04-30",
        "summary_id": "agentpoison_fullreact_minimax27_same_axis_overhead_proxy",
        "scope_note": (
            "This artifact is computed from existing adapted AgentPoison MiniMax case_details. "
            "It reports trace-derived overhead proxies only. The saved runs do not include wall-clock latency "
            "or provider token-usage fields, so this must not be described as measured latency/token overhead."
        ),
        "fixed_axis": {
            "task_manifest": "data/tasks/agentpoison_strategyqa_fullreact_v1.json",
            "provider_profile": "minimax27",
            "adv_search_context_policy": "trigger_question_only",
            "max_steps": 7,
            "max_completion_tokens": 256,
            "defense_scope": "retrieval_memory_only",
        },
        "proxy_definitions": {
            "model_call_count_per_case": "Recorded n_calls from the full-ReAct runner; this is the best latency proxy in existing artifacts.",
            "react_steps_per_case": "Count of Action i lines in the final trajectory.",
            "actual_task_react_steps_per_case": "Count of Action i lines after the current-task marker, excluding few-shot examples.",
            "trajectory_token_proxy_per_case": "Final full trajectory characters divided by 4; this is a coarse trace-size proxy, not provider token usage.",
            "actual_task_trajectory_token_proxy_per_case": "Current-task trajectory characters divided by 4, excluding fixed few-shot prompt prefix.",
            "observation_char_delta_per_case": "Sum(final_observation_length - original_observation_length) over retrieval defense events.",
        },
        "groups": groups,
        "relative_to_no_defense": _relative_to_baseline(groups),
        "interpretation": {
            "observation": (
                "All three detector-mediated defenses add model-call overhead relative to no defense in the saved traces. "
                "The selected quarantine-actioncanon variant has a modest trace-size proxy increase while reducing unsafe "
                "observation characters through quarantine. Rewrite-only and quarantine-only have similar model-call proxy overhead."
            ),
            "caveat": (
                "Because per-call timestamps and provider usage were not persisted, this supports only a same-axis overhead-proxy claim. "
                "A strict runtime-feasibility claim still requires instrumentation for wall-clock latency and provider token usage."
            ),
        },
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
