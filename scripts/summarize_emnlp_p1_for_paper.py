#!/usr/bin/env python3
"""Summarize existing EMNLP P1 artifacts for paper writing.

This script is intentionally read-only: it loads saved CSV/JSON/JSONL
artifacts and prints the paper-facing numbers used in the EMNLP draft.
It does not run experiments or call provider APIs.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


FAMILIES = [
    "factual_misinformation",
    "mixed_language",
    "soft_preference",
]

CONDITIONS = [
    "no_defense",
    "static_keyword_filter",
    "flowfence_lite",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_json(path: Path) -> Any:
    with path.open() as f:
        return json.load(f)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def rate(rows: list[dict[str, Any]], predicate) -> float:
    if not rows:
        return 0.0
    return sum(1 for row in rows if predicate(row)) / len(rows)


def summarize(root: Path) -> dict[str, Any]:
    inspector_path = root / "artifacts/emnlp2026_p1/inspector_swap/inspector_swap_summary.csv"
    benign_path = root / "artifacts/emnlp2026_p1/benign_false_quarantine/benign_false_quarantine_summary.csv"

    inspector_order = {
        "rule": 0,
        "heuristic": 1,
        "llm_judge_kimi25": 2,
        "llm_judge_minimax27": 3,
    }
    family_order = {
        "benign_instructional": 0,
        "useful_factual": 1,
        "irrelevant_harmless": 2,
        "all": 3,
    }
    inspector_rows = sorted(read_csv(inspector_path), key=lambda r: inspector_order.get(r["inspector"], 99))
    benign_rows = sorted(
        read_csv(benign_path),
        key=lambda r: (inspector_order.get(r["inspector"], 99), family_order.get(r["family"], 99)),
    )

    adaptive_rows = []
    for family in FAMILIES:
        for condition in CONDITIONS:
            run_dir = root / f"results/emnlp_p1_adaptive_{family}_{condition}_kimi25_v1"
            metrics = read_json(run_dir / "metrics.json")
            cases = read_jsonl(run_dir / "case_results.jsonl")
            detail_count = len(list((run_dir / "case_details").glob("case_*.json")))
            adaptive_rows.append(
                {
                    "family": family,
                    "condition": condition,
                    "case_results": len(cases),
                    "case_detail_files": detail_count,
                    "detected": rate(cases, lambda r: r.get("adv_poisoned_content_detected", 0) > 0),
                    "exposed": rate(cases, lambda r: r.get("adv_poisoned_content_exposed", 0) > 0),
                    "manifestation": rate(cases, lambda r: bool(r.get("attack_manifested"))),
                    "attacked_utility": metrics["future_defense_metrics"]["attacked_utility_rate"],
                    "clean_utility": metrics["future_defense_metrics"]["clean_utility_rate"],
                    "int_per_case": metrics["defense_diagnostics"]["defense_intervention_events_per_case_mode"],
                    "benign_false_block_proxy": metrics["defense_diagnostics"]["benign_false_block_proxy_rate"],
                }
            )

    return {
        "inspector_swap": inspector_rows,
        "benign_false_quarantine": benign_rows,
        "adaptive_pilot": adaptive_rows,
        "scope_note": (
            "Read-only summary of saved artifacts. Inspector swap is fixed-trace replay; "
            "LLM judges use a capped 50-event subset; adaptive pilot uses corrected "
            "case-level poisoned-content detected/exposed fields."
        ),
    }


def fmt_float(value: Any) -> str:
    if value in ("", None):
        return ""
    try:
        return f"{float(value):.3f}"
    except (TypeError, ValueError):
        return str(value)


def print_markdown(summary: dict[str, Any]) -> None:
    print("# EMNLP P1 Paper Summary")
    print()
    print(summary["scope_note"])
    print()

    print("## Inspector-Swap Replay")
    print()
    print("| Inspector | Events | Poison/Clean | Recall | Exposed | FQ | Cost |")
    print("|---|---:|---:|---:|---:|---:|---:|")
    for row in summary["inspector_swap"]:
        cost = (
            f"{float(row['mean_local_microseconds']):.2f} us/event"
            if row.get("mean_local_microseconds")
            else f"{int(row['total_llm_tokens'])} tokens"
        )
        poison_clean = f"{row['poisoned_event_count']}/{row['clean_event_count']}"
        print(
            "| {inspector} | {events} | {poison_clean} | {recall} | {exposed} | {fq} | {cost} |".format(
                inspector=row["inspector"],
                events=row["event_count"],
                poison_clean=poison_clean,
                recall=fmt_float(row["poison_recall"]),
                exposed=fmt_float(row["poison_exposed_rate"]),
                fq=fmt_float(row["false_quarantine_rate"]),
                cost=cost,
            )
        )
    print()

    print("## Benign False-Quarantine Replay")
    print()
    print("| Inspector | Family | Records | FQ | Intervention |")
    print("|---|---|---:|---:|---:|")
    for row in summary["benign_false_quarantine"]:
        print(
            "| {inspector} | {family} | {records} | {fq} | {intervention} |".format(
                inspector=row["inspector"],
                family=row["family"],
                records=row["record_count"],
                fq=fmt_float(row["false_quarantine_rate"]),
                intervention=fmt_float(row["intervention_rate"]),
            )
        )
    print()

    print("## Adaptive Poisoning Pilot")
    print()
    print("| Family | Condition | Cases | Detail files | Detected | Exposed | Man. | AtkU |")
    print("|---|---|---:|---:|---:|---:|---:|---:|")
    for row in summary["adaptive_pilot"]:
        print(
            "| {family} | {condition} | {cases} | {details} | {detected:.2f} | {exposed:.2f} | {man:.2f} | {atku:.2f} |".format(
                family=row["family"],
                condition=row["condition"],
                cases=row["case_results"],
                details=row["case_detail_files"],
                detected=row["detected"],
                exposed=row["exposed"],
                man=row["manifestation"],
                atku=row["attacked_utility"],
            )
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."), help="Repository root")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    summary = summarize(args.root)
    if args.format == "json":
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print_markdown(summary)


if __name__ == "__main__":
    main()
