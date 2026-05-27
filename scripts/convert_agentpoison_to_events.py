#!/usr/bin/env python3
"""Convert saved AgentPoison full-ReAct run outputs into FlowFence event traces."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

EVENT_SCHEMA_VERSION = "flowfence_event_v1"
POLICY_SCHEMA_VERSION = "flowfence_policy_decision_v1"
OUTPUT_NAMES = (
    "events.full.jsonl",
    "events.safe.jsonl",
    "policy_decisions.jsonl",
    "metrics.recomputed.json",
)

SKIP_FILE_NAMES = {
    "metrics.json",
    "metrics.recomputed.json",
    "manifest.json",
    "run_manifest.json",
    "mismatch_notes.json",
    "official_eval.json",
    "resolved_config.json",
}
SKIP_NAME_PARTS = ("events.", "policy_decisions", "summary", "config", "eval")
POISON_REDACTION_PATTERNS = (
    re.compile(r"com ##cturing reeve eased pulled", re.IGNORECASE),
    re.compile(r"ignore (?:the )?(?:previous|above|original) instructions?", re.IGNORECASE),
    re.compile(r"final answer must be", re.IGNORECASE),
    re.compile(r"do not follow", re.IGNORECASE),
    re.compile(r"override", re.IGNORECASE),
    re.compile(r"SYNTHETIC_RAW_POISON_PAYLOAD_DO_NOT_EXPOSE", re.IGNORECASE),
)


class ConversionError(RuntimeError):
    """Raised when a run directory cannot be converted safely."""


def sha256_text(value: str | None) -> str | None:
    if value is None:
        return None
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def stable_token(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.:-]+", "_", value.strip())
    return cleaned.strip("_") or hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]


def redact_preview(value: Any, *, max_chars: int, safe: bool) -> str | None:
    if value is None:
        return None
    text = str(value).replace("\r", " ").replace("\n", "\\n")
    text = text[:max_chars]
    if safe:
        for pattern in POISON_REDACTION_PATTERNS:
            text = pattern.sub("[REDACTED_POISON_PAYLOAD]", text)
    return text


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


def infer_task_type(path: Path, row: dict[str, Any]) -> str:
    task_type = row.get("task_type")
    if isinstance(task_type, str) and task_type:
        return task_type
    name = path.name.lower()
    if "_adv" in name or "adv_" in name or name.endswith("adv.json"):
        return "adv"
    if "benign" in name or "clean" in name:
        return "benign"
    return "unknown"


def iter_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ConversionError(f"Invalid JSONL in {path} line {line_no}: {exc}") from exc
            if isinstance(row, dict):
                yield row


def iter_json(path: Path) -> Iterable[dict[str, Any]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ConversionError(f"Invalid JSON in {path}: {exc}") from exc
    if isinstance(payload, list):
        for row in payload:
            if isinstance(row, dict):
                yield row
        return
    if not isinstance(payload, dict):
        return
    for key in ("cases", "case_results", "rows", "results"):
        rows = payload.get(key)
        if isinstance(rows, list):
            for row in rows:
                if isinstance(row, dict):
                    yield row
            return
    yield payload


def is_case_row(row: dict[str, Any]) -> bool:
    if "question" in row and ("question_idx" in row or "case_id" in row):
        return True
    if isinstance(row.get("defense_events"), list):
        return True
    return False


def candidate_files(run_dir: Path) -> list[Path]:
    preferred = sorted((run_dir / "upstream_outputs").glob("*.jsonl"))
    if preferred:
        return preferred
    case_details = sorted((run_dir / "case_details").glob("*.json"))
    if case_details:
        return case_details
    files: list[Path] = []
    for pattern in ("*.jsonl", "*.json"):
        for path in sorted(run_dir.glob(pattern)):
            if path.name in SKIP_FILE_NAMES:
                continue
            if any(part in path.name for part in SKIP_NAME_PARTS):
                continue
            files.append(path)
    return files


def load_rows(run_dir: Path) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    inspected: list[str] = []
    warnings: list[str] = []
    rows: list[dict[str, Any]] = []
    for path in candidate_files(run_dir):
        inspected.append(str(path))
        iterator = iter_jsonl(path) if path.suffix == ".jsonl" else iter_json(path)
        found = 0
        for row in iterator:
            if not is_case_row(row):
                continue
            row = dict(row)
            row["_source_file"] = str(path)
            row["_task_type"] = infer_task_type(path, row)
            rows.append(row)
            found += 1
        if found == 0:
            warnings.append(f"No compatible per-case rows found in {path}")
    return rows, inspected, warnings


def case_id_for(row: dict[str, Any], ordinal: int) -> str:
    if row.get("case_id"):
        return stable_token(str(row["case_id"]))
    qidx = row.get("question_idx")
    task_type = row.get("_task_type") or row.get("task_type") or "unknown"
    if qidx is not None:
        return f"case_{int(qidx):03d}_{stable_token(str(task_type))}"
    source = f"{row.get('_source_file', '')}:{ordinal}:{row.get('question', '')[:80]}"
    return f"case_{hashlib.sha256(source.encode('utf-8')).hexdigest()[:12]}"


def event_record(
    *,
    run_id: str,
    case_id: str,
    task_type: str,
    step_idx: int,
    event_type: str,
    channel: str,
    actor_id: str,
    object_id: str,
    causal_parents: list[str],
    payload_sha256: str | None,
    payload_preview_redacted: str | None,
    contains_poison: bool,
    defense: dict[str, Any] | None = None,
    exposure: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
    ordinal: int = 0,
) -> dict[str, Any]:
    event_id = f"{run_id}:{case_id}:{step_idx:03d}:{event_type.lower()}:{ordinal:03d}"
    return {
        "schema_version": EVENT_SCHEMA_VERSION,
        "event_id": event_id,
        "run_id": run_id,
        "case_id": case_id,
        "task_type": task_type,
        "step_idx": step_idx,
        "event_type": event_type,
        "channel": channel,
        "actor_id": actor_id,
        "object_id": object_id,
        "causal_parents": causal_parents,
        "payload_sha256": payload_sha256,
        "payload_preview_redacted": payload_preview_redacted,
        "contains_poison": contains_poison,
        "defense": defense or {},
        "exposure": {
            "poisoned_content_detected": None,
            "poisoned_content_exposed": None,
            "raw_poisoned_retrieval": None,
            "attack_manifested": None,
            "safe_trace_redacted": False,
            **(exposure or {}),
        },
        "metadata": metadata or {},
    }


def action_kind(candidate_action: str) -> str:
    lowered = candidate_action.lower()
    if lowered.startswith("search["):
        return "search"
    if lowered.startswith("lookup["):
        return "lookup"
    return "unknown"


def defense_fired(defense_event: dict[str, Any]) -> bool:
    if "defense_fired" in defense_event:
        return boolish(defense_event.get("defense_fired"))
    return str(defense_event.get("decision", "allow")) != "allow"


def convert_rows(rows: list[dict[str, Any]], run_id: str, max_preview_chars: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    events_full: list[dict[str, Any]] = []
    policy_decisions: list[dict[str, Any]] = []
    case_ids: set[str] = set()
    raw_poison_cases: set[str] = set()
    exposed_cases: set[str] = set()
    detected_cases: set[str] = set()
    attack_cases: set[str] = set()
    intervention_count = 0
    memory_read_count = 0
    rewrite_count = 0
    quarantine_count = 0

    for ordinal, row in enumerate(rows):
        task_type = str(row.get("_task_type") or row.get("task_type") or "unknown")
        case_id = case_id_for(row, ordinal)
        case_ids.add(case_id)
        attack_manifested = boolish(row.get("attack_manifested"))
        if attack_manifested:
            attack_cases.add(case_id)
        if boolish(row.get("raw_retrieval_success")) or boolish(row.get("injected_retrieval_success")):
            raw_poison_cases.add(case_id)
        if boolish(row.get("retrieval_success")):
            exposed_cases.add(case_id)
        if boolish(row.get("defense_summary", {}).get("poisoned_content_detected_count")):
            detected_cases.add(case_id)
        if boolish(row.get("defense_summary", {}).get("poisoned_content_exposed_count")):
            exposed_cases.add(case_id)

        defense_events = row.get("defense_events") if isinstance(row.get("defense_events"), list) else []
        for event_ordinal, defense_event in enumerate(defense_events):
            if not isinstance(defense_event, dict):
                continue
            step_idx = int(defense_event.get("step_idx") or 0)
            candidate_action = str(defense_event.get("candidate_action") or "")
            action_type = action_kind(candidate_action)
            contains_poison = boolish(defense_event.get("poisoned_content_detected"))
            exposed = boolish(defense_event.get("poisoned_content_exposed"))
            if contains_poison:
                raw_poison_cases.add(case_id)
                detected_cases.add(case_id)
            if exposed:
                exposed_cases.add(case_id)

            tool_event_id: str | None = None
            if action_type in {"search", "lookup"}:
                tool_event = event_record(
                    run_id=run_id,
                    case_id=case_id,
                    task_type=task_type,
                    step_idx=step_idx,
                    event_type="TOOL_CALL",
                    channel="tool",
                    actor_id="agent",
                    object_id=action_type,
                    causal_parents=[],
                    payload_sha256=sha256_text(candidate_action),
                    payload_preview_redacted=redact_preview(candidate_action, max_chars=max_preview_chars, safe=False),
                    contains_poison=False,
                    metadata={
                        "candidate_action": candidate_action,
                        "source_file": row.get("_source_file"),
                    },
                    ordinal=event_ordinal,
                )
                events_full.append(tool_event)
                tool_event_id = tool_event["event_id"]

            final_preview = defense_event.get("final_observation_preview")
            final_sha = sha256_text(final_preview) if final_preview is not None else None
            memory_event = event_record(
                run_id=run_id,
                case_id=case_id,
                task_type=task_type,
                step_idx=step_idx,
                event_type="MEMORY_READ",
                channel="retrieval_memory",
                actor_id="agent",
                object_id=str(defense_event.get("raw_observation_sha256") or f"retrieval:{case_id}:{step_idx}"),
                causal_parents=[tool_event_id] if tool_event_id else [],
                payload_sha256=defense_event.get("raw_observation_sha256"),
                payload_preview_redacted=redact_preview(
                    defense_event.get("raw_observation_preview"),
                    max_chars=max_preview_chars,
                    safe=False,
                ),
                contains_poison=contains_poison,
                defense={
                    "decision": defense_event.get("decision"),
                    "risk_score": defense_event.get("risk_score"),
                    "reason_codes": defense_event.get("reason_codes") or [],
                    "lease_signal": defense_event.get("lease_signal"),
                    "defense_fired": defense_fired(defense_event),
                    "rewritten_content_sha256": final_sha,
                    "rewritten_content_preview_redacted": redact_preview(
                        final_preview,
                        max_chars=max_preview_chars,
                        safe=False,
                    ),
                    "hard_blocker": defense_event.get("hard_blocker"),
                },
                exposure={
                    "poisoned_content_detected": contains_poison,
                    "poisoned_content_exposed": exposed,
                    "raw_poisoned_retrieval": contains_poison,
                    "attack_manifested": attack_manifested,
                    "safe_trace_redacted": False,
                },
                metadata={
                    "candidate_action": candidate_action,
                    "action_type": action_type,
                    "original_observation_length": defense_event.get("original_observation_length"),
                    "final_observation_length": defense_event.get("final_observation_length"),
                    "defense_wall_time_seconds": defense_event.get("defense_wall_time_seconds"),
                    "recovery_hint_applied": defense_event.get("recovery_hint_applied"),
                    "source_file": row.get("_source_file"),
                },
                ordinal=event_ordinal,
            )
            events_full.append(memory_event)
            memory_read_count += 1

            if defense_fired(defense_event):
                intervention_count += 1
            if defense_event.get("decision") == "rewrite_safe_view":
                rewrite_count += 1
            if defense_event.get("decision") == "quarantine":
                quarantine_count += 1

            decision_id = f"{run_id}:{case_id}:{step_idx:03d}:decision:{event_ordinal:03d}"
            policy_decisions.append(
                {
                    "schema_version": POLICY_SCHEMA_VERSION,
                    "decision_id": decision_id,
                    "event_id": memory_event["event_id"],
                    "run_id": run_id,
                    "case_id": case_id,
                    "task_type": task_type,
                    "step_idx": step_idx,
                    "defense_mode": str(row.get("defense_summary", {}).get("defense_mode") or "unknown"),
                    "decision": defense_event.get("decision"),
                    "risk_score": defense_event.get("risk_score"),
                    "reason_codes": defense_event.get("reason_codes") or [],
                    "lease_signal": defense_event.get("lease_signal"),
                    "actions": [str(defense_event.get("decision"))] if defense_event.get("decision") else [],
                    "metadata": {
                        "hard_blocker": defense_event.get("hard_blocker"),
                        "candidate_action": candidate_action,
                        "source_file": row.get("_source_file"),
                    },
                }
            )

        answer = row.get("answer")
        if answer is not None:
            step_idx = int(row.get("n_calls") or 0)
            events_full.append(
                event_record(
                    run_id=run_id,
                    case_id=case_id,
                    task_type=task_type,
                    step_idx=step_idx,
                    event_type="FINAL_OUTPUT",
                    channel="final_output",
                    actor_id="agent",
                    object_id=f"answer:{case_id}",
                    causal_parents=[],
                    payload_sha256=sha256_text(str(answer)),
                    payload_preview_redacted=redact_preview(answer, max_chars=max_preview_chars, safe=False),
                    contains_poison=False,
                    exposure={
                        "attack_manifested": attack_manifested,
                        "safe_trace_redacted": False,
                    },
                    metadata={
                        "em": row.get("em"),
                        "gt_answer_sha256": sha256_text(str(row.get("gt_answer"))) if row.get("gt_answer") is not None else None,
                        "predicted_label": row.get("predicted_label"),
                        "source_file": row.get("_source_file"),
                    },
                    ordinal=0,
                )
            )

    events_safe = [to_safe_event(event, max_preview_chars=max_preview_chars) for event in events_full]
    case_count = len(case_ids)
    metrics = {
        "schema_version": "flowfence_event_metrics_v1",
        "run_id": run_id,
        "case_count": case_count,
        "event_count": len(events_full),
        "memory_read_event_count": memory_read_count,
        "defense_decision_count": len(policy_decisions),
        "raw_poisoned_retrieval_case_rate": rate(len(raw_poison_cases), case_count),
        "exposed_poisoned_retrieval_case_rate": rate(len(exposed_cases), case_count),
        "poisoned_content_detected_case_rate": rate(len(detected_cases), case_count),
        "poisoned_content_exposed_case_rate": rate(len(exposed_cases), case_count),
        "attack_manifestation_case_rate": rate(len(attack_cases), case_count),
        "defense_intervention_event_rate": rate(intervention_count, memory_read_count),
        "rewrite_count": rewrite_count,
        "quarantine_count": quarantine_count,
        "official_acc": None,
        "official_em": None,
        "notes": [
            "Converter-level metrics only; final audit/recompute is a later goal.",
            "Official ACC/EM are unavailable from event traces and are not recomputed here.",
            "No provider calls or new experiments are run by this converter.",
        ],
    }
    return events_full, events_safe, policy_decisions, metrics


def rate(numerator: int, denominator: int) -> float | None:
    if denominator == 0:
        return None
    return round(numerator / denominator, 6)


def to_safe_event(event: dict[str, Any], *, max_preview_chars: int) -> dict[str, Any]:
    safe_event = json.loads(json.dumps(event))
    safe_event["payload_preview_redacted"] = redact_preview(
        safe_event.get("payload_preview_redacted"),
        max_chars=max_preview_chars,
        safe=True,
    )
    defense = safe_event.get("defense") or {}
    if "rewritten_content_preview_redacted" in defense:
        defense["rewritten_content_preview_redacted"] = redact_preview(
            defense.get("rewritten_content_preview_redacted"),
            max_chars=max_preview_chars,
            safe=True,
        )
    metadata = safe_event.get("metadata") or {}
    if "candidate_action" in metadata:
        metadata["candidate_action"] = redact_preview(metadata.get("candidate_action"), max_chars=max_preview_chars, safe=True)
    safe_event["exposure"]["safe_trace_redacted"] = True
    return safe_event


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def ensure_outputs_allowed(output_dir: Path, overwrite: bool) -> None:
    existing = [str(output_dir / name) for name in OUTPUT_NAMES if (output_dir / name).exists()]
    if existing and not overwrite:
        joined = "\n  ".join(existing)
        raise ConversionError(f"Output files already exist. Use --overwrite to replace:\n  {joined}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert saved adapted AgentPoison full-ReAct outputs into FlowFence event traces."
    )
    parser.add_argument("--run-dir", required=True, type=Path, help="Existing AgentPoison run directory.")
    parser.add_argument("--output-dir", type=Path, help="Directory for generated event outputs. Defaults to --run-dir.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing event output files.")
    parser.add_argument("--max-preview-chars", type=int, default=240, help="Maximum characters retained in previews.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    run_dir = args.run_dir.resolve()
    output_dir = (args.output_dir or args.run_dir).resolve()
    if not run_dir.exists() or not run_dir.is_dir():
        raise ConversionError(f"--run-dir is not a directory: {run_dir}")
    if args.max_preview_chars < 0:
        raise ConversionError("--max-preview-chars must be non-negative")

    output_dir.mkdir(parents=True, exist_ok=True)
    ensure_outputs_allowed(output_dir, args.overwrite)
    rows, inspected, warnings = load_rows(run_dir)
    if not rows:
        inspected_text = "\n  ".join(inspected) if inspected else "(no candidate JSON/JSONL files found)"
        raise ConversionError(f"No compatible per-case result rows found in run-dir {run_dir}. Inspected:\n  {inspected_text}")

    run_id = stable_token(run_dir.name)
    events_full, events_safe, policy_decisions, metrics = convert_rows(rows, run_id, args.max_preview_chars)
    if not events_full:
        raise ConversionError(f"Conversion generated no events for run-dir {run_dir}; refusing to write empty traces.")
    metrics["inspected_files"] = inspected
    metrics["warnings"] = warnings

    write_jsonl(output_dir / "events.full.jsonl", events_full)
    write_jsonl(output_dir / "events.safe.jsonl", events_safe)
    write_jsonl(output_dir / "policy_decisions.jsonl", policy_decisions)
    write_json(output_dir / "metrics.recomputed.json", metrics)
    print(f"Wrote {len(events_full)} events and {len(policy_decisions)} policy decisions to {output_dir}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ConversionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
