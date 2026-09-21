#!/usr/bin/env python3
"""Recompute descriptive six-cluster R3 statistics from preserved safe Git evidence.

This performs no model invocation or outcome evaluation: it aggregates the saved
episode outcome fields. R3 is the controlled mechanism study in the revised manuscript.
"""

from __future__ import annotations

import argparse
import csv
import io
import itertools
import json
import math
import subprocess
from fractions import Fraction
from pathlib import Path


SOURCE_COMMIT = "9615ca34d166c8c9f75c0c037626956512b0c251"
SOURCE_ROOT = "artifacts/aamas2027/R3_CONFIRMATORY/"
CONDITIONS = ("clean", "heldout_registered_A", "heldout_registered_B")
R2 = "flowfence_lite_nonoracle_r2"
IFC = "ifc_safeview"


def git_text(repo: Path, commit: str, path: str) -> str:
    return subprocess.check_output(
        ["git", "show", f"{commit}:{path}"], cwd=repo
    ).decode("utf-8")


def cluster_statistics(values: list[Fraction]) -> dict:
    """Exact enumeration; the fixed six clusters yield 6**6 ordered resamples."""
    n = len(values)
    if n != 6:
        raise ValueError("This descriptive analysis is specified for six task clusters")
    bootstrap = sorted(
        sum(sample, Fraction()) / n
        for sample in itertools.product(values, repeat=n)
    )
    positive = sum(value > 0 for value in values)
    negative = sum(value < 0 for value in values)
    nonzero = positive + negative
    sign_p = (
        min(
            Fraction(1),
            Fraction(
                2 * sum(math.comb(nonzero, k) for k in range(min(positive, negative) + 1)),
                2**nonzero,
            ),
        )
        if nonzero
        else None
    )
    mean = sum(values, Fraction()) / n
    percentile_indices = [
        math.ceil(probability * len(bootstrap)) - 1
        for probability in (Fraction(1, 40), Fraction(39, 40))
    ]
    return {
        "task_clusters": n,
        "mean": float(mean),
        "mean_exact": str(mean),
        "differences": [float(value) for value in values],
        "differences_exact": [str(value) for value in values],
        "bootstrap_95_percentile_interval": [
            float(bootstrap[index]) for index in percentile_indices
        ],
        "bootstrap_resamples_enumerated": len(bootstrap),
        "negative_clusters": negative,
        "positive_clusters": positive,
        "tie_clusters": n - nonzero,
        "exact_two_sided_sign_p": float(sign_p) if sign_p is not None else None,
    }


def recompute(rows: list[dict], saved_clusters: list[dict]) -> dict:
    index = {
        (row["task_id"], row["condition"], row["replicate_id"], row["defense"]): row
        for row in rows
    }
    tasks = sorted({row["task_id"] for row in rows})
    if len(rows) != 108 or len(index) != 108 or len(tasks) != 6:
        raise ValueError("Expected 108 unique registered episodes across six tasks")
    results = {}
    for condition in CONDITIONS:
        privacy, utility, matched_utility, details = [], [], [], []
        for task in tasks:
            leak_differences, utility_differences, matched_differences = [], [], []
            for replicate in (1, 2, 3):
                r2 = index[task, condition, replicate, R2]
                ifc = index[task, condition, replicate, IFC]
                utility_difference = int(r2["task_success"]) - int(ifc["task_success"])
                utility_differences.append(utility_difference)
                if r2["status"] == ifc["status"] == "completed":
                    leak_differences.append(
                        r2["episode_reconstructable_disclosure"]
                        - ifc["episode_reconstructable_disclosure"]
                    )
                    matched_differences.append(utility_difference)
            if not leak_differences:
                raise ValueError(f"No completed matched pairs for {task}/{condition}")
            privacy_mean = Fraction(sum(leak_differences), len(leak_differences))
            utility_mean = Fraction(sum(utility_differences), 3)
            matched_mean = Fraction(sum(matched_differences), len(matched_differences))
            saved = next(
                row for row in saved_clusters
                if row["condition"] == condition and row["task_id"] == task
            )
            for calculated, field in (
                (privacy_mean, "paired_leak_difference"),
                (utility_mean, "task_success_difference"),
                (matched_mean, "matched_task_success_difference"),
            ):
                # Original CSV serializes repeating fractions as decimal floats.
                if abs(float(calculated) - float(saved[field])) > 1e-12:
                    raise ValueError(f"Saved cluster disagreement: {task}/{condition}/{field}")
            if len(leak_differences) != int(saved["matched_completed_pairs"]):
                raise ValueError(f"Saved matched-pair count disagrees for {task}/{condition}")
            privacy.append(privacy_mean)
            utility.append(utility_mean)
            matched_utility.append(matched_mean)
            details.append({
                "task_id": task,
                "matched_completed_pairs": len(leak_differences),
                "privacy_difference_exact": str(privacy_mean),
                "registered_utility_difference_exact": str(utility_mean),
                "matched_utility_difference_exact": str(matched_mean),
            })
        results[condition] = {
            "privacy_completed_matched": cluster_statistics(privacy),
            "utility_all_registered": cluster_statistics(utility),
            "utility_completed_matched": cluster_statistics(matched_utility),
            "task_rows": details,
        }
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--source-commit", default=SOURCE_COMMIT)
    parser.add_argument(
        "--output", type=Path,
        default=Path("artifacts/aamas2027_paper_revision/controlled_cluster_reanalysis.json"),
    )
    parser.add_argument(
        "--cluster-csv", type=Path,
        default=Path("artifacts/aamas2027_paper_revision/controlled_task_clusters.csv"),
        help="Write a byte-preserving safe snapshot of the historical cluster CSV",
    )
    parser.add_argument(
        "--verify-against", type=Path,
        default=Path("artifacts/aamas2027_paper_revision/recognizer_controlled.json"),
        help="Existing audit whose conditions must agree exactly before output is written",
    )
    args = parser.parse_args()
    episode_path = SOURCE_ROOT + "formal/episodes.jsonl"
    cluster_path = SOURCE_ROOT + "derived/paired_task_cluster.csv"
    episode_text = git_text(args.repo, args.source_commit, episode_path)
    cluster_text = git_text(args.repo, args.source_commit, cluster_path)
    rows = [json.loads(line) for line in episode_text.splitlines() if line]
    conditions = recompute(rows, list(csv.DictReader(io.StringIO(cluster_text))))
    existing = json.loads(args.verify_against.read_text())
    if conditions != existing["conditions"]:
        raise ValueError("Recomputed conditions differ from the saved paper-revision audit")
    result = {
        "scope": existing["scope"],
        "sources": {
            "git_commit": args.source_commit,
            "episodes": episode_path,
            "cluster_table": cluster_path,
            "preregistration": "artifacts/aamas2027/R3_EXPERIMENT_PREREGISTRATION.md",
        },
        "method": existing["method"],
        "conditions": conditions,
        "validation": {
            "episodes": len(rows),
            "historical_cluster_table_matches": True,
            "saved_revision_audit_matches": True,
            "model_calls": 0,
            "evaluator_calls": 0,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    args.cluster_csv.parent.mkdir(parents=True, exist_ok=True)
    args.cluster_csv.write_text(cluster_text)
    print(json.dumps({"output": str(args.output), "cluster_csv": str(args.cluster_csv),
                      "audit_match": True, "episodes": len(rows)}))


if __name__ == "__main__":
    main()
