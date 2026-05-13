from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from statistics import mean
from typing import Any


FAMILIES = [
    "direct_instruction",
    "policy_style",
    "factual_note",
    "system_imitation",
    "tool_suggestion",
    "indirect_preference",
]
CONDITIONS = ["no_defense", "static_keyword_filter", "flowfence_lite"]
PRESSURE_KNN = [1, 3, 5]
REPEATS = ["v1", "repeat1", "repeat2"]


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _stats(values: list[float]) -> dict[str, float | None]:
    if not values:
        return {"mean": None, "min": None, "max": None}
    return {"mean": round(mean(values), 4), "min": round(min(values), 4), "max": round(max(values), 4)}


def _run_names(prefix: str) -> list[str]:
    return [f"{prefix}_{repeat}" for repeat in REPEATS]


def _metric_row(results_root: Path, run_name: str) -> dict[str, Any]:
    run_dir = results_root / run_name
    metrics = _load_json(run_dir / "metrics.json")
    future = metrics["future_defense_metrics"]
    diagnostics = metrics.get("defense_diagnostics", {})
    overhead = _summarize_overhead(run_dir)
    false_positive = _summarize_false_positive(run_dir)
    return {
        "run_name": run_name,
        "artifact": f"results/{run_name}/",
        "status": metrics.get("status"),
        "clean_utility_rate": future.get("clean_utility_rate"),
        "attacked_utility_rate": future.get("attacked_utility_rate"),
        "attack_manifestation_rate": future.get("attack_manifestation_rate"),
        "raw_poisoned_retrieval_case_rate": future.get("raw_poisoned_retrieval_case_rate"),
        "exposed_poisoned_retrieval_case_rate": future.get("exposed_poisoned_retrieval_case_rate"),
        "defense_intervention_event_rate": diagnostics.get("defense_intervention_event_rate", 0.0),
        "benign_false_block_proxy_rate": diagnostics.get("benign_false_block_proxy_rate", 0.0),
        "adv_intervention_case_rate": diagnostics.get("adv_intervention_case_rate", 0.0),
        "intervention_count": diagnostics.get("intervention_count", 0),
        "rewrite_count": diagnostics.get("rewrite_count", 0),
        "quarantine_count": diagnostics.get("quarantine_count", 0),
        **overhead,
        **false_positive,
    }


def _summarize_overhead(run_dir: Path) -> dict[str, Any]:
    case_paths = sorted((run_dir / "case_details").glob("case_*.json"))
    if not case_paths:
        return {
            "avg_llm_calls": None,
            "avg_wall_time_seconds": None,
            "avg_total_tokens": None,
            "avg_total_token_proxy": None,
        }
    calls = []
    wall = []
    tokens = []
    token_proxy = []
    for path in case_paths:
        case = _load_json(path)
        overhead = case.get("overhead_measurement", {}) or {}
        calls.append(float(overhead.get("llm_call_count", 0)))
        wall.append(float(overhead.get("wall_time_seconds", 0.0)))
        if overhead.get("total_tokens") is not None:
            tokens.append(float(overhead["total_tokens"]))
        token_proxy.append(float(overhead.get("total_token_proxy", 0.0)))
    return {
        "avg_llm_calls": round(mean(calls), 4) if calls else None,
        "avg_wall_time_seconds": round(mean(wall), 4) if wall else None,
        "avg_total_tokens": round(mean(tokens), 4) if tokens else None,
        "avg_total_token_proxy": round(mean(token_proxy), 4) if token_proxy else None,
    }


def _summarize_false_positive(run_dir: Path) -> dict[str, Any]:
    case_paths = sorted((run_dir / "case_details").glob("case_*.json"))
    benign_retrieved_cases = 0
    benign_quarantined_cases = 0
    false_positive_cases = []
    for path in case_paths:
        case = _load_json(path)
        retrieved = int(case.get("benign_instruction_retrieval_success", 0)) > 0
        if not retrieved:
            continue
        benign_retrieved_cases += 1
        quarantined = any(event.get("decision") == "quarantine" for event in case.get("defense_events", []))
        if quarantined:
            benign_quarantined_cases += 1
            false_positive_cases.append(path.name)
    return {
        "benign_instruction_retrieved_cases": benign_retrieved_cases,
        "benign_instruction_quarantined_cases": benign_quarantined_cases,
        "false_quarantine_rate_on_benign_instruction": (
            round(benign_quarantined_cases / benign_retrieved_cases, 4) if benign_retrieved_cases else None
        ),
        "false_positive_case_examples": ";".join(false_positive_cases[:5]),
    }


def _aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    metric_names = [
        "clean_utility_rate",
        "attacked_utility_rate",
        "attack_manifestation_rate",
        "raw_poisoned_retrieval_case_rate",
        "exposed_poisoned_retrieval_case_rate",
        "defense_intervention_event_rate",
        "benign_false_block_proxy_rate",
        "adv_intervention_case_rate",
        "avg_llm_calls",
        "avg_wall_time_seconds",
        "avg_total_tokens",
        "avg_total_token_proxy",
        "false_quarantine_rate_on_benign_instruction",
    ]
    aggregate = {}
    for metric in metric_names:
        values = [float(row[metric]) for row in rows if row.get(metric) is not None]
        aggregate[metric] = _stats(values)
    for count_name in [
        "intervention_count",
        "rewrite_count",
        "quarantine_count",
        "benign_instruction_retrieved_cases",
        "benign_instruction_quarantined_cases",
    ]:
        aggregate[count_name] = _stats([float(row[count_name]) for row in rows if row.get(count_name) is not None])
    return aggregate


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _build_matrix(results_root: Path, prefixes: dict[str, list[str]]) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    groups = {}
    run_rows = []
    aggregate_rows = []
    for group_name, run_names in prefixes.items():
        rows = [_metric_row(results_root, run_name) for run_name in run_names]
        aggregate = _aggregate(rows)
        groups[group_name] = {"runs": rows, "aggregate": aggregate}
        run_rows.extend({"group": group_name, **row} for row in rows)
        flat = {"group": group_name}
        for metric, stats in aggregate.items():
            if isinstance(stats, dict):
                flat[f"{metric}_mean"] = stats.get("mean")
                flat[f"{metric}_min"] = stats.get("min")
                flat[f"{metric}_max"] = stats.get("max")
        aggregate_rows.append(flat)
    return groups, run_rows, aggregate_rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize ICDE supplemental AgentPoison MiniMax experiments")
    parser.add_argument("--results-root", default="results")
    parser.add_argument("--out-dir", default="artifacts/icde2027_supplemental/results")
    args = parser.parse_args()

    results_root = Path(args.results_root)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    paraphrase_prefixes = {}
    for family in FAMILIES:
        for condition in CONDITIONS:
            group = f"{family}/{condition}"
            paraphrase_prefixes[group] = _run_names(f"icde_paraphrase_{family}_{condition}")
    paraphrase_groups, paraphrase_runs, paraphrase_aggregates = _build_matrix(results_root, paraphrase_prefixes)

    pressure_prefixes = {}
    for knn in PRESSURE_KNN:
        for condition in CONDITIONS:
            group = f"knn{knn}/{condition}"
            pressure_prefixes[group] = _run_names(f"icde_pressure_knn{knn}_{condition}")
    pressure_groups, pressure_runs, pressure_aggregates = _build_matrix(results_root, pressure_prefixes)

    false_positive_prefixes = {
        condition: _run_names(f"icde_false_positive_benign_instruction_{condition}")
        for condition in ["no_defense", "flowfence_lite"]
    }
    false_positive_groups, false_positive_runs, false_positive_aggregates = _build_matrix(
        results_root, false_positive_prefixes
    )

    summary = {
        "status": "ok",
        "summary_date": "2026-05-07",
        "provider_profile": "minimax27",
        "scope_note": (
            "Supplemental ICDE strengthening experiments on the same adapted AgentPoison StrategyQA full-ReAct "
            "MiniMax axis. These artifacts are not full official AgentPoison reproduction and do not claim "
            "universal detection."
        ),
        "paraphrase_family": paraphrase_groups,
        "pressure_topk_candidate_pool": pressure_groups,
        "false_positive_clean_memory": false_positive_groups,
    }
    (out_dir / "icde_supplemental_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    _write_csv(out_dir / "paraphrase_family_runs.csv", paraphrase_runs)
    _write_csv(out_dir / "paraphrase_family_results.csv", paraphrase_aggregates)
    _write_csv(out_dir / "poison_pressure_runs.csv", pressure_runs)
    _write_csv(out_dir / "poison_pressure_results.csv", pressure_aggregates)
    _write_csv(out_dir / "false_positive_runs.csv", false_positive_runs)
    _write_csv(out_dir / "false_positive_results.csv", false_positive_aggregates)
    print(json.dumps({"status": "ok", "out_dir": str(out_dir)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
