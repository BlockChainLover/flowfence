import argparse
import json
from pathlib import Path
from typing import List


FROZEN_METRICS = [
    "clean_utility_rate",
    "attacked_utility_rate",
    "attack_manifestation_rate",
    "poisoned_retrieval_case_rate",
    "poisoned_retrieval_gap_mean",
]


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _metric_keys(metrics: dict) -> List[str]:
    future = metrics.get("future_defense_metrics")
    if not isinstance(future, dict):
        raise ValueError("metrics.json missing future_defense_metrics block")
    return sorted(future.keys())


def _metric_stats(values: List[float]) -> dict:
    return {
        "mean": sum(values) / len(values),
        "min": min(values),
        "max": max(values),
    }


def _directionally_stable(values: List[float]) -> bool:
    all_nonnegative = all(value >= 0 for value in values)
    all_nonpositive = all(value <= 0 for value in values)
    return all_nonnegative or all_nonpositive


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize multiple pre-method reruns on the same AgentPoison manifest")
    parser.add_argument("--runs", nargs="+", required=True)
    parser.add_argument("--results-root", default="results")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    if len(args.runs) != 3:
        raise ValueError("Expected exactly 3 rerun directories for the pre-method summary")

    results_root = Path.cwd() / args.results_root
    loaded_runs = []
    metric_key_sets = []
    manifest_ids = []
    question_indices_sets = []

    for run_name in args.runs:
        run_dir = results_root / run_name
        manifest = _load_json(run_dir / "run_manifest.json")
        metrics = _load_json(run_dir / "metrics.json")
        if metrics.get("status") != "ok":
            raise ValueError(f"Run {run_name} did not finish successfully")
        loaded_runs.append(
            {
                "run_name": run_name,
                "run_dir": str(run_dir),
                "manifest": manifest,
                "metrics": metrics,
                "future": metrics["future_defense_metrics"],
            }
        )
        metric_key_sets.append(_metric_keys(metrics))
        manifest_ids.append(manifest["task_manifest_id"])
        question_indices_sets.append(manifest["question_indices"])

    schema_consistent = all(keys == metric_key_sets[0] for keys in metric_key_sets[1:])
    manifest_consistent = all(manifest_id == manifest_ids[0] for manifest_id in manifest_ids[1:])
    question_indices_consistent = all(indices == question_indices_sets[0] for indices in question_indices_sets[1:])

    aggregate_metrics = {}
    for key in FROZEN_METRICS:
        values = [run["future"][key] for run in loaded_runs]
        aggregate_metrics[key] = _metric_stats(values)

    attack_values = [run["future"]["attack_manifestation_rate"] for run in loaded_runs]
    directionally_stable = _directionally_stable(attack_values)

    summary = {
        "summary_type": "premethod_rerun_bundle",
        "task_manifest_id": manifest_ids[0],
        "run_count": len(loaded_runs),
        "runs": [
            {
                "run_name": run["run_name"],
                "metrics_path": f"{run['run_dir']}/metrics.json",
                "status": run["metrics"]["status"],
                "future_defense_metrics": run["future"],
            }
            for run in loaded_runs
        ],
        "schema_consistency": {
            "metric_keys_match": schema_consistent,
            "metric_keys": metric_key_sets[0],
        },
        "manifest_consistency": {
            "task_manifest_id_match": manifest_consistent,
            "question_indices_match": question_indices_consistent,
            "question_indices": question_indices_sets[0],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_checks": {
            "artifact_schema_match": schema_consistent,
            "metric_keys_match": schema_consistent,
            "manifest_match": manifest_consistent and question_indices_consistent,
            "attack_manifestation_directionally_stable": directionally_stable,
            "report_clean_and_attacked_utility_as_mean_min_max": True,
        },
    }

    output_path = Path(args.output) if args.output else results_root / f"premethod_summary_{manifest_ids[0]}.json"
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
