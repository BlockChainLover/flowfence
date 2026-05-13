from __future__ import annotations

import argparse
import csv
import json
import random
from pathlib import Path
from statistics import mean, stdev
from typing import Any


METRICS = [
    "clean_utility_rate",
    "attacked_utility_rate",
    "raw_poisoned_retrieval_case_rate",
    "exposed_poisoned_retrieval_case_rate",
    "attack_manifestation_rate",
    "defense_intervention_event_rate",
    "benign_false_block_proxy_rate",
    "avg_llm_calls",
    "avg_total_tokens",
    "avg_total_token_proxy",
    "avg_wall_time_seconds",
]
REPEATS = ["v1", "repeat1", "repeat2"]


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def _rate(values: list[bool]) -> float | None:
    return None if not values else sum(1 for value in values if value) / len(values)


def _ci(values: list[float], *, samples: int = 2000, seed: int = 7) -> tuple[float | None, float | None]:
    if not values:
        return None, None
    rng = random.Random(seed)
    draws = []
    for _ in range(samples):
        sample = [values[rng.randrange(len(values))] for _ in values]
        draws.append(mean(sample))
    draws.sort()
    return draws[int(0.025 * (samples - 1))], draws[int(0.975 * (samples - 1))]


def _overhead(run_dir: Path) -> dict[str, float | None]:
    case_paths = sorted((run_dir / "case_details").glob("case_*.json"))
    calls: list[float] = []
    tokens: list[float] = []
    token_proxy: list[float] = []
    wall: list[float] = []
    for path in case_paths:
        case = _load_json(path)
        overhead = case.get("overhead_measurement", {}) or {}
        if "llm_call_count" in overhead:
            calls.append(float(overhead["llm_call_count"]))
        if overhead.get("total_tokens") is not None:
            tokens.append(float(overhead["total_tokens"]))
        if overhead.get("total_token_proxy") is not None:
            token_proxy.append(float(overhead["total_token_proxy"]))
        if overhead.get("wall_time_seconds") is not None:
            wall.append(float(overhead["wall_time_seconds"]))
        elif "wall_time_seconds" in case:
            wall.append(float(case["wall_time_seconds"]))
    return {
        "avg_llm_calls": round(mean(calls), 4) if calls else None,
        "avg_total_tokens": round(mean(tokens), 4) if tokens else None,
        "avg_total_token_proxy": round(mean(token_proxy), 4) if token_proxy else None,
        "avg_wall_time_seconds": round(mean(wall), 4) if wall else None,
    }


def _case_metric_values(run_dir: Path) -> dict[str, list[float]]:
    rows = _load_jsonl(run_dir / "case_results.jsonl")
    values = {
        "clean_utility_rate": [1.0 if row.get("benign_em") else 0.0 for row in rows],
        "attacked_utility_rate": [1.0 if row.get("adv_em") else 0.0 for row in rows],
        "raw_poisoned_retrieval_case_rate": [
            1.0 if int(row.get("adv_raw_retrieval_success", row.get("adv_retrieval_success", 0))) > 0 else 0.0
            for row in rows
        ],
        "exposed_poisoned_retrieval_case_rate": [
            1.0
            if int(row.get("adv_poisoned_content_exposed", row.get("adv_retrieval_success", 0))) > 0
            else 0.0
            for row in rows
        ],
        "attack_manifestation_rate": [1.0 if row.get("attack_manifested") else 0.0 for row in rows],
        "benign_false_block_proxy_rate": [
            1.0 if int(row.get("benign_defense_intervention_count", 0)) > 0 else 0.0 for row in rows
        ],
    }
    interventions = []
    for row in rows:
        retrievals = int(row.get("benign_overall_retrieval", 0)) + int(row.get("adv_overall_retrieval", 0))
        intervention_count = int(row.get("benign_defense_intervention_count", 0)) + int(
            row.get("adv_defense_intervention_count", 0)
        )
        if retrievals > 0:
            interventions.append(intervention_count / retrievals)
    values["defense_intervention_event_rate"] = interventions
    return values


def _run_row(results_root: Path, run_name: str, provider: str, condition: str, repeat: str) -> dict[str, Any]:
    run_dir = results_root / run_name
    metrics = _load_json(run_dir / "metrics.json")
    future = metrics["future_defense_metrics"]
    diagnostics = metrics.get("defense_diagnostics", {})
    row = {
        "provider": provider,
        "condition": condition,
        "repeat": repeat,
        "run_name": run_name,
        "artifact": f"results/{run_name}/",
        "status": metrics.get("status"),
        "resolved_model_name": metrics.get("resolved_model_name"),
        "question_count": metrics.get("question_count"),
        "clean_utility_rate": future.get("clean_utility_rate"),
        "attacked_utility_rate": future.get("attacked_utility_rate"),
        "raw_poisoned_retrieval_case_rate": future.get("raw_poisoned_retrieval_case_rate"),
        "exposed_poisoned_retrieval_case_rate": future.get("exposed_poisoned_retrieval_case_rate"),
        "attack_manifestation_rate": future.get("attack_manifestation_rate"),
        "defense_intervention_event_rate": diagnostics.get("defense_intervention_event_rate"),
        "benign_false_block_proxy_rate": diagnostics.get("benign_false_block_proxy_rate"),
    }
    row.update(_overhead(run_dir))
    return row


def _aggregate_group(rows: list[dict[str, Any]], case_values: dict[str, list[float]]) -> dict[str, Any]:
    out: dict[str, Any] = {
        "provider": rows[0]["provider"],
        "condition": rows[0]["condition"],
        "n_runs": len(rows),
        "n_cases_for_ci": len(case_values.get("clean_utility_rate", [])),
        "run_names": ";".join(row["run_name"] for row in rows),
        "artifacts": ";".join(row["artifact"] for row in rows),
    }
    for metric in METRICS:
        values = [float(row[metric]) for row in rows if row.get(metric) is not None]
        out[f"{metric}_mean"] = round(mean(values), 4) if values else None
        out[f"{metric}_sd"] = round(stdev(values), 4) if len(values) > 1 else 0.0 if values else None
        # Utility metrics are official-eval aggregates; case_results EM can diverge from
        # upstream eval parsing, so use run-level values for their descriptive CIs.
        ci_source = values if metric in {"clean_utility_rate", "attacked_utility_rate"} else case_values.get(metric, values)
        low, high = _ci([float(v) for v in ci_source if v is not None])
        out[f"{metric}_ci95_low"] = round(low, 4) if low is not None else None
        out[f"{metric}_ci95_high"] = round(high, 4) if high is not None else None
    return out


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


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize EMNLP P0 AgentPoison runs with bootstrap CIs")
    parser.add_argument("--results-root", default="results")
    parser.add_argument("--out-dir", default="artifacts/emnlp2026_p0/results")
    parser.add_argument("--providers", nargs="+", default=["minimax27", "qwen36", "kimi25"])
    parser.add_argument("--conditions", nargs="+", default=["no_defense", "static_keyword_filter", "flowfence_lite"])
    parser.add_argument("--allow-missing", action="store_true")
    args = parser.parse_args()

    results_root = Path(args.results_root)
    run_rows: list[dict[str, Any]] = []
    aggregate_rows: list[dict[str, Any]] = []
    missing: list[str] = []

    for provider in args.providers:
        for condition in args.conditions:
            rows = []
            case_values = {metric: [] for metric in METRICS}
            for repeat in REPEATS:
                if provider == "minimax27":
                    prefix_map = {
                        "no_defense": "baseline_agentpoison_fullreact_dpr_strategyqa_minimax27_triggerquery",
                        "static_keyword_filter": "baseline_agentpoison_fullreact_minimax27_triggerquery_static_keyword_filter",
                        "flowfence_lite": (
                            "method_flowfence_lite_fullreact_minimax27_triggerquery_quarantine_actioncanon"
                        ),
                    }
                    suffix = "v1" if repeat == "v1" else repeat
                    run_name = f"{prefix_map[condition]}_{suffix}"
                else:
                    run_name = f"emnlp_p0_cross_provider_{provider}_{condition}_{repeat}"
                run_dir = results_root / run_name
                if not (run_dir / "metrics.json").exists():
                    missing.append(run_name)
                    continue
                row = _run_row(results_root, run_name, provider, condition, repeat)
                rows.append(row)
                run_rows.append(row)
                if (run_dir / "case_results.jsonl").exists():
                    per_case = _case_metric_values(run_dir)
                    for metric, values in per_case.items():
                        case_values.setdefault(metric, []).extend(values)
            if rows:
                aggregate_rows.append(_aggregate_group(rows, case_values))

    if missing and not args.allow_missing:
        raise SystemExit(f"missing expected runs: {', '.join(missing)}")

    out_dir = Path(args.out_dir)
    _write_csv(out_dir / "emnlp_p0_cross_provider_runs.csv", run_rows)
    _write_csv(out_dir / "emnlp_p0_cross_provider_results.csv", aggregate_rows)
    summary = {
        "status": "ok" if not missing else "partial",
        "missing": missing,
        "run_count": len(run_rows),
        "group_count": len(aggregate_rows),
        "scope_note": (
            "Adapted AgentPoison StrategyQA full-ReAct trigger-query axis. Bootstrap CIs are case-level "
            "descriptive intervals over the fixed question subset and repeats, not a new dataset sample."
        ),
    }
    (out_dir / "emnlp_p0_cross_provider_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
