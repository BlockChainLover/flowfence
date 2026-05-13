from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


DEFAULT_CANDIDATES = {
    "nodefense_attack": [
        "icde_paraphrase_direct_instruction_no_defense_v1",
        "baseline_agentpoison_fullreact_dpr_strategyqa_minimax27_triggerquery_v1",
    ],
    "flowfence_containment": [
        "icde_paraphrase_direct_instruction_flowfence_lite_v1",
        "method_flowfence_lite_fullreact_minimax27_triggerquery_quarantine_actioncanon_v1",
    ],
    "static_filter_comparator": [
        "icde_paraphrase_direct_instruction_static_keyword_filter_v1",
        "baseline_agentpoison_fullreact_minimax27_triggerquery_heldout_instruction_static_keyword_filter_v2",
    ],
}


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _case_paths(results_root: Path, run_name: str) -> list[Path]:
    return sorted((results_root / run_name / "case_details").glob("case_*_adv.json"))


def _find_case(results_root: Path, run_names: list[str], mode: str) -> tuple[str, Path, dict[str, Any]] | None:
    for run_name in run_names:
        run_dir = results_root / run_name
        if not run_dir.exists():
            continue
        for path in _case_paths(results_root, run_name):
            case = _load_json(path)
            raw = int(case.get("raw_retrieval_success", 0)) > 0
            exposed = int(case.get("retrieval_success", 0)) > 0
            manifested = bool(case.get("attack_manifested", False))
            has_quarantine = any(event.get("decision") == "quarantine" for event in case.get("defense_events", []))
            if mode == "nodefense_attack" and raw and exposed and manifested:
                return run_name, path, case
            if mode == "flowfence_containment" and raw and not exposed and not manifested and has_quarantine:
                return run_name, path, case
            if mode == "static_filter_comparator" and raw and (exposed or manifested or not has_quarantine):
                return run_name, path, case
    return None


def _visible_context(case: dict[str, Any]) -> str:
    traj = str(case.get("traj", ""))
    return traj[-2000:]


def _record_from_case(case_type: str, run_name: str, path: Path, case: dict[str, Any]) -> dict[str, Any]:
    defense_events = case.get("defense_events", [])
    retrieved_records = []
    for event_idx, event in enumerate(defense_events):
        raw_preview = str(event.get("raw_observation_preview", ""))
        retrieved_records.append(
            {
                "event_idx": event_idx,
                "record_id": case.get("last_retrieved_record_id"),
                "content_sha256": event.get("raw_observation_sha256")
                or hashlib.sha256(raw_preview.encode("utf-8")).hexdigest(),
                "source": "AgentPoison StrategyQA DPR local_wikienv",
                "retrieval_score": None,
                "poisoned_label": bool(event.get("poisoned_content_detected", False)),
                "raw_preview": raw_preview,
            }
        )
    if not retrieved_records and str(case.get("traj", "")):
        retrieved_records.append(
            {
                "event_idx": 0,
                "record_id": case.get("last_retrieved_record_id"),
                "content_sha256": hashlib.sha256(str(case.get("traj", "")).encode("utf-8")).hexdigest(),
                "source": "AgentPoison StrategyQA DPR local_wikienv",
                "retrieval_score": None,
                "poisoned_label": bool(case.get("raw_retrieval_success", 0)),
                "raw_preview": "No defense-events recorded; retrieved content is visible in the ReAct trajectory.",
            }
        )

    decisions = [
        {
            "step_idx": event.get("step_idx"),
            "decision": event.get("decision"),
            "reason_codes": event.get("reason_codes", []),
            "lease_signal": event.get("lease_signal"),
            "unsafe_crossed_boundary": bool(event.get("poisoned_content_exposed", False)),
            "model_visible_preview": event.get("final_observation_preview"),
        }
        for event in defense_events
    ]
    if not decisions:
        decisions = [
            {
                "step_idx": None,
                "decision": "allow",
                "reason_codes": [],
                "lease_signal": "none",
                "unsafe_crossed_boundary": bool(case.get("retrieval_success", 0)),
                "model_visible_preview": "No defense; raw retrieved observation is included in trajectory.",
            }
        ]

    return {
        "case_type": case_type,
        "run_name": run_name,
        "case_path": str(path),
        "question_id": case.get("question_idx"),
        "user_query": case.get("question"),
        "retrieved_records": retrieved_records,
        "defense_decisions": decisions,
        "model_visible_context_tail": _visible_context(case),
        "final_answer": case.get("answer"),
        "attack_manifestation": bool(case.get("attack_manifested", False)),
        "action_trace_present": bool(case.get("traj")),
        "unsafe_content_crossed_retrieval_exposure_boundary": bool(case.get("retrieval_success", 0)),
        "raw_poisoned_retrieval": bool(case.get("raw_retrieval_success", 0)),
    }


def _write_md(path: Path, records: list[dict[str, Any]]) -> None:
    lines = ["# FlowFence-Lite Audit Cases", ""]
    for record in records:
        lines.extend(
            [
                f"## {record['case_type']}",
                "",
                f"- run: `{record['run_name']}`",
                f"- question id: `{record['question_id']}`",
                f"- raw poisoned retrieval: `{record['raw_poisoned_retrieval']}`",
                f"- unsafe crossed retrieval-exposure boundary: `{record['unsafe_content_crossed_retrieval_exposure_boundary']}`",
                f"- attack manifestation: `{record['attack_manifestation']}`",
                f"- final answer: `{record['final_answer']}`",
                "",
                "| step | decision | reason codes | boundary crossed |",
                "|---|---|---|---|",
            ]
        )
        for decision in record["defense_decisions"]:
            lines.append(
                f"| {decision['step_idx']} | {decision['decision']} | "
                f"{', '.join(decision['reason_codes'])} | {decision['unsafe_crossed_boundary']} |"
            )
        lines.extend(["", "```text", str(record["model_visible_context_tail"])[-1200:], "```", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Export compact audit cases from AgentPoison full-ReAct artifacts")
    parser.add_argument("--results-root", default="results")
    parser.add_argument("--out-dir", default="artifacts/icde2027_supplemental/audit_cases")
    args = parser.parse_args()

    results_root = Path(args.results_root)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    records = []
    for case_type, run_names in DEFAULT_CANDIDATES.items():
        found = _find_case(results_root, run_names, case_type)
        if found is None:
            records.append({"case_type": case_type, "status": "not_found", "candidate_runs": run_names})
            continue
        run_name, path, case = found
        records.append(_record_from_case(case_type, run_name, path, case))

    with (out_dir / "audit_cases.jsonl").open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    (out_dir / "audit_cases.json").write_text(json.dumps(records, indent=2), encoding="utf-8")
    _write_md(out_dir / "audit_cases.md", records)
    print(json.dumps({"status": "ok", "out_dir": str(out_dir), "case_count": len(records)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
