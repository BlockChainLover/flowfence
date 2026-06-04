#!/usr/bin/env python3
"""Export redacted qualitative case studies from committed high-level evidence.

The exporter intentionally consumes summary/audit artifacts and optional safe
trace previews only. It does not read full traces, prompts, provider responses,
or policy decision logs.
"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SYNTHETIC_MARKERS = (
    "$4800",
    "supplier breach investigation",
    "CUST-8831-PRIVATE",
    "sk-internal-demo-token",
)

FORBIDDEN_OUTPUT_PHRASES = (
    "raw provider output",
    "full raw prompt",
    "events.full.jsonl content",
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def load_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def redact_text(value: Any, max_chars: int | None = None) -> str:
    text = "" if value is None else str(value)
    replacements = {
        "$4800": "[REDACTED_NUMERIC_LIMIT]",
        "supplier breach investigation": "[REDACTED_INTERNAL_CAUSE]",
        "CUST-8831-PRIVATE": "[REDACTED_CUSTOMER_REFERENCE]",
        "sk-internal-demo-token": "[REDACTED_CREDENTIAL_MARKER]",
    }
    for marker, replacement in replacements.items():
        text = text.replace(marker, replacement)
    if max_chars is not None and len(text) > max_chars:
        return text[: max(0, max_chars - 1)] + "…"
    return text


def find_row(rows: list[dict[str, Any]], **criteria: Any) -> dict[str, Any] | None:
    for row in rows:
        if all(str(row.get(key)) == str(value) for key, value in criteria.items()):
            return row
    return None


def metrics_from_failure(row: dict[str, Any] | None) -> dict[str, Any]:
    if not row:
        return {"source_status": "not found in committed summary"}
    return {
        "task_success": row.get("task_success"),
        "unauthorized_raw_leakage": row.get("unauthorized_raw_leakage"),
        "external_leakage": row.get("external_leakage"),
        "cascade_size": row.get("cascade_size"),
        "privilege_reach": row.get("privilege_reach"),
        "failure_type": row.get("failure_type"),
    }


def metrics_from_group(row: dict[str, str] | None) -> dict[str, Any]:
    if not row:
        return {"source_status": "not found in committed summary"}
    keys = (
        "run_count",
        "task_success_rate",
        "unauthorized_raw_leakage_mean",
        "external_leakage_mean",
        "cascade_size_mean",
        "privilege_reach_mean",
        "oracle_annotation_used_true_count",
    )
    return {key: row.get(key, "NA") for key in keys if key in row}


def comparison_summary(summary: dict[str, Any], key: str) -> str:
    block = summary.get(key, {})
    raw = block.get("unauthorized_raw_leakage", {})
    external = block.get("external_leakage", {})
    task = block.get("task_success", {})
    return (
        f"raw improves {raw.get('improves', 'NA')}/ties {raw.get('ties', 'NA')}; "
        f"external improves {external.get('improves', 'NA')}/ties {external.get('ties', 'NA')}; "
        f"task success improves {task.get('improves', 'NA')}/ties {task.get('ties', 'NA')}"
    )


def collect_safe_snippets(
    runs_root: Path | None,
    include_safe_trace_snippets: bool,
    max_events: int,
    max_preview_chars: int,
) -> tuple[bool, list[dict[str, Any]], str]:
    if not include_safe_trace_snippets:
        return False, [], "safe trace snippets not requested"
    if runs_root is None or not runs_root.exists():
        return False, [], "safe trace unavailable"

    snippets: list[dict[str, Any]] = []
    for safe_path in sorted(runs_root.rglob("events.safe.jsonl")):
        if len(snippets) >= max_events:
            break
        for line in safe_path.read_text(encoding="utf-8").splitlines():
            if len(snippets) >= max_events:
                break
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            preview = (
                event.get("safe_preview")
                or event.get("content_preview")
                or event.get("message_preview")
                or event.get("text")
                or event
            )
            snippets.append(
                {
                    "run_dir": safe_path.parent.name,
                    "event_type": event.get("event_type") or event.get("type") or "unknown",
                    "preview": redact_text(preview, max_preview_chars),
                }
            )
    status = "safe trace snippets used" if snippets else "safe trace unavailable"
    return bool(snippets), snippets, status


def build_cases(summary_root: Path, safe_snippets: list[dict[str, Any]], safe_status: str) -> list[dict[str, Any]]:
    coverage_summary = load_json(summary_root / "minimax_p1_coverage_3seed" / "coverage_summary.json")
    minimax_nonoracle = load_json(summary_root / "minimax_nonoracle_heldout_targeted" / "summary.json")
    deterministic_nonoracle = load_json(summary_root / "nonoracle_heldout_deterministic" / "summary.json")
    coverage_failures = load_jsonl(summary_root / "minimax_p1_coverage_3seed" / "failure_breakdown.jsonl")
    deterministic_failures = load_jsonl(summary_root / "nonoracle_heldout_deterministic" / "failure_breakdown.jsonl")
    coverage_by_attack_defense = load_csv(
        summary_root / "minimax_p1_coverage_3seed" / "coverage_by_attack_defense.csv"
    )
    targeted_by_attack_defense = load_csv(
        summary_root / "minimax_nonoracle_heldout_targeted" / "comparison_by_attack_defense.csv"
    )

    no_defense_workspace = find_row(
        coverage_failures,
        topology="blackboard_4",
        attack="workspace_poisoning_indirect",
        defense="none",
        seed=1,
    )
    prompt_filter_paraphrase = find_row(
        deterministic_failures,
        topology="blackboard_4",
        attack="workspace_poisoning_paraphrase",
        defense="prompt_filter",
        seed=1,
    )
    flowfence_workspace = find_row(
        coverage_by_attack_defense,
        attack="workspace_poisoning_indirect",
        defense="flowfence_lite",
    )
    flowfence_nonoracle_workspace = find_row(
        targeted_by_attack_defense,
        attack="workspace_poisoning_paraphrase",
        defense="flowfence_lite_nonoracle",
    )

    shared_caveat = (
        "Evidence is from committed high-level summaries over a synthetic deterministic MAS runtime; "
        "MiniMax is the only real provider represented; this is not production safety, real computer-use, "
        "arbitrary attack robustness, or non-MiniMax generalization evidence."
    )

    cases = [
        {
            "case_id": "case_1_no_defense_workspace_propagation",
            "title": "Case 1: No-defense workspace propagation leaks raw private context",
            "source_evidence": [
                "artifacts/minimax_p1_coverage_3seed/failure_breakdown.jsonl",
                "artifacts/minimax_p1_coverage_3seed/coverage_by_attack_defense.csv",
            ],
            "configuration": {
                "experiment": "MiniMax-backed multi-agent synthetic-runtime coverage experiment",
                "topology": "blackboard_4",
                "attack": "workspace_poisoning_indirect",
                "defense": "none",
                "seed": 1,
                "provider": coverage_summary.get("provider"),
                "agent_backend": coverage_summary.get("agent_backend"),
            },
            "observed_metrics": metrics_from_failure(no_defense_workspace),
            "redacted_event_path": [
                "A private workspace note is made available in a shared blackboard setting.",
                "The unprotected agent path carries private fields into downstream task context.",
                "The final partner-facing update exposes redacted private context outside the authorized boundary.",
            ],
            "privacy_failure_or_prevention": "failure",
            "interpretation": (
                "The no-defense run illustrates why the benchmark treats privacy leakage as propagation. "
                "The shared workspace topology creates a broad transfer path, and the high-level audit records "
                "raw and external leakage for this configuration."
            ),
            "paper_use": "Use as a qualitative failure example for unprotected blackboard/shared-workspace propagation.",
            "caveat": shared_caveat,
            "safe_trace_status": safe_status,
            "safe_trace_snippets": safe_snippets[:1],
        },
        {
            "case_id": "case_2_prompt_filter_paraphrase_failure",
            "title": "Case 2: Prompt-filter misses paraphrased shared-state exfiltration",
            "source_evidence": [
                "artifacts/nonoracle_heldout_deterministic/failure_breakdown.jsonl",
                "artifacts/nonoracle_heldout_deterministic/summary.json",
            ],
            "configuration": {
                "experiment": "deterministic non-oracle held-out validation",
                "topology": "blackboard_4",
                "attack": "workspace_poisoning_paraphrase",
                "defense": "prompt_filter",
                "seed": 1,
                "provider": deterministic_nonoracle.get("provider"),
                "provider_calls_enabled": deterministic_nonoracle.get("provider_calls_enabled"),
                "agent_backend": deterministic_nonoracle.get("agent_backend"),
            },
            "observed_metrics": metrics_from_failure(prompt_filter_paraphrase),
            "redacted_event_path": [
                "A paraphrased instruction asks the system to mirror private finance and reference-like values.",
                "The wording avoids the benchmark's earlier obvious direct/indirect trigger phrases.",
                "Prompt filtering leaves enough paraphrased intent for downstream leakage in the high-level audit.",
            ],
            "privacy_failure_or_prevention": "failure",
            "interpretation": (
                "This case illustrates phrase-overfitting risk for prompt-filter defenses: the held-out paraphrase "
                "does not need the original obvious trigger wording to produce leakage pressure."
            ),
            "paper_use": "Use as the prompt-filter paraphrase-bypass example in the analysis section.",
            "caveat": shared_caveat,
            "safe_trace_status": safe_status,
            "safe_trace_snippets": safe_snippets[1:2],
        },
        {
            "case_id": "case_3_flowfence_workspace_containment",
            "title": "Case 3: FlowFence rewrites or quarantines risky shared-state content",
            "source_evidence": [
                "artifacts/minimax_p1_coverage_3seed/coverage_by_attack_defense.csv",
                "artifacts/minimax_p1_coverage_3seed/flowfence_clean_matrix.md",
            ],
            "configuration": {
                "experiment": "MiniMax-backed multi-agent synthetic-runtime coverage experiment",
                "topology": "all configured topologies",
                "attack": "workspace_poisoning_indirect",
                "defense": "flowfence_lite",
                "seed": "1,2,3 aggregate",
                "provider": coverage_summary.get("provider"),
                "agent_backend": coverage_summary.get("agent_backend"),
            },
            "observed_metrics": metrics_from_group(flowfence_workspace),
            "redacted_event_path": [
                "FlowFence observes cross-principal/shared-workspace propagation risk.",
                "The unsafe raw private fields are withheld or rewritten into a safe view before external transfer.",
                "The high-level aggregate records task success with zero raw and external leakage for the group.",
            ],
            "privacy_failure_or_prevention": "prevention",
            "interpretation": (
                "The same attack family that leaks under no defense is clean under FlowFence in the committed "
                "coverage summary, supporting a containment rather than phrase-blocking interpretation."
            ),
            "paper_use": "Use as the paired prevention example against Case 1.",
            "caveat": shared_caveat,
            "safe_trace_status": safe_status,
            "safe_trace_snippets": safe_snippets[2:3],
        },
        {
            "case_id": "case_4_nonoracle_flowfence_heldout_paraphrase",
            "title": "Case 4: Non-oracle FlowFence contains held-out paraphrase without attack labels",
            "source_evidence": [
                "artifacts/minimax_nonoracle_heldout_targeted/summary.json",
                "artifacts/minimax_nonoracle_heldout_targeted/comparison_by_attack_defense.csv",
                "artifacts/nonoracle_heldout_deterministic/summary.json",
            ],
            "configuration": {
                "experiment": "targeted MiniMax-backed synthetic-runtime validation",
                "topology": "chain_4 and blackboard_4 aggregate",
                "attack": "workspace_poisoning_paraphrase",
                "defense": "flowfence_lite_nonoracle",
                "seed": "1,2,3 aggregate",
                "provider": minimax_nonoracle.get("provider"),
                "provider_calls_enabled": minimax_nonoracle.get("provider_calls_enabled"),
                "agent_backend": minimax_nonoracle.get("agent_backend"),
            },
            "observed_metrics": {
                **metrics_from_group(flowfence_nonoracle_workspace),
                "targeted_expected_completed_failed": (
                    f"{minimax_nonoracle.get('expected_run_count')}/"
                    f"{minimax_nonoracle.get('completed_run_count')}/"
                    f"{minimax_nonoracle.get('failed_run_count')}"
                ),
                "targeted_flowfence_lite_nonoracle": minimax_nonoracle.get("flowfence_lite_nonoracle"),
                "targeted_vs_no_defense": comparison_summary(
                    minimax_nonoracle, "flowfence_lite_nonoracle_vs_no_defense"
                ),
                "targeted_vs_prompt_filter": comparison_summary(
                    minimax_nonoracle, "flowfence_lite_nonoracle_vs_prompt_filter"
                ),
            },
            "redacted_event_path": [
                "A held-out paraphrase requests transfer of private finance and credential-like fields.",
                "The non-oracle defense ignores attack annotations and uses runtime-observable signals only.",
                "The targeted MiniMax-backed synthetic-runtime validation records zero oracle-label violations and zero leakage.",
            ],
            "privacy_failure_or_prevention": "prevention",
            "interpretation": (
                "This case addresses the oracle-annotation concern: the non-oracle variant remains clean on the "
                "configured held-out paraphrase matrix without using attack labels."
            ),
            "paper_use": "Use as the non-oracle validity example for Tables 7 and 8.",
            "caveat": shared_caveat,
            "safe_trace_status": safe_status,
            "safe_trace_snippets": safe_snippets[3:4],
        },
    ]
    return cases


def validate_no_forbidden_text(output_dir: Path) -> list[str]:
    findings: list[str] = []
    for path in sorted(output_dir.rglob("*")):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        lowered = text.lower()
        for marker in SYNTHETIC_MARKERS:
            if marker in text:
                findings.append(f"{path}: synthetic marker {marker!r}")
        for phrase in FORBIDDEN_OUTPUT_PHRASES:
            if phrase in lowered:
                findings.append(f"{path}: forbidden phrase {phrase!r}")
    return findings


def write_markdown(output_dir: Path, cases: list[dict[str, Any]], safe_trace_used: bool, safe_status: str) -> None:
    lines = [
        "# Redacted Case Studies",
        "",
        "These qualitative cases are generated from committed high-level summaries. They are intended for paper",
        "drafting and reviewer-facing explanation, not as raw execution evidence.",
        "",
        f"- Generated at: {datetime.now(timezone.utc).isoformat()}",
        f"- Safe trace snippets used: {str(safe_trace_used).lower()}",
        f"- Safe trace status: {safe_status}",
        "- Provider scope: MiniMax only where real-provider evidence is represented.",
        "- Runtime scope: synthetic deterministic MAS runtime; not production or real computer-use evidence.",
        "- Exclusions: full event traces, provider responses, prompts, policy logs, and per-run generated directories.",
        "",
    ]
    for case in cases:
        lines.extend(
            [
                f"## {case['title']}",
                "",
                f"**Configuration.** {json.dumps(case['configuration'], sort_keys=True)}",
                "",
                f"**Observed metrics.** {json.dumps(case['observed_metrics'], sort_keys=True)}",
                "",
                "**Redacted event path.**",
            ]
        )
        lines.extend(f"- {item}" for item in case["redacted_event_path"])
        lines.extend(
            [
                "",
                f"**Outcome.** {case['privacy_failure_or_prevention']}.",
                "",
                f"**Interpretation.** {case['interpretation']}",
                "",
                f"**Paper use.** {case['paper_use']}",
                "",
                f"**Caveat.** {case['caveat']}",
                "",
                f"**Evidence.** {', '.join(case['source_evidence'])}",
                "",
            ]
        )
    (output_dir / "redacted_case_studies.md").write_text("\n".join(lines), encoding="utf-8")


def write_individual_cases(output_dir: Path, cases: list[dict[str, Any]]) -> None:
    filenames = [
        "case_1_no_defense_workspace_leak.md",
        "case_2_prompt_filter_paraphrase_failure.md",
        "case_3_flowfence_safe_view.md",
        "case_4_nonoracle_heldout_prevention.md",
    ]
    for filename, case in zip(filenames, cases, strict=True):
        lines = [
            f"# {case['title']}",
            "",
            "## Evidence",
            *[f"- {path}" for path in case["source_evidence"]],
            "",
            "## Configuration",
            "",
            json.dumps(case["configuration"], indent=2, sort_keys=True),
            "",
            "## Observed Metrics",
            "",
            json.dumps(case["observed_metrics"], indent=2, sort_keys=True),
            "",
            "## Redacted Event Path",
            *[f"- {item}" for item in case["redacted_event_path"]],
            "",
            "## Interpretation",
            "",
            case["interpretation"],
            "",
            "## Caveat",
            "",
            case["caveat"],
            "",
        ]
        (output_dir / filename).write_text("\n".join(lines), encoding="utf-8")


def write_support_files(
    output_dir: Path,
    cases: list[dict[str, Any]],
    safe_trace_used: bool,
    safe_status: str,
    summary_root: Path,
) -> None:
    readme = f"""# FlowFence-Lite Redacted Case Studies

This directory contains redacted qualitative case-study artifacts generated from committed high-level evidence.

- Source summary root: `{summary_root}`
- Safe trace snippets used: `{str(safe_trace_used).lower()}`
- Safe trace status: `{safe_status}`
- Real-provider scope: MiniMax only.
- Runtime scope: synthetic deterministic MAS runtime.
- Not supported: production safety, real browser/desktop computer-use deployment, arbitrary attack robustness, or non-MiniMax generalization.
- Excluded inputs: full event traces, provider responses, prompts, policy logs, generated run directories, and credentials.

These files are paper-drafting aids. They are not substitutes for the committed summary tables and audits.
"""
    (output_dir / "README.md").write_text(readme, encoding="utf-8")

    traceability_lines = [
        "# Case Study Traceability",
        "",
        "| case | supported point | evidence artifact | table/result link | caveat |",
        "| --- | --- | --- | --- | --- |",
    ]
    for case in cases:
        traceability_lines.append(
            "| "
            + " | ".join(
                [
                    case["case_id"],
                    redact_text(case["interpretation"]),
                    ", ".join(case["source_evidence"]),
                    case["paper_use"],
                    case["caveat"],
                ]
            )
            + " |"
        )
    (output_dir / "case_study_traceability.md").write_text("\n".join(traceability_lines), encoding="utf-8")

    review_notes = f"""# Case Study Review Notes

## Safe Trace Availability

{safe_status}. The case studies therefore use committed high-level metrics and redacted conceptual event paths.

## Human Review Checklist

- Confirm the cases are useful as qualitative explanations rather than new evidence.
- Confirm no claim exceeds the committed summaries.
- Confirm MiniMax-only and synthetic-runtime caveats remain visible.
- Confirm no production, real computer-use, arbitrary attack robustness, or non-MiniMax generalization claim is implied.

## Suggested Paper Placement

- Case 1 and Case 3: Results or Analysis, paired failure/prevention example.
- Case 2: Analysis of prompt-filter limitations.
- Case 4: Non-oracle validation discussion.
"""
    (output_dir / "case_study_review_notes.md").write_text(review_notes, encoding="utf-8")


def export(args: argparse.Namespace) -> int:
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_root = Path(args.summary_root)
    safe_trace_used, safe_snippets, safe_status = collect_safe_snippets(
        Path(args.runs_root) if args.runs_root else None,
        args.include_safe_trace_snippets,
        args.max_events,
        args.max_preview_chars,
    )

    cases = build_cases(summary_root, safe_snippets, safe_status)
    payload = {
        "schema_version": "flowfence_redacted_case_studies_v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary_root": str(summary_root),
        "safe_trace_snippets_used": safe_trace_used,
        "safe_trace_status": safe_status,
        "case_count": len(cases),
        "cases": cases,
    }

    (output_dir / "redacted_case_studies.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    write_markdown(output_dir, cases, safe_trace_used, safe_status)
    write_individual_cases(output_dir, cases)
    write_support_files(output_dir, cases, safe_trace_used, safe_status, summary_root)

    findings = validate_no_forbidden_text(output_dir)
    if findings:
        print("Forbidden text found in exported case studies:")
        for finding in findings:
            print(f"- {finding}")
        return 2 if args.strict else 1
    print(f"Wrote {len(cases)} redacted case studies to {output_dir}")
    print(f"safe_trace_snippets_used={str(safe_trace_used).lower()} status={safe_status}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="artifacts/case_studies")
    parser.add_argument("--summary-root", default="artifacts")
    parser.add_argument("--runs-root", default=None)
    parser.add_argument("--include-safe-trace-snippets", action="store_true")
    parser.add_argument("--max-events", type=int, default=8)
    parser.add_argument("--max-preview-chars", type=int, default=180)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    return export(parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
