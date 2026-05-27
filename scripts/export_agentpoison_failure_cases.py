#!/usr/bin/env python3
"""Export AgentPoison failure and false-positive cases from FlowFence event traces."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_OUTPUT_DIR = Path("artifacts/agentpoison_failure_cases")
DEFAULT_JSONL_NAME = "agentpoison_failure_cases.jsonl"
DEFAULT_MARKDOWN_NAME = "agentpoison_failure_cases.md"
SUMMARY_NAME = "agentpoison_failure_cases_summary.json"
FORBIDDEN_OUTPUT_KEYS = {"traj", "full_trajectory", "raw_observation", "full_observation", "prompt"}


class ExportError(RuntimeError):
    """Raised for invalid input traces."""


def boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y"}
    return bool(value)


def load_jsonl(path: Path, *, strict: bool = False) -> tuple[list[dict[str, Any]], list[str]]:
    rows: list[dict[str, Any]] = []
    warnings: list[str] = []
    if not path.exists():
        if strict:
            raise ExportError(f"Missing required JSONL file: {path}")
        return rows, [f"Missing optional JSONL file: {path}"]
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ExportError(f"Invalid JSONL in {path} line {line_number}: {exc}") from exc
            if not isinstance(row, dict):
                raise ExportError(f"Invalid JSONL in {path} line {line_number}: row is not an object")
            row["_line_number"] = line_number
            rows.append(row)
    return rows, warnings


def discover_run_dirs(run_dirs: list[Path], results_root: Path | None) -> list[Path]:
    discovered = [path.resolve() for path in run_dirs]
    if results_root:
        discovered.extend(path.parent.resolve() for path in results_root.resolve().rglob("events.full.jsonl"))
    unique = sorted({path for path in discovered if (path / "events.full.jsonl").exists()})
    return unique


def task_kind(task_type: Any) -> str:
    text = str(task_type or "").strip().lower()
    if text in {"benign", "clean", "normal"} or "benign" in text or "clean" in text:
        return "benign"
    if text in {"adv", "adversarial", "attack"} or "adv" in text or "attack" in text:
        return "adv"
    return "unknown"


def decision_of(event: dict[str, Any]) -> str | None:
    defense = event.get("defense") if isinstance(event.get("defense"), dict) else {}
    decision = defense.get("decision")
    return str(decision) if decision is not None else None


def defense_fired(event: dict[str, Any]) -> bool:
    defense = event.get("defense") if isinstance(event.get("defense"), dict) else {}
    decision = decision_of(event)
    return boolish(defense.get("defense_fired")) or decision not in (None, "", "allow")


def exposure(event: dict[str, Any], key: str) -> bool:
    exposure_obj = event.get("exposure") if isinstance(event.get("exposure"), dict) else {}
    return boolish(exposure_obj.get(key))


def has_forbidden_key(value: Any) -> bool:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in FORBIDDEN_OUTPUT_KEYS:
                return True
            if has_forbidden_key(child):
                return True
    elif isinstance(value, list):
        return any(has_forbidden_key(child) for child in value)
    return False


def truncate(value: Any, max_chars: int) -> str | None:
    if value is None:
        return None
    text = str(value).replace("\r", " ").replace("\n", "\\n")
    return text[:max_chars]


def safe_event_map(safe_events: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(event.get("event_id")): event for event in safe_events if event.get("event_id") is not None}


def first_event(events: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not events:
        return None
    return sorted(events, key=lambda event: (int(event.get("step_idx") or 0), str(event.get("event_id") or "")))[0]


def classify_adversarial_failure(events: list[dict[str, Any]]) -> str:
    exposed = [event for event in events if exposure(event, "poisoned_content_exposed")]
    detected_any = any(exposure(event, "poisoned_content_detected") for event in events)
    if exposed:
        if not detected_any:
            return "detector_miss"
        if any(decision_of(event) == "rewrite_safe_view" for event in exposed):
            return "safe_view_too_weak"
        if any(decision_of(event) in (None, "", "allow") for event in exposed):
            return "detector_miss"
        return "policy_miss"
    if any(exposure(event, "attack_manifested") for event in events):
        return "policy_miss" if detected_any else "unknown"
    return "unknown"


def make_record(
    *,
    record_type: str,
    failure_type: str,
    run_dir: Path,
    event: dict[str, Any],
    safe_event: dict[str, Any] | None,
    case_events: list[dict[str, Any]],
    max_preview_chars: int,
    notes: list[str],
) -> dict[str, Any]:
    defense = event.get("defense") if isinstance(event.get("defense"), dict) else {}
    exposure_obj = event.get("exposure") if isinstance(event.get("exposure"), dict) else {}
    safe_defense = safe_event.get("defense", {}) if isinstance(safe_event, dict) else {}
    final_output = next((item for item in case_events if item.get("event_type") == "FINAL_OUTPUT"), None)
    final_safe = safe_event if event.get("event_type") == "FINAL_OUTPUT" else None
    if final_output and safe_event is not None:
        final_safe = safe_event
    row = {
        "record_type": record_type,
        "failure_type": failure_type,
        "run_dir": str(run_dir),
        "run_id": event.get("run_id"),
        "case_id": event.get("case_id"),
        "task_type": event.get("task_type"),
        "first_event_id": event.get("event_id"),
        "first_step_idx": event.get("step_idx"),
        "event_type": event.get("event_type"),
        "channel": event.get("channel"),
        "defense_decision": defense.get("decision"),
        "risk_score": defense.get("risk_score"),
        "reason_codes": defense.get("reason_codes") or [],
        "poisoned_content_detected": exposure_obj.get("poisoned_content_detected"),
        "poisoned_content_exposed": exposure_obj.get("poisoned_content_exposed"),
        "contains_poison": event.get("contains_poison"),
        "payload_preview_redacted": truncate(
            (safe_event or event).get("payload_preview_redacted"),
            max_preview_chars,
        ),
        "rewritten_content_preview_redacted": truncate(
            safe_defense.get("rewritten_content_preview_redacted")
            if isinstance(safe_defense, dict)
            else defense.get("rewritten_content_preview_redacted"),
            max_preview_chars,
        ),
        "final_output_preview_redacted": truncate(
            (final_safe or final_output or {}).get("payload_preview_redacted"),
            max_preview_chars,
        ),
        "notes": notes,
    }
    if has_forbidden_key(row):
        raise ExportError("Exporter attempted to emit a forbidden raw-trace field")
    return row


def export_from_run(
    run_dir: Path,
    *,
    include_benign: bool,
    include_unknown_task_type: bool,
    max_preview_chars: int,
    strict: bool,
) -> tuple[list[dict[str, Any]], dict[str, Any], list[str]]:
    full_events, warnings = load_jsonl(run_dir / "events.full.jsonl", strict=True)
    safe_events, safe_warnings = load_jsonl(run_dir / "events.safe.jsonl", strict=False)
    _decisions, decision_warnings = load_jsonl(run_dir / "policy_decisions.jsonl", strict=False)
    warnings.extend(safe_warnings)
    warnings.extend(decision_warnings)
    if strict and warnings:
        raise ExportError("; ".join(warnings))
    safe_by_id = safe_event_map(safe_events)
    cases: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in full_events:
        if strict:
            missing = [key for key in ("event_id", "run_id", "case_id", "task_type", "event_type", "exposure") if key not in event]
            if missing:
                raise ExportError(f"Missing required fields in {run_dir}: {missing}")
        case_id = str(event.get("case_id") or "unknown")
        cases[case_id].append(event)

    rows: list[dict[str, Any]] = []
    task_type_counts: Counter[str] = Counter()
    decision_counts: Counter[str] = Counter()
    for case_id, events in cases.items():
        task = str(events[0].get("task_type") or "unknown")
        kind = task_kind(task)
        task_type_counts[task] += 1
        for event in events:
            if event.get("event_type") == "MEMORY_READ":
                decision_counts[decision_of(event) or "missing"] += 1

        memory_reads = [event for event in events if event.get("event_type") == "MEMORY_READ"]
        any_poison = any(boolish(event.get("contains_poison")) for event in events)
        any_detected = any(exposure(event, "poisoned_content_detected") for event in events)
        any_exposed = any(exposure(event, "poisoned_content_exposed") for event in events)
        any_attack = any(exposure(event, "attack_manifested") for event in events)
        interventions = [event for event in memory_reads if defense_fired(event)]
        is_unknown_allowed = include_unknown_task_type and kind == "unknown"

        if include_benign and (kind == "benign" or is_unknown_allowed):
            if interventions and not any_poison and not any_detected and not any_exposed:
                event = first_event(interventions) or interventions[0]
                rows.append(
                    make_record(
                        record_type="false_positive",
                        failure_type="overblocking",
                        run_dir=run_dir,
                        event=event,
                        safe_event=safe_by_id.get(str(event.get("event_id"))),
                        case_events=events,
                        max_preview_chars=max_preview_chars,
                        notes=["Benign/clean case had defense intervention without poison labels."],
                    )
                )
                continue

        if kind == "adv" or is_unknown_allowed:
            failure_events = [event for event in memory_reads if exposure(event, "poisoned_content_exposed")]
            if not failure_events and any_attack:
                failure_events = [event for event in events if exposure(event, "attack_manifested")]
            if failure_events:
                event = first_event(failure_events) or failure_events[0]
                rows.append(
                    make_record(
                        record_type="adversarial_failure",
                        failure_type=classify_adversarial_failure(events),
                        run_dir=run_dir,
                        event=event,
                        safe_event=safe_by_id.get(str(event.get("event_id"))),
                        case_events=events,
                        max_preview_chars=max_preview_chars,
                        notes=["Adversarial case had exposed poison or attack manifestation."],
                    )
                )

    run_summary = {
        "case_count": len(cases),
        "task_type_counts": dict(sorted(task_type_counts.items())),
        "defense_decision_counts": dict(sorted(decision_counts.items())),
    }
    return rows, run_summary, warnings


def summarize(rows: list[dict[str, Any]], run_summaries: list[dict[str, Any]], run_dirs: list[Path], warnings: list[str]) -> dict[str, Any]:
    failure_counts = Counter(row["failure_type"] for row in rows)
    record_counts = Counter(row["record_type"] for row in rows)
    task_type_counts: Counter[str] = Counter()
    defense_decision_counts: Counter[str] = Counter()
    case_count = 0
    for summary in run_summaries:
        case_count += int(summary.get("case_count", 0))
        task_type_counts.update(summary.get("task_type_counts", {}))
        defense_decision_counts.update(summary.get("defense_decision_counts", {}))
    return {
        "schema_version": "flowfence_agentpoison_failure_cases_v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "run_dir_count": len(run_dirs),
        "case_count": case_count,
        "exported_record_count": len(rows),
        "false_positive_count": record_counts.get("false_positive", 0),
        "adversarial_failure_count": record_counts.get("adversarial_failure", 0),
        "detector_miss_count": failure_counts.get("detector_miss", 0),
        "policy_miss_count": failure_counts.get("policy_miss", 0),
        "safe_view_too_weak_count": failure_counts.get("safe_view_too_weak", 0),
        "overblocking_count": failure_counts.get("overblocking", 0),
        "trace_incomplete_count": failure_counts.get("trace_incomplete", 0),
        "unknown_count": failure_counts.get("unknown", 0),
        "task_type_counts": dict(sorted(task_type_counts.items())),
        "defense_decision_counts": dict(sorted(defense_decision_counts.items())),
        "input_directories": [str(path) for path in run_dirs],
        "warnings": warnings,
    }


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_None._\n"
    header = "| run_id | case_id | failure_type | step | decision | preview |\n| --- | --- | --- | --- | --- | --- |\n"
    body = []
    for row in rows:
        preview = str(row.get("payload_preview_redacted") or "").replace("|", "\\|")
        body.append(
            f"| {row.get('run_id')} | {row.get('case_id')} | {row.get('failure_type')} | "
            f"{row.get('first_step_idx')} | {row.get('defense_decision')} | {preview} |"
        )
    return header + "\n".join(body) + "\n"


def write_markdown(path: Path, summary: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    false_rows = [row for row in rows if row["record_type"] == "false_positive"]
    adv_rows = [row for row in rows if row["record_type"] == "adversarial_failure"]
    lines = [
        "# AgentPoison Failure-Case Export",
        "",
        f"Generated timestamp: `{summary['generated_at']}`",
        "",
        "## Input Directories",
        "",
        *[f"- `{item}`" for item in summary["input_directories"]],
        "",
        "## Summary Counts",
        "",
        f"- run_dir_count: {summary['run_dir_count']}",
        f"- case_count: {summary['case_count']}",
        f"- exported_record_count: {summary['exported_record_count']}",
        f"- false_positive_count: {summary['false_positive_count']}",
        f"- adversarial_failure_count: {summary['adversarial_failure_count']}",
        f"- detector_miss_count: {summary['detector_miss_count']}",
        f"- policy_miss_count: {summary['policy_miss_count']}",
        f"- safe_view_too_weak_count: {summary['safe_view_too_weak_count']}",
        f"- overblocking_count: {summary['overblocking_count']}",
        f"- trace_incomplete_count: {summary['trace_incomplete_count']}",
        f"- unknown_count: {summary['unknown_count']}",
        "",
        "## False Positives",
        "",
        md_table(false_rows),
        "",
        "## Adversarial Failures",
        "",
        md_table(adv_rows),
        "",
        "## Notes and Limitations",
        "",
        "- This report is generated only from converted event traces and policy decisions.",
        "- It does not read raw trajectories or original provider logs.",
        "- Detection-success cases are intentionally not exported as failures.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export AgentPoison failure and false-positive cases from event traces.")
    parser.add_argument("--run-dir", action="append", type=Path, default=[], help="Converted run directory.")
    parser.add_argument("--results-root", type=Path, help="Root directory to scan for converted event traces.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Report output directory.")
    parser.add_argument("--include-benign", action="store_true", help="Export benign/clean false positives.")
    parser.add_argument("--include-unknown-task-type", action="store_true", help="Include unknown task_type cases.")
    parser.add_argument("--max-preview-chars", type=int, default=240, help="Maximum preview length in reports.")
    parser.add_argument("--strict", action="store_true", help="Fail on missing optional fields or warnings.")
    parser.add_argument("--jsonl-name", default=DEFAULT_JSONL_NAME, help="JSONL report filename.")
    parser.add_argument("--markdown-name", default=DEFAULT_MARKDOWN_NAME, help="Markdown report filename.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if not args.run_dir and not args.results_root:
        print("ERROR: at least one of --run-dir or --results-root is required", file=sys.stderr)
        return 2
    if args.max_preview_chars < 0:
        print("ERROR: --max-preview-chars must be non-negative", file=sys.stderr)
        return 2
    run_dirs = discover_run_dirs(args.run_dir, args.results_root)
    if not run_dirs:
        print("ERROR: no converted run directories containing events.full.jsonl were found", file=sys.stderr)
        return 2

    rows: list[dict[str, Any]] = []
    run_summaries: list[dict[str, Any]] = []
    warnings: list[str] = []
    try:
        for run_dir in run_dirs:
            run_rows, run_summary, run_warnings = export_from_run(
                run_dir,
                include_benign=args.include_benign,
                include_unknown_task_type=args.include_unknown_task_type,
                max_preview_chars=args.max_preview_chars,
                strict=args.strict,
            )
            rows.extend(run_rows)
            run_summaries.append(run_summary)
            warnings.extend(run_warnings)
    except ExportError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    rows.sort(
        key=lambda row: (
            str(row.get("run_dir") or ""),
            str(row.get("run_id") or ""),
            str(row.get("case_id") or ""),
            int(row.get("first_step_idx") or 0),
            str(row.get("first_event_id") or ""),
        )
    )
    summary = summarize(rows, run_summaries, run_dirs, warnings)
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(output_dir / args.jsonl_name, rows)
    write_markdown(output_dir / args.markdown_name, summary, rows)
    (output_dir / SUMMARY_NAME).write_text(json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    print(f"Wrote {len(rows)} failure/false-positive records to {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
