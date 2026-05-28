#!/usr/bin/env python3
"""Review generated paper-facing tables against committed evidence artifacts."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any


NA = "NA"
RAW_SECRET_MARKERS = [
    "$4800",
    "supplier breach investigation",
    "CUST-8831-PRIVATE",
    "sk-internal-demo-token",
]

REQUIRED_TABLES = [
    "table_1_p0_agentpoison",
    "table_2_p1_synthetic",
    "table_3_minimax_postfix_smoke",
    "table_4_claims_matrix",
    "table_5_evidence_boundaries",
]

P0_MAIN = Path("results/baseline_agentpoison_fullreact_minimax27_small_matrix_summary.json")
P0_STATIC = Path("results/baseline_agentpoison_fullreact_minimax27_static_keyword_filter_weak_comparator_summary.json")
P0_REWRITE = Path("results/baseline_agentpoison_fullreact_minimax27_rewrite_only_weak_comparator_summary.json")
P0_HELDOUT = Path("results/baseline_agentpoison_fullreact_minimax27_heldout_instruction_matrix_summary.json")
MINIMAX_SUMMARY = Path("artifacts/minimax_p1_smoke_postfix/summary_18run.json")
MINIMAX_AUDIT = Path("artifacts/minimax_p1_smoke_postfix_audit/audit_summary.json")
MINIMAX_FAILURES = Path("artifacts/minimax_p1_smoke_postfix_audit/failure_breakdown.jsonl")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def as_float(value: Any) -> float | None:
    if value in (None, "", NA):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def eq_number(observed: Any, expected: Any, tolerance: float = 1e-6) -> bool:
    observed_f = as_float(observed)
    expected_f = as_float(expected)
    return observed_f is not None and expected_f is not None and abs(observed_f - expected_f) <= tolerance


def issue(
    issues: list[dict[str, Any]],
    severity: str,
    table: str,
    row_id: str,
    check_name: str,
    expected: Any,
    observed: Any,
    evidence_path: str,
    message: str,
) -> None:
    issues.append(
        {
            "severity": severity,
            "table": table,
            "row_id": row_id,
            "check_name": check_name,
            "expected": expected,
            "observed": observed,
            "evidence_path": evidence_path,
            "message": message,
        }
    )


def find_row(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str] | None:
    for row in rows:
        if row.get(key) == value:
            return row
    return None


def metric_mean(group: dict[str, Any], name: str) -> Any:
    value = group.get("aggregate", {}).get(name, {})
    if isinstance(value, dict):
        return value.get("mean")
    return None


def check_metric(
    issues: list[dict[str, Any]],
    table: str,
    row: dict[str, str] | None,
    row_id: str,
    column: str,
    expected: Any,
    evidence_path: Path,
) -> None:
    if row is None:
        issue(issues, "ERROR", table, row_id, "row_present", "present", "missing", str(evidence_path), f"Missing row {row_id}.")
        return
    observed = row.get(column)
    if not eq_number(observed, expected):
        issue(issues, "ERROR", table, row_id, f"value_{column}", expected, observed, str(evidence_path), f"{column} contradicts committed evidence.")


def check_required_files(tables_dir: Path, issues: list[dict[str, Any]]) -> None:
    for stem in REQUIRED_TABLES:
        for suffix in [".csv", ".md"]:
            path = tables_dir / f"{stem}{suffix}"
            if not path.exists():
                issue(issues, "ERROR", stem, stem, "required_file_exists", "present", "missing", str(path), f"Required table file missing: {path}")


def check_raw_secrets(tables_dir: Path, output_dir: Path, issues: list[dict[str, Any]], max_preview_chars: int) -> None:
    for path in list(tables_dir.glob("*")) + list(output_dir.glob("*")):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for marker in RAW_SECRET_MARKERS:
            if marker in text:
                issue(issues, "ERROR", path.name, path.name, "raw_secret_absent", "absent", "[REDACTED_RAW_SECRET_MARKER]", str(path), "Raw synthetic secret marker appears in table or review output.")


def check_table_1(tables_dir: Path, issues: list[dict[str, Any]]) -> None:
    table = "table_1_p0_agentpoison"
    path = tables_dir / f"{table}.csv"
    if not path.exists():
        return
    rows = read_csv(path)
    main = read_json(P0_MAIN)
    groups = main.get("groups", {})
    no_defense = find_row(rows, "condition", "no_defense")
    flowfence = find_row(rows, "condition", "flowfence_lite_quarantine_actioncanon")
    check_metric(issues, table, no_defense, "no_defense", "exposed_poisoned_retrieval_case_rate_mean", metric_mean(groups["no_defense"], "exposed_poisoned_retrieval_case_rate"), P0_MAIN)
    check_metric(issues, table, flowfence, "flowfence_lite_quarantine_actioncanon", "exposed_poisoned_retrieval_case_rate_mean", 0.0, P0_MAIN)
    check_metric(issues, table, flowfence, "flowfence_lite_quarantine_actioncanon", "attack_manifestation_rate_mean", 0.0, P0_MAIN)
    if no_defense and flowfence:
        nd = as_float(no_defense.get("exposed_poisoned_retrieval_case_rate_mean"))
        ff = as_float(flowfence.get("exposed_poisoned_retrieval_case_rate_mean"))
        if nd is None or ff is None or not nd > ff:
            issue(issues, "ERROR", table, "no_defense_vs_flowfence", "exposure_order", "no_defense > flowfence", f"{nd} <= {ff}", str(P0_MAIN), "No-defense exposure should be greater than FlowFence exposure.")
    for row in rows:
        provider = row.get("provider", "").lower()
        if "minimax" not in provider:
            issue(issues, "ERROR", table, row.get("condition", ""), "provider_minimax_only", "contains minimax", row.get("provider"), row.get("evidence_path", ""), "P0 row does not identify MiniMax provider/profile.")
        condition = row.get("condition", "")
        caveat = row.get("caveat", "").lower()
        if condition == "static_keyword_filter_weak_comparator" and not ("known-trigger" in caveat and "same-axis" in caveat):
            issue(issues, "ERROR", table, condition, "static_keyword_caveat", "known-trigger and same-axis caveat", row.get("caveat"), str(P0_STATIC), "Static keyword row lacks required weak-baseline caveat.")
        if condition == "rewrite_only_weak_comparator" and not ("same" in caveat and "weak" in caveat):
            issue(issues, "ERROR", table, condition, "rewrite_caveat", "same-axis weak comparator caveat", row.get("caveat"), str(P0_REWRITE), "Rewrite-only row lacks required weak-comparator caveat.")
        if condition.startswith("heldout_") and not ("stress" in caveat and "not broad" in caveat):
            issue(issues, "ERROR", table, condition, "heldout_caveat", "stress-test only / not broad caveat", row.get("caveat"), str(P0_HELDOUT), "Held-out row lacks required stress-test caveat.")
    issue(issues, "INFO", table, "table", "review_complete", "P0 value and caveat checks", "passed unless ERROR rows are present", str(path), "Reviewed P0 AgentPoison table.")


def check_table_2(tables_dir: Path, issues: list[dict[str, Any]]) -> None:
    table = "table_2_p1_synthetic"
    path = tables_dir / f"{table}.csv"
    if not path.exists():
        return
    rows = read_csv(path)
    for row in rows:
        label = row.get("evidence_axis", "")
        if row.get("provider_calls_enabled") != "false":
            issue(issues, "ERROR", table, label, "provider_calls_disabled", "false", row.get("provider_calls_enabled"), row.get("evidence_path", ""), "Deterministic synthetic table must have provider calls disabled.")
        caveat = row.get("caveat", "").lower()
        if "synthetic" not in caveat and "deterministic" not in caveat:
            issue(issues, "WARN", table, label, "synthetic_caveat", "synthetic/deterministic caveat", row.get("caveat"), row.get("evidence_path", ""), "Synthetic row caveat could be clearer.")
        if label == "initial_deterministic_mas_sweep" and row.get("topology_effect_observed") == "true":
            issue(issues, "ERROR", table, label, "initial_topology_effect", "not true", "true", row.get("evidence_path", ""), "Initial deterministic sweep should not claim topology effect.")
        if label == "strengthened_deterministic_mas_benchmark" and row.get("topology_effect_observed") != "true":
            issue(issues, "ERROR", table, label, "strengthened_topology_effect", "true", row.get("topology_effect_observed"), row.get("evidence_path", ""), "Strengthened benchmark should report topology effect observed.")
    issue(issues, "INFO", table, "table", "review_complete", "synthetic scope checks", "passed unless ERROR/WARN rows are present", str(path), "Reviewed P1 synthetic table.")


def check_table_3(tables_dir: Path, issues: list[dict[str, Any]]) -> None:
    table = "table_3_minimax_postfix_smoke"
    path = tables_dir / f"{table}.csv"
    if not path.exists():
        return
    rows = read_csv(path)
    summary = read_json(MINIMAX_SUMMARY)
    audit = read_json(MINIMAX_AUDIT)
    failures = read_jsonl(MINIMAX_FAILURES)
    overall = summary["overall_metrics"]
    aggregate = find_row(rows, "group", "aggregate")
    expected_aggregate = {
        "completed_runs": summary["completed_run_count"],
        "failed_runs": summary["failed_run_count"],
        "task_success_rate": overall["task_success_rate"],
        "unauthorized_raw_leakage_mean": overall["unauthorized_raw_leakage_mean"],
        "external_leakage_mean": overall["external_leakage_mean"],
        "cascade_size_mean": overall["cascade_size_mean"],
        "privilege_reach_mean": overall["privilege_reach_mean"],
    }
    for column, expected in expected_aggregate.items():
        check_metric(issues, table, aggregate, "aggregate", column, expected, MINIMAX_SUMMARY)
    if aggregate and aggregate.get("topology_effect_observed") != "true":
        issue(issues, "ERROR", table, "aggregate", "topology_effect_observed", "true", aggregate.get("topology_effect_observed"), str(MINIMAX_SUMMARY), "Aggregate row should record topology_effect_observed=true.")
    for defense, status_key in [
        ("flowfence_lite_subset", "flowfence_group_status"),
        ("none_subset", "no_defense_group_status"),
        ("prompt_filter_subset", "prompt_filter_group_status"),
    ]:
        row = find_row(rows, "group", defense)
        status = audit[status_key]
        for column, metric_key in [
            ("task_success_rate", "task_success_rate"),
            ("unauthorized_raw_leakage_mean", "unauthorized_raw_leakage_mean"),
            ("external_leakage_mean", "external_leakage_mean"),
        ]:
            check_metric(issues, table, row, defense, column, status[metric_key], MINIMAX_AUDIT)
    failure_labels = {f"{f['topology']} / {f['attack']} / {f['defense']} / seed={f['seed']}" for f in failures}
    table_text = path.read_text(encoding="utf-8")
    for label in failure_labels:
        if label not in table_text:
            issue(issues, "ERROR", table, label, "failure_group_listed", "listed", "missing", str(MINIMAX_FAILURES), "Prompt-filter failure group missing from Table 3.")
    for row in rows:
        if row.get("provider") != "minimax":
            issue(issues, "ERROR", table, row.get("group", ""), "provider_minimax_only", "minimax", row.get("provider"), row.get("evidence_path", ""), "MiniMax smoke table contains non-MiniMax active provider.")
        if "broad real-model robustness" in row.get("caveat", "").lower():
            continue
        issue(issues, "WARN", table, row.get("group", ""), "minimax_smoke_caveat", "small smoke / not broad robustness caveat", row.get("caveat"), row.get("evidence_path", ""), "MiniMax row caveat could more explicitly mention not broad real-model robustness.")
    issue(issues, "INFO", table, "table", "review_complete", "MiniMax smoke checks", "passed unless ERROR/WARN rows are present", str(path), "Reviewed MiniMax post-fix smoke table.")


def check_table_4(tables_dir: Path, issues: list[dict[str, Any]]) -> None:
    table = "table_4_claims_matrix"
    path = tables_dir / f"{table}.csv"
    if not path.exists():
        return
    rows = read_csv(path)
    unsupported_needles = [
        "non-minimax generalization",
        "broad real-model robustness",
        "production safety",
        "official agentpoison reproduction",
        "full 252-run real minimax matrix",
        "real-model multi-seed robustness",
    ]
    text = path.read_text(encoding="utf-8").lower()
    for needle in unsupported_needles[:4]:
        if needle not in text:
            issue(issues, "ERROR", table, needle, "unsupported_claim_present", "present", "missing", str(path), "Required unsupported claim boundary is missing from claims matrix.")
    for row in rows:
        claim_text = " ".join([row.get("claim", ""), row.get("caveat", ""), row.get("supported_status", "")]).lower()
        if "non-minimax" in claim_text and "unsupported" not in row.get("supported_status", "").lower():
            issue(issues, "ERROR", table, row.get("claim_id", ""), "non_minimax_unsupported", "unsupported", row.get("supported_status"), row.get("evidence_path", ""), "Non-MiniMax generalization is marked as supported.")
        if "production safety" in claim_text and "unsupported" not in row.get("supported_status", "").lower():
            issue(issues, "ERROR", table, row.get("claim_id", ""), "production_safety_unsupported", "unsupported", row.get("supported_status"), row.get("evidence_path", ""), "Production safety claim is marked as supported.")
        if "official agentpoison" in claim_text and "unsupported" not in row.get("supported_status", "").lower():
            issue(issues, "ERROR", table, row.get("claim_id", ""), "official_agentpoison_unsupported", "unsupported", row.get("supported_status"), row.get("evidence_path", ""), "Official AgentPoison reproduction is marked as supported.")
        if row.get("supported_status", "").lower() == "unsupported" and row.get("ready_for_paper", "").lower() not in {"no", "yes, limitation/safety-motivation only"}:
            issue(issues, "WARN", table, row.get("claim_id", ""), "unsupported_ready_status", "no or limitation-only", row.get("ready_for_paper"), row.get("evidence_path", ""), "Unsupported claim has unexpected ready_for_paper status.")
    issue(issues, "INFO", table, "table", "review_complete", "claims scope checks", "passed unless ERROR/WARN rows are present", str(path), "Reviewed claims matrix.")


def check_table_5(tables_dir: Path, issues: list[dict[str, Any]]) -> None:
    table = "table_5_evidence_boundaries"
    path = tables_dir / f"{table}.csv"
    if not path.exists():
        return
    rows = read_csv(path)
    labels = {row.get("evidence_scope", ""): row for row in rows}
    required = [
        "P0 AgentPoison retrieval-memory comparator",
        "P1 deterministic synthetic MAS",
        "P1 MiniMax 18-run smoke",
        "Not yet done: non-MiniMax providers",
        "Not yet done: real browser / desktop agents",
        "Not yet done: learned graph risk scorer",
    ]
    for label in required:
        if label not in labels:
            issue(issues, "ERROR", table, label, "boundary_row_present", "present", "missing", str(path), "Required evidence-boundary row missing.")
    p0 = labels.get("P0 AgentPoison retrieval-memory comparator", {})
    if "retrieval-memory" not in p0.get("evidence_scope", "").lower() and "retrieval-memory" not in p0.get("main_caveat", "").lower():
        issue(issues, "ERROR", table, "P0", "p0_retrieval_memory_scope", "retrieval-memory", p0, str(path), "P0 row does not state retrieval-memory scope.")
    synthetic = labels.get("P1 deterministic synthetic MAS", {})
    if synthetic.get("provider_calls_enabled") != "false":
        issue(issues, "ERROR", table, "P1 deterministic synthetic MAS", "provider_calls_disabled", "false", synthetic.get("provider_calls_enabled"), str(path), "Synthetic row should have provider calls disabled.")
    non_minimax = labels.get("Not yet done: non-MiniMax providers", {})
    if "unsupported" not in " ".join(non_minimax.values()).lower() and "not done" not in " ".join(non_minimax.values()).lower():
        issue(issues, "ERROR", table, "Not yet done: non-MiniMax providers", "non_minimax_boundary", "unsupported/not done", non_minimax, str(path), "Non-MiniMax provider boundary is not explicit.")
    issue(issues, "INFO", table, "table", "review_complete", "evidence boundary checks", "passed unless ERROR/WARN rows are present", str(path), "Reviewed evidence boundaries.")


def write_outputs(output_dir: Path, issues: list[dict[str, Any]], strict: bool) -> int:
    output_dir.mkdir(parents=True, exist_ok=True)
    counts = Counter(i["severity"] for i in issues)
    report = {
        "schema_version": "flowfence_paper_table_review_v1",
        "status": "fail" if counts.get("ERROR", 0) else "pass",
        "issue_counts": {"ERROR": counts.get("ERROR", 0), "WARN": counts.get("WARN", 0), "INFO": counts.get("INFO", 0)},
        "tables_reviewed": REQUIRED_TABLES,
        "provider_boundary": "MiniMax is the only real provider represented.",
        "raw_data_boundary": "Raw traces, raw provider outputs, prompts, event JSONL, policy JSONL, per-run metrics, credentials, and secrets are not included.",
        "table_values_inconsistent": any(i["severity"] == "ERROR" and i["check_name"].startswith("value_") for i in issues),
        "unsupported_claim_overmarked": any(i["severity"] == "ERROR" and "unsupported" in i["check_name"] for i in issues),
        "raw_secret_found": any(i["severity"] == "ERROR" and i["check_name"] == "raw_secret_absent" for i in issues),
        "issues": issues,
    }
    (output_dir / "table_review_report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with (output_dir / "table_issues.jsonl").open("w", encoding="utf-8") as f:
        for item in issues:
            f.write(json.dumps(item, sort_keys=True) + "\n")
    md = [
        "# Paper Table Review Report",
        "",
        f"- Status: `{report['status']}`",
        f"- ERROR count: `{counts.get('ERROR', 0)}`",
        f"- WARN count: `{counts.get('WARN', 0)}`",
        f"- INFO count: `{counts.get('INFO', 0)}`",
        f"- Table values inconsistent with source evidence: `{report['table_values_inconsistent']}`",
        f"- Unsupported claim overmarked: `{report['unsupported_claim_overmarked']}`",
        f"- Raw secret appeared: `{report['raw_secret_found']}`",
        "",
        "## Tables reviewed",
    ]
    for table in REQUIRED_TABLES:
        md.append(f"- `{table}`")
    md.extend(["", "## Issues"])
    if issues:
        md.append("| severity | table | row | check | message |")
        md.append("| --- | --- | --- | --- | --- |")
        for item in issues:
            md.append(f"| {item['severity']} | {item['table']} | {item['row_id']} | {item['check_name']} | {str(item['message']).replace('|', '/')} |")
    else:
        md.append("- No issues recorded.")
    md.extend([
        "",
        "## Interpretation",
        "",
        "The generated paper-facing tables are consistent with committed high-level evidence unless ERROR issues are listed above. Raw traces and provider outputs are intentionally not included. MiniMax is the only real provider represented.",
        "",
    ])
    (output_dir / "table_review_report.md").write_text("\n".join(md), encoding="utf-8")
    readme = """# Paper Tables Review

This directory contains a review of paper-facing tables generated from committed high-level evidence.

Raw traces and provider outputs are intentionally not included.

MiniMax is the only real provider represented.

Tables still require human review before being copied into a paper.

Unsupported claims remain unsupported.
"""
    (output_dir / "README.md").write_text(readme, encoding="utf-8")
    if strict and counts.get("ERROR", 0):
        return 1
    return 0


def run_review(tables_dir: Path, output_dir: Path, strict: bool, max_preview_chars: int) -> int:
    issues: list[dict[str, Any]] = []
    check_required_files(tables_dir, issues)
    check_table_1(tables_dir, issues)
    check_table_2(tables_dir, issues)
    check_table_3(tables_dir, issues)
    check_table_4(tables_dir, issues)
    check_table_5(tables_dir, issues)
    check_raw_secrets(tables_dir, output_dir, issues, max_preview_chars)
    return write_outputs(output_dir, issues, strict)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Review paper-facing FlowFence-Lite tables against committed evidence summaries.")
    parser.add_argument("--tables-dir", default="artifacts/paper_tables", help="Directory containing generated paper tables.")
    parser.add_argument("--output-dir", default="artifacts/paper_tables_review", help="Directory for review report artifacts.")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero when ERROR-level issues are found.")
    parser.add_argument("--max-preview-chars", type=int, default=200, help="Maximum preview length for detected raw-secret snippets.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return run_review(Path(args.tables_dir), Path(args.output_dir), args.strict, args.max_preview_chars)


if __name__ == "__main__":
    raise SystemExit(main())
