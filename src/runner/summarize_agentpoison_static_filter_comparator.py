from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean
from typing import Any


RUNS = {
    "static_keyword_filter": [
        "baseline_agentpoison_fullreact_minimax27_triggerquery_static_keyword_filter_v1",
        "baseline_agentpoison_fullreact_minimax27_triggerquery_static_keyword_filter_repeat1",
        "baseline_agentpoison_fullreact_minimax27_triggerquery_static_keyword_filter_repeat2",
    ],
}


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


def _run_metrics(results_root: Path, run_name: str) -> dict[str, Any]:
    run_dir = results_root / run_name
    metrics = _load_json(run_dir / "metrics.json")
    future = metrics["future_defense_metrics"]
    diagnostics = metrics["defense_diagnostics"]
    return {
        "artifact": f"results/{run_name}/",
        "clean_utility_rate": future["clean_utility_rate"],
        "attacked_utility_rate": future["attacked_utility_rate"],
        "attack_manifestation_rate": future["attack_manifestation_rate"],
        "exposed_poisoned_retrieval_case_rate": future["exposed_poisoned_retrieval_case_rate"],
        "raw_poisoned_retrieval_case_rate": future["raw_poisoned_retrieval_case_rate"],
        "defense_intervention_event_rate": diagnostics["defense_intervention_event_rate"],
        "benign_false_block_proxy_rate": diagnostics["benign_false_block_proxy_rate"],
        "adv_intervention_case_rate": diagnostics["adv_intervention_case_rate"],
        "intervention_count": diagnostics["intervention_count"],
        "rewrite_count": diagnostics["rewrite_count"],
        "quarantine_count": diagnostics["quarantine_count"],
    }


def _aggregate(runs: list[dict[str, Any]]) -> dict[str, Any]:
    metric_names = [
        "clean_utility_rate",
        "attacked_utility_rate",
        "attack_manifestation_rate",
        "exposed_poisoned_retrieval_case_rate",
        "raw_poisoned_retrieval_case_rate",
        "defense_intervention_event_rate",
        "benign_false_block_proxy_rate",
        "adv_intervention_case_rate",
    ]
    aggregate = {name: _stats([run[name] for run in runs]) for name in metric_names}
    aggregate["intervention_count"] = _stats([run["intervention_count"] for run in runs])
    aggregate["rewrite_count"] = _stats([run["rewrite_count"] for run in runs])
    aggregate["quarantine_count"] = _stats([run["quarantine_count"] for run in runs])
    return aggregate


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize static keyword filter comparator runs")
    parser.add_argument("--results-root", default="results")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    results_root = Path(args.results_root)
    groups = {}
    for group, run_names in RUNS.items():
        runs = [_run_metrics(results_root, run_name) for run_name in run_names]
        groups[group] = {
            "runs": runs,
            "aggregate": _aggregate(runs),
        }

    summary = {
        "status": "ok",
        "summary_date": "2026-05-06",
        "provider_profile": "minimax27",
        "matrix_id": "agentpoison_fullreact_minimax27_triggerquery_static_keyword_filter_independent_weak_comparator",
        "scope_note": (
            "This is an independent weak-defense comparator on the adapted full-ReAct AgentPoison MiniMax setup. "
            "It uses static keyword/blocklist filtering rather than the FlowFence-Lite risk score, lease signal, "
            "safe-view rewrite, or quarantine policy. It must not be described as full official AgentPoison reproduction."
        ),
        "comparison_question": (
            "Does a static keyword filter baseline contain exposed poisoned retrieval on the fixed adapted "
            "AgentPoison MiniMax axis, and what utility/intervention cost does it show?"
        ),
        "fixed_settings": {
            "task_manifest": "data/tasks/agentpoison_strategyqa_fullreact_v1.json",
            "static_filter_config": "configs/experiment/agentpoison_fullreact_static_keyword_filter_minimax27_triggerquery.yaml",
            "provider_profile": "minimax27",
            "adv_search_context_policy": "trigger_question_only",
            "max_steps": 7,
            "max_completion_tokens": 256,
            "defense_scope": "retrieval_memory_only",
            "canonical_action_writeback": True,
        },
        "groups": groups,
        "interpretation": {
            "observation": (
                "The static keyword filter is an independent weak baseline because it does not use the FlowFence-Lite "
                "risk score or lease semantics. It should be compared against no-defense, rewrite-only, and "
                "quarantine-actioncanon using the same fixed axis."
            ),
            "caveat": "This summary contains only the completed static-filter runs listed in this artifact.",
        },
    }
    output_path = Path(args.output)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
