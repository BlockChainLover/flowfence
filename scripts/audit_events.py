#!/usr/bin/env python3
"""Audit FlowFence event traces generated from saved AgentPoison runs."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

REQUIRED_FILES = ("events.full.jsonl", "events.safe.jsonl", "policy_decisions.jsonl")
REQUIRED_EVENT_FIELDS = {
    "schema_version",
    "event_id",
    "run_id",
    "case_id",
    "task_type",
    "step_idx",
    "event_type",
    "channel",
    "actor_id",
    "object_id",
    "causal_parents",
    "payload_sha256",
    "payload_preview_redacted",
    "contains_poison",
    "defense",
    "exposure",
    "metadata",
}
REQUIRED_MEMORY_DEFENSE_FIELDS = {"decision", "risk_score", "reason_codes"}
REQUIRED_EXPOSURE_FIELDS = {"poisoned_content_detected", "poisoned_content_exposed"}
FORBIDDEN_SAFE_FIELD_NAMES = {"raw_observation", "full_observation", "full_trajectory", "traj"}


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


def load_jsonl(path: Path, failures: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError as exc:
                    failures.append(
                        failure(
                            "jsonl_parseability",
                            path,
                            line_number=line_number,
                            details=f"JSON parse error: {exc}",
                        )
                    )
                    continue
                if not isinstance(row, dict):
                    failures.append(
                        failure("jsonl_parseability", path, line_number=line_number, details="Row is not an object")
                    )
                    continue
                row["_line_number"] = line_number
                rows.append(row)
    except OSError as exc:
        failures.append(failure("jsonl_parseability", path, details=f"Could not read file: {exc}"))
    return rows


def failure(
    check_name: str,
    filename: Path | str,
    *,
    line_number: int | None = None,
    run_id: str | None = None,
    case_id: str | None = None,
    event_id: str | None = None,
    details: str,
) -> dict[str, Any]:
    return {
        "check_name": check_name,
        "filename": str(filename),
        "line_number": line_number,
        "run_id": run_id,
        "case_id": case_id,
        "event_id": event_id,
        "details": details,
    }


def nested_has_forbidden_key(value: Any) -> str | None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in FORBIDDEN_SAFE_FIELD_NAMES:
                return key
            found = nested_has_forbidden_key(child)
            if found:
                return found
    elif isinstance(value, list):
        for child in value:
            found = nested_has_forbidden_key(child)
            if found:
                return found
    return None


def audit(run_dir: Path, *, trigger_string: str | None, strict: bool, max_safe_preview_chars: int = 500) -> dict[str, Any]:
    failures: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    paths = {name: run_dir / name for name in REQUIRED_FILES}

    for name, path in paths.items():
        if not path.exists():
            failures.append(failure("required_files_exist", path, details=f"Missing required file {name}"))

    full_events = load_jsonl(paths["events.full.jsonl"], failures) if paths["events.full.jsonl"].exists() else []
    safe_events = load_jsonl(paths["events.safe.jsonl"], failures) if paths["events.safe.jsonl"].exists() else []
    decisions = load_jsonl(paths["policy_decisions.jsonl"], failures) if paths["policy_decisions.jsonl"].exists() else []

    full_ids: set[str] = set()
    safe_ids: set[str] = set()
    memory_read_ids: set[str] = set()
    defended_memory_read_ids: set[str] = set()
    for path_name, events, id_set in (
        ("events.full.jsonl", full_events, full_ids),
        ("events.safe.jsonl", safe_events, safe_ids),
    ):
        path = paths[path_name]
        case_steps: dict[str, list[tuple[int, str, int, str]]] = defaultdict(list)
        for row in events:
            line_number = row.get("_line_number")
            event_id = row.get("event_id")
            missing = sorted(REQUIRED_EVENT_FIELDS - set(row))
            if missing:
                failures.append(
                    failure(
                        "required_event_fields",
                        path,
                        line_number=line_number,
                        run_id=row.get("run_id"),
                        case_id=row.get("case_id"),
                        event_id=event_id,
                        details=f"Missing fields: {', '.join(missing)}",
                    )
                )
            if event_id in id_set:
                failures.append(
                    failure(
                        "event_id_uniqueness",
                        path,
                        line_number=line_number,
                        run_id=row.get("run_id"),
                        case_id=row.get("case_id"),
                        event_id=event_id,
                        details="Duplicate event_id",
                    )
                )
            if event_id:
                id_set.add(str(event_id))

            exposure = row.get("exposure")
            if not isinstance(exposure, dict):
                failures.append(
                    failure(
                        "required_exposure_fields",
                        path,
                        line_number=line_number,
                        run_id=row.get("run_id"),
                        case_id=row.get("case_id"),
                        event_id=event_id,
                        details="exposure is missing or not an object",
                    )
                )
            else:
                missing_exposure = sorted(REQUIRED_EXPOSURE_FIELDS - set(exposure))
                if missing_exposure:
                    failures.append(
                        failure(
                            "required_exposure_fields",
                            path,
                            line_number=line_number,
                            run_id=row.get("run_id"),
                            case_id=row.get("case_id"),
                            event_id=event_id,
                            details=f"Missing exposure fields: {', '.join(missing_exposure)}",
                        )
                    )
                if boolish(exposure.get("poisoned_content_exposed")) and not (
                    boolish(row.get("contains_poison")) or boolish(exposure.get("poisoned_content_detected"))
                ):
                    failures.append(
                        failure(
                            "exposed_poison_traceability",
                            path,
                            line_number=line_number,
                            run_id=row.get("run_id"),
                            case_id=row.get("case_id"),
                            event_id=event_id,
                            details="poisoned_content_exposed=true without contains_poison or detected flag",
                        )
                    )

            try:
                step_idx = int(row.get("step_idx", -1))
            except (TypeError, ValueError):
                step_idx = -1
            if step_idx < 0:
                failures.append(
                    failure(
                        "step_ordering",
                        path,
                        line_number=line_number,
                        run_id=row.get("run_id"),
                        case_id=row.get("case_id"),
                        event_id=event_id,
                        details="step_idx is negative or invalid",
                    )
                )
            if row.get("case_id") is not None:
                case_steps[str(row.get("case_id"))].append(
                    (step_idx, str(event_id), int(line_number or 0), str(row.get("event_type") or ""))
                )

            if row.get("event_type") == "MEMORY_READ":
                if path_name == "events.full.jsonl" and event_id:
                    memory_read_ids.add(str(event_id))
                defense = row.get("defense")
                if not isinstance(defense, dict):
                    failures.append(
                        failure(
                            "memory_read_defense_fields",
                            path,
                            line_number=line_number,
                            run_id=row.get("run_id"),
                            case_id=row.get("case_id"),
                            event_id=event_id,
                            details="defense is missing or not an object",
                        )
                    )
                else:
                    missing_defense = sorted(REQUIRED_MEMORY_DEFENSE_FIELDS - set(defense))
                    if missing_defense:
                        failures.append(
                            failure(
                                "memory_read_defense_fields",
                                path,
                                line_number=line_number,
                                run_id=row.get("run_id"),
                                case_id=row.get("case_id"),
                                event_id=event_id,
                                details=f"Missing defense fields: {', '.join(missing_defense)}",
                            )
                        )
                    decision = defense.get("decision")
                    if path_name == "events.full.jsonl" and event_id and decision not in (None, "", "allow"):
                        defended_memory_read_ids.add(str(event_id))
                    if path_name == "events.full.jsonl" and event_id and boolish(defense.get("defense_fired")):
                        defended_memory_read_ids.add(str(event_id))

        for case_id, steps in case_steps.items():
            previous = -1
            for step_idx, event_id, line_number, event_type in steps:
                effective_step = previous if event_type == "FINAL_OUTPUT" and step_idx == 0 and previous >= 0 else step_idx
                if effective_step < previous:
                    failures.append(
                        failure(
                            "step_ordering",
                            path,
                            line_number=line_number,
                            case_id=case_id,
                            event_id=event_id,
                            details="Events are not ordered non-decreasing by step_idx within case_id",
                        )
                    )
                previous = max(previous, step_idx)
                previous = max(previous, effective_step)

    decision_event_ids: set[str] = set()
    for row in decisions:
        event_id = row.get("event_id")
        if not event_id:
            failures.append(
                failure(
                    "policy_decision_alignment",
                    paths["policy_decisions.jsonl"],
                    line_number=row.get("_line_number"),
                    run_id=row.get("run_id"),
                    case_id=row.get("case_id"),
                    details="Policy decision missing event_id",
                )
            )
            continue
        decision_event_ids.add(str(event_id))
        if str(event_id) not in full_ids:
            failures.append(
                failure(
                    "policy_decision_alignment",
                    paths["policy_decisions.jsonl"],
                    line_number=row.get("_line_number"),
                    run_id=row.get("run_id"),
                    case_id=row.get("case_id"),
                    event_id=str(event_id),
                    details="Policy decision event_id not found in events.full.jsonl",
                )
            )
    missing_decisions = sorted(defended_memory_read_ids - decision_event_ids)
    for event_id in missing_decisions:
        failures.append(
            failure(
                "policy_decision_alignment",
                paths["events.full.jsonl"],
                event_id=event_id,
                details="Defended MEMORY_READ event has no corresponding policy decision",
            )
        )

    for row in safe_events:
        line_number = row.get("_line_number")
        forbidden_key = nested_has_forbidden_key(row)
        if forbidden_key:
            failures.append(
                failure(
                    "safe_trace_hygiene",
                    paths["events.safe.jsonl"],
                    line_number=line_number,
                    run_id=row.get("run_id"),
                    case_id=row.get("case_id"),
                    event_id=row.get("event_id"),
                    details=f"Safe event contains forbidden field name: {forbidden_key}",
                )
            )
        serialized = json.dumps(row, ensure_ascii=False)
        if trigger_string and trigger_string in serialized:
            failures.append(
                failure(
                    "safe_trace_hygiene",
                    paths["events.safe.jsonl"],
                    line_number=line_number,
                    run_id=row.get("run_id"),
                    case_id=row.get("case_id"),
                    event_id=row.get("event_id"),
                    details="Safe event contains trigger string",
                )
            )
        preview = row.get("payload_preview_redacted")
        if isinstance(preview, str) and len(preview) > max_safe_preview_chars:
            failures.append(
                failure(
                    "safe_trace_hygiene",
                    paths["events.safe.jsonl"],
                    line_number=line_number,
                    run_id=row.get("run_id"),
                    case_id=row.get("case_id"),
                    event_id=row.get("event_id"),
                    details=f"Safe payload preview exceeds {max_safe_preview_chars} chars",
                )
            )

    if len(full_events) != len(safe_events):
        failures.append(
            failure(
                "full_vs_safe_event_count",
                run_dir,
                details=f"full={len(full_events)} safe={len(safe_events)}",
            )
        )
    if full_events and not any(row.get("event_type") == "MEMORY_READ" for row in full_events):
        warnings.append(failure("event_type_sanity", paths["events.full.jsonl"], details="No MEMORY_READ event found"))
    if full_events and not any(row.get("event_type") == "FINAL_OUTPUT" for row in full_events):
        warnings.append(failure("event_type_sanity", paths["events.full.jsonl"], details="No FINAL_OUTPUT event found"))

    if strict and warnings:
        failures.extend(warnings)
        warnings = []

    return {
        "schema_version": "flowfence_event_audit_v1",
        "run_dir": str(run_dir),
        "status": "pass" if not failures else "fail",
        "event_count": len(full_events),
        "safe_event_count": len(safe_events),
        "policy_decision_count": len(decisions),
        "failure_count": len(failures),
        "warning_count": len(warnings),
        "failures": failures,
        "warnings": warnings,
    }


def print_report(report: dict[str, Any]) -> None:
    if report["status"] == "pass":
        print("AUDIT PASS")
    else:
        print("AUDIT FAIL")
    rows = report["failures"] or report["warnings"]
    if rows:
        print("check_name\tfilename\tline_number\trun_id\tcase_id\tevent_id\tdetails")
        for row in rows:
            print(
                "\t".join(
                    str(row.get(key) if row.get(key) is not None else "")
                    for key in ("check_name", "filename", "line_number", "run_id", "case_id", "event_id", "details")
                )
            )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit FlowFence event JSONL traces.")
    parser.add_argument("--run-dir", required=True, type=Path, help="Directory containing event JSONL outputs.")
    parser.add_argument("--trigger-string", help="Optional raw poison trigger string forbidden in safe traces.")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures.")
    parser.add_argument("--json-output", type=Path, help="Optional path for machine-readable audit report.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    report = audit(args.run_dir.resolve(), trigger_string=args.trigger_string, strict=args.strict)
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print_report(report)
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
