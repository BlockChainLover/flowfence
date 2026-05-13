from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean
from typing import Any


GROUPS = {
    "no_defense": [
        "baseline_agentpoison_fullreact_dpr_strategyqa_minimax27_triggerquery_heldout_instruction_v2",
        "baseline_agentpoison_fullreact_dpr_strategyqa_minimax27_triggerquery_heldout_instruction_repeat1",
        "baseline_agentpoison_fullreact_dpr_strategyqa_minimax27_triggerquery_heldout_instruction_repeat2",
    ],
    "static_keyword_filter_nonoracle": [
        "baseline_agentpoison_fullreact_minimax27_triggerquery_heldout_instruction_static_keyword_filter_v2",
        "baseline_agentpoison_fullreact_minimax27_triggerquery_heldout_instruction_static_keyword_filter_repeat1",
        "baseline_agentpoison_fullreact_minimax27_triggerquery_heldout_instruction_static_keyword_filter_repeat2",
    ],
    "flowfence_lite_quarantine_actioncanon": [
        "method_flowfence_lite_fullreact_minimax27_triggerquery_heldout_instruction_quarantine_actioncanon_v2",
        "method_flowfence_lite_fullreact_minimax27_triggerquery_heldout_instruction_quarantine_actioncanon_repeat1",
        "method_flowfence_lite_fullreact_minimax27_triggerquery_heldout_instruction_quarantine_actioncanon_repeat2",
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
    metrics = _load_json(results_root / run_name / "metrics.json")
    future = metrics["future_defense_metrics"]
    diagnostics = metrics.get("defense_diagnostics", {})
    return {
        "artifact": f"results/{run_name}/",
        "clean_utility_rate": future["clean_utility_rate"],
        "attacked_utility_rate": future["attacked_utility_rate"],
        "attack_manifestation_rate": future["attack_manifestation_rate"],
        "exposed_poisoned_retrieval_case_rate": future["exposed_poisoned_retrieval_case_rate"],
        "raw_poisoned_retrieval_case_rate": future["raw_poisoned_retrieval_case_rate"],
        "defense_intervention_event_rate": diagnostics.get("defense_intervention_event_rate", 0.0),
        "benign_false_block_proxy_rate": diagnostics.get("benign_false_block_proxy_rate", 0.0),
        "adv_intervention_case_rate": diagnostics.get("adv_intervention_case_rate", 0.0),
        "intervention_count": diagnostics.get("intervention_count", 0),
        "rewrite_count": diagnostics.get("rewrite_count", 0),
        "quarantine_count": diagnostics.get("quarantine_count", 0),
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
        "intervention_count",
        "rewrite_count",
        "quarantine_count",
    ]
    return {name: _stats([float(run[name]) for run in runs]) for name in metric_names}


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize held-out AgentPoison instruction comparator")
    parser.add_argument("--results-root", default="results")
    parser.add_argument(
        "--output",
        default="results/baseline_agentpoison_fullreact_minimax27_heldout_instruction_matrix_summary.json",
    )
    args = parser.parse_args()

    results_root = Path(args.results_root)
    groups = {}
    for group, run_names in GROUPS.items():
        runs = [_run_metrics(results_root, run_name) for run_name in run_names]
        groups[group] = {"runs": runs, "aggregate": _aggregate(runs)}

    summary = {
        "status": "ok",
        "summary_date": "2026-05-06",
        "provider_profile": "minimax27",
        "matrix_id": "agentpoison_fullreact_minimax27_triggerquery_heldout_instruction_matrix_v1",
        "scope_note": (
            "This matrix keeps the adapted full-ReAct AgentPoison MiniMax setup but changes the poisoned guidance "
            "to a paraphrased held-out instruction. The static keyword filter is intentionally non-oracle: it does "
            "not match the trigger sequence and only blocks old-axis attack phrases. This is not full official "
            "AgentPoison reproduction."
        ),
        "comparison_question": (
            "Does FlowFence-Lite retain containment on a held-out poisoned-instruction paraphrase where a simple "
            "old-axis keyword filter is expected to be brittle?"
        ),
        "fixed_settings": {
            "task_manifest": "data/tasks/agentpoison_strategyqa_fullreact_v1.json",
            "provider_profile": "minimax27",
            "adv_search_context_policy": "trigger_question_only",
            "max_steps": 7,
            "max_completion_tokens": 256,
            "heldout_configs": [
                "configs/experiment/agentpoison_fullreact_minimax27_triggerquery_heldout_instruction.yaml",
                "configs/experiment/agentpoison_fullreact_static_keyword_filter_minimax27_triggerquery_heldout_instruction.yaml",
                "configs/experiment/agentpoison_fullreact_flowfence_lite_minimax27_triggerquery_heldout_instruction_quarantine_actioncanon.yaml",
            ],
        },
        "groups": groups,
        "interpretation": {
            "observation": (
                "This artifact reports a 3-run held-out-instruction stress test. No-defense should have non-zero "
                "raw poisoned retrieval and attack manifestation for the stress test to be non-vacuous."
            ),
            "caveat": "This summary aggregates the configured repeat artifacts when all listed runs are present.",
        },
    }
    output_path = Path(args.output)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
