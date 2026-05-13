import argparse
import json
from pathlib import Path
from typing import Optional, Tuple


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _required_metric_block(metrics: dict) -> dict:
    if "future_defense_metrics" not in metrics:
        raise ValueError(f"metrics.json missing future_defense_metrics in {metrics}")
    return metrics["future_defense_metrics"]


def _load_baseline_target(
    results_root: Path,
    baseline_run: Optional[str],
    baseline_summary: Optional[str],
) -> Tuple[str, str, dict]:
    if baseline_summary:
        summary_path = Path(baseline_summary)
        if not summary_path.is_absolute():
            summary_path = Path.cwd() / baseline_summary
        summary_payload = _load_json(summary_path)
        task_manifest_id = summary_payload["task_manifest_id"]
        aggregate_metrics = {
            key: value["mean"] for key, value in summary_payload["aggregate_metrics"].items() if isinstance(value, dict)
        }
        return (summary_path.name, task_manifest_id, aggregate_metrics)

    if not baseline_run:
        raise ValueError("Either --baseline-run or --baseline-summary must be provided")

    baseline_dir = results_root / baseline_run
    baseline_manifest = _load_json(baseline_dir / "run_manifest.json")
    baseline_metrics = _load_json(baseline_dir / "metrics.json")
    return (
        baseline_run,
        baseline_manifest["task_manifest_id"],
        _required_metric_block(baseline_metrics),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare two pre-method runs on the fixed AgentPoison slice")
    parser.add_argument("--baseline-run", default=None)
    parser.add_argument("--baseline-summary", default=None)
    parser.add_argument("--candidate-run", required=True)
    parser.add_argument("--results-root", default="results")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    results_root = Path.cwd() / args.results_root
    candidate_dir = results_root / args.candidate_run

    candidate_manifest = _load_json(candidate_dir / "run_manifest.json")
    candidate_metrics = _load_json(candidate_dir / "metrics.json")
    baseline_label, baseline_task_manifest_id, baseline_future = _load_baseline_target(
        results_root,
        args.baseline_run,
        args.baseline_summary,
    )

    if baseline_task_manifest_id != candidate_manifest["task_manifest_id"]:
        raise ValueError("Run manifests do not share the same task_manifest_id")

    candidate_future = _required_metric_block(candidate_metrics)
    comparison = {
        "baseline_run": baseline_label,
        "candidate_run": args.candidate_run,
        "task_manifest_id": candidate_manifest["task_manifest_id"],
        "metric_keys": sorted(baseline_future.keys()),
        "baseline_future_defense_metrics": baseline_future,
        "candidate_future_defense_metrics": candidate_future,
        "deltas": {},
    }

    for key in baseline_future:
        baseline_value = baseline_future[key]
        candidate_value = candidate_future.get(key)
        if isinstance(baseline_value, (int, float)) and isinstance(candidate_value, (int, float)):
            comparison["deltas"][key] = candidate_value - baseline_value

    if args.output:
        output_path = Path(args.output)
    elif args.baseline_summary:
        output_path = candidate_dir / "comparison_vs_premethod_summary.json"
    else:
        output_path = candidate_dir / f"comparison_vs_{args.baseline_run}.json"
    output_path.write_text(json.dumps(comparison, indent=2), encoding="utf-8")
    print(json.dumps(comparison, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
