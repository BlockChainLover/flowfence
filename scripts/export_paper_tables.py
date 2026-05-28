#!/usr/bin/env python3
"""Export paper-facing result tables from committed high-level evidence.

This script intentionally reads only summary/evidence artifacts committed to the
repository. It does not read raw event traces, provider outputs, prompts, or
per-run generated directories.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Iterable


NA = "NA"

P0_SOURCES = {
    "main": Path("results/baseline_agentpoison_fullreact_minimax27_small_matrix_summary.json"),
    "ablation": Path("results/ablation_agentpoison_fullreact_minimax27_quarantine_only_vs_actioncanon_summary.json"),
    "rewrite": Path("results/baseline_agentpoison_fullreact_minimax27_rewrite_only_weak_comparator_summary.json"),
    "static": Path("results/baseline_agentpoison_fullreact_minimax27_static_keyword_filter_weak_comparator_summary.json"),
    "heldout": Path("results/baseline_agentpoison_fullreact_minimax27_heldout_instruction_matrix_summary.json"),
    "overhead_measured": Path("results/overhead_agentpoison_fullreact_minimax27_same_axis_measured_summary.json"),
    "overhead_proxy": Path("results/overhead_agentpoison_fullreact_minimax27_same_axis_proxy_summary.json"),
}

P1_SOURCES = {
    "mas_sweep": Path("artifacts/codex_task_state/codex_p1_mas_sweep.md"),
    "benchmark_strengthening": Path("artifacts/codex_task_state/codex_p1_benchmark_strengthening.md"),
}

MINIMAX_SOURCES = {
    "summary_18run": Path("artifacts/minimax_p1_smoke_postfix/summary_18run.json"),
    "run_manifest": Path("artifacts/minimax_p1_smoke_postfix/run_manifest.json"),
    "audit_summary": Path("artifacts/minimax_p1_smoke_postfix_audit/audit_summary.json"),
    "failure_breakdown": Path("artifacts/minimax_p1_smoke_postfix_audit/failure_breakdown.jsonl"),
}

CLAIM_SOURCES = {
    "evidence_index": Path("results/evidence_index/current_evidence_index.md"),
    "claims_checklist": Path("papers/claims_checklist.md"),
    "claims_refresh_3": Path("artifacts/evidence_index/p1_claims_refresh_3.md"),
}

ALL_REQUIRED = {
    **P0_SOURCES,
    **P1_SOURCES,
    **MINIMAX_SOURCES,
    **CLAIM_SOURCES,
}

RAW_SECRET_MARKERS = [
    "$4800",
    "supplier breach investigation",
    "CUST-8831-PRIVATE",
    "sk-internal-demo-token",
]


def load_json(path: Path, warnings: list[str], strict: bool) -> dict[str, Any]:
    if not path.exists():
        msg = f"MISSING_OR_NOT_INSPECTED: {path}"
        warnings.append(msg)
        if strict:
            raise FileNotFoundError(msg)
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_text(path: Path, warnings: list[str], strict: bool) -> str:
    if not path.exists():
        msg = f"MISSING_OR_NOT_INSPECTED: {path}"
        warnings.append(msg)
        if strict:
            raise FileNotFoundError(msg)
        return ""
    return path.read_text(encoding="utf-8")


def load_jsonl(path: Path, warnings: list[str], strict: bool) -> list[dict[str, Any]]:
    if not path.exists():
        msg = f"MISSING_OR_NOT_INSPECTED: {path}"
        warnings.append(msg)
        if strict:
            raise FileNotFoundError(msg)
        return []
    rows = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            msg = f"JSONL_PARSE_ERROR: {path}:{lineno}: {exc}"
            warnings.append(msg)
            if strict:
                raise
    return rows


def mean_metric(group: dict[str, Any], metric: str) -> Any:
    value = group.get("aggregate", {}).get(metric, {})
    if isinstance(value, dict) and "mean" in value:
        return value["mean"]
    return NA


def run_count(group: dict[str, Any]) -> Any:
    runs = group.get("runs")
    if isinstance(runs, list):
        return len(runs)
    artifacts = group.get("artifacts")
    if isinstance(artifacts, list):
        return len(artifacts)
    if "run_count" in group:
        return group["run_count"]
    return NA


def fmt(value: Any) -> str:
    if value is None:
        return NA
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return f"{value:.6f}".rstrip("0").rstrip(".")
    if isinstance(value, (list, tuple)):
        return "; ".join(fmt(v) for v in value)
    return str(value)


def write_csv(path: Path, rows: list[dict[str, Any]], headers: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: fmt(row.get(key, NA)) for key in headers})


def escape_md(value: Any) -> str:
    text = fmt(value)
    return text.replace("|", "\\|").replace("\n", "<br>")


def write_markdown_table(path: Path, title: str, rows: list[dict[str, Any]], headers: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# {title}", ""]
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    for row in rows:
        lines.append("| " + " | ".join(escape_md(row.get(h, NA)) for h in headers) + " |")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def p0_row(axis: str, provider: str, condition: str, group: dict[str, Any], caveat: str, evidence_path: Path) -> dict[str, Any]:
    return {
        "evidence_axis": axis,
        "provider": provider,
        "condition": condition,
        "runs": run_count(group),
        "clean_utility_rate_mean": mean_metric(group, "clean_utility_rate"),
        "attacked_utility_rate_mean": mean_metric(group, "attacked_utility_rate"),
        "attack_manifestation_rate_mean": mean_metric(group, "attack_manifestation_rate"),
        "exposed_poisoned_retrieval_case_rate_mean": mean_metric(group, "exposed_poisoned_retrieval_case_rate"),
        "raw_poisoned_retrieval_case_rate_mean": mean_metric(group, "raw_poisoned_retrieval_case_rate"),
        "defense_intervention_event_rate_mean": mean_metric(group, "defense_intervention_event_rate"),
        "benign_false_block_proxy_rate_mean": mean_metric(group, "benign_false_block_proxy_rate"),
        "caveat": caveat,
        "evidence_path": str(evidence_path),
    }


def build_table_1(warnings: list[str], strict: bool) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    main = load_json(P0_SOURCES["main"], warnings, strict)
    provider = main.get("provider_profile", "minimax27")
    for condition in ["no_defense", "flowfence_lite_quarantine_actioncanon"]:
        group = main.get("groups", {}).get(condition)
        if group:
            rows.append(p0_row("adapted_agentpoison_fullreact_retrieval_memory", provider, condition, group, "Adapted AgentPoison comparator; MiniMax only; retrieval-memory only; not official reproduction.", P0_SOURCES["main"]))

    ablation = load_json(P0_SOURCES["ablation"], warnings, strict)
    provider = ablation.get("provider_profile", "minimax27")
    for condition in ["quarantine_only", "quarantine_actioncanon"]:
        group = ablation.get("groups", {}).get(condition)
        if group:
            rows.append(p0_row("p0_quarantine_ablation", provider, condition, group, "Same adapted retrieval-memory axis; mechanism ablation, not broad generalization.", P0_SOURCES["ablation"]))

    rewrite = load_json(P0_SOURCES["rewrite"], warnings, strict)
    group = rewrite.get("groups", {}).get("rewrite_only_weak_defense")
    if group:
        rows.append(p0_row("p0_rewrite_weak_comparator", rewrite.get("provider_profile", "minimax27"), "rewrite_only_weak_comparator", group, "Same detector-mediated axis; weak comparator, not broad rewrite robustness.", P0_SOURCES["rewrite"]))

    static = load_json(P0_SOURCES["static"], warnings, strict)
    group = static.get("groups", {}).get("static_keyword_filter")
    if group:
        rows.append(p0_row("p0_static_keyword_weak_comparator", static.get("provider_profile", "minimax27"), "static_keyword_filter_weak_comparator", group, "Known-trigger same-axis baseline; brittle under paraphrase/adaptive attacks.", P0_SOURCES["static"]))

    heldout = load_json(P0_SOURCES["heldout"], warnings, strict)
    provider = heldout.get("provider_profile", "minimax27")
    for condition in ["static_keyword_filter_nonoracle", "flowfence_lite_quarantine_actioncanon"]:
        group = heldout.get("groups", {}).get(condition)
        if group:
            rows.append(p0_row("p0_heldout_instruction_stress", provider, f"heldout_{condition}", group, "Held-out instruction stress test only; same retrieval anchor; not broad held-out generalization.", P0_SOURCES["heldout"]))
    return rows


def extract_line(text: str, prefix: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(prefix):
            return stripped.lstrip("- ").strip()
    return NA


def build_table_2(warnings: list[str], strict: bool) -> list[dict[str, Any]]:
    sweep_text = load_text(P1_SOURCES["mas_sweep"], warnings, strict)
    strengthen_text = load_text(P1_SOURCES["benchmark_strengthening"], warnings, strict)
    return [
        {
            "evidence_axis": "initial_deterministic_mas_sweep",
            "provider_metadata": "minimax",
            "provider_calls_enabled": "false",
            "run_count": "144 expected/completed in prior sweep summary",
            "topology_effect_observed": "false in prior sweep summary",
            "no_defense_meaningful_leakage": "yes in prior sweep summary",
            "flowfence_vs_no_defense_raw_leakage": "improved in 12/12 topology x attack groups",
            "flowfence_vs_no_defense_external_leakage": "improved in 12/12 topology x attack groups",
            "flowfence_vs_static_acl_indirect": "tied before strengthening",
            "flowfence_vs_prompt_filter_indirect": "tied before strengthening",
            "topology_claim_status": "unsupported before strengthening",
            "caveat": "Deterministic scripted runtime only; generated validation outputs not committed.",
            "evidence_path": str(P1_SOURCES["mas_sweep"]),
        },
        {
            "evidence_axis": "strengthened_deterministic_mas_benchmark",
            "provider_metadata": "minimax",
            "provider_calls_enabled": "false",
            "run_count": "252 completed / 0 failed",
            "topology_effect_observed": "true",
            "no_defense_meaningful_leakage": "yes",
            "flowfence_vs_no_defense_raw_leakage": "improved on 18 attack/topology groups; tied on 3 no-attack groups",
            "flowfence_vs_no_defense_external_leakage": "improved on 18 attack/topology groups; tied on 3 no-attack groups",
            "flowfence_vs_static_acl_indirect": "improved on all 9 indirect groups for cascade/privilege; improved 6/9 raw leakage and 4/9 external leakage",
            "flowfence_vs_prompt_filter_indirect": "improved on all 9 indirect attack/topology groups for raw leakage, external leakage, cascade size, and privilege reach",
            "topology_claim_status": "supported for deterministic synthetic benchmark only",
            "caveat": "Synthetic deterministic evidence only; no provider calls; not real-model generalization.",
            "evidence_path": str(P1_SOURCES["benchmark_strengthening"]),
        },
    ]


def comparison_text(obj: dict[str, Any], key: str) -> str:
    comp = obj.get(key, {})
    parts = []
    for metric in ["unauthorized_raw_leakage", "external_leakage"]:
        m = comp.get(metric, {})
        if m:
            parts.append(f"{metric}: improves {m.get('improves', NA)}/6, ties {m.get('ties', NA)}/6, underperforms {m.get('underperforms', NA)}/6")
    return "; ".join(parts) if parts else NA


def build_table_3(warnings: list[str], strict: bool) -> list[dict[str, Any]]:
    summary = load_json(MINIMAX_SOURCES["summary_18run"], warnings, strict)
    manifest = load_json(MINIMAX_SOURCES["run_manifest"], warnings, strict)
    audit = load_json(MINIMAX_SOURCES["audit_summary"], warnings, strict)
    failures = load_jsonl(MINIMAX_SOURCES["failure_breakdown"], warnings, strict)
    overall = summary.get("overall_metrics", {})
    rows = [
        {
            "evidence_axis": "p1_minimax_postfix_18run_smoke",
            "provider": summary.get("provider", manifest.get("provider", "minimax")),
            "provider_calls_enabled": summary.get("provider_calls_enabled", manifest.get("provider_calls_enabled", True)),
            "agent_backend": summary.get("agent_backend", manifest.get("agent_backend", "minimax_final_writer")),
            "group": "aggregate",
            "completed_runs": summary.get("completed_run_count", manifest.get("eighteen_run", {}).get("completed_run_count", NA)),
            "failed_runs": summary.get("failed_run_count", manifest.get("eighteen_run", {}).get("failed_run_count", NA)),
            "task_success_rate": overall.get("task_success_rate", audit.get("aggregate_task_success_rate", NA)),
            "unauthorized_raw_leakage_mean": overall.get("unauthorized_raw_leakage_mean", audit.get("aggregate_unauthorized_raw_leakage_mean", NA)),
            "external_leakage_mean": overall.get("external_leakage_mean", audit.get("aggregate_external_leakage_mean", NA)),
            "cascade_size_mean": overall.get("cascade_size_mean", audit.get("aggregate_cascade_size_mean", NA)),
            "privilege_reach_mean": overall.get("privilege_reach_mean", audit.get("aggregate_privilege_reach_mean", NA)),
            "topology_effect_observed": overall.get("topology_effect_observed", audit.get("topology_effect_observed", NA)),
            "failure_groups": "; ".join(f"{f.get('topology')} / {f.get('attack')} / {f.get('defense')} / seed={f.get('seed')}" for f in failures) or NA,
            "caveat": "Small MiniMax-only 18-run smoke; not full real-model robustness.",
            "evidence_path": str(MINIMAX_SOURCES["summary_18run"]),
        }
    ]
    by_defense = summary.get("by_defense", {})
    audit_status = {
        "flowfence_lite": audit.get("flowfence_group_status", {}),
        "none": audit.get("no_defense_group_status", {}),
        "prompt_filter": audit.get("prompt_filter_group_status", {}),
    }
    for defense in ["flowfence_lite", "none", "prompt_filter"]:
        group = by_defense.get(defense, {})
        status = audit_status.get(defense, {})
        rows.append(
            {
                "evidence_axis": "p1_minimax_postfix_18run_smoke",
                "provider": summary.get("provider", "minimax"),
                "provider_calls_enabled": summary.get("provider_calls_enabled", True),
                "agent_backend": summary.get("agent_backend", "minimax_final_writer"),
                "group": f"{defense}_subset",
                "completed_runs": group.get("run_count", status.get("run_count", NA)),
                "failed_runs": 0 if group.get("run_count") is not None else NA,
                "task_success_rate": group.get("task_success_rate", status.get("task_success_rate", NA)),
                "unauthorized_raw_leakage_mean": group.get("unauthorized_raw_leakage_mean", status.get("unauthorized_raw_leakage_mean", NA)),
                "external_leakage_mean": group.get("external_leakage_mean", status.get("external_leakage_mean", NA)),
                "cascade_size_mean": group.get("cascade_size_mean", status.get("cascade_size_mean", NA)),
                "privilege_reach_mean": group.get("privilege_reach_mean", status.get("privilege_reach_mean", NA)),
                "topology_effect_observed": overall.get("topology_effect_observed", NA),
                "failure_groups": "; ".join(f"{f.get('topology')} / {f.get('attack')} / {f.get('defense')} / seed={f.get('seed')}" for f in failures if f.get("defense") == defense) or NA,
                "caveat": "Subset audit from small MiniMax smoke; scoped to saved 6-run subset.",
                "evidence_path": str(MINIMAX_SOURCES["audit_summary"]),
            }
        )
    for f in failures:
        rows.append(
            {
                "evidence_axis": "p1_minimax_postfix_18run_smoke",
                "provider": summary.get("provider", "minimax"),
                "provider_calls_enabled": summary.get("provider_calls_enabled", True),
                "agent_backend": summary.get("agent_backend", "minimax_final_writer"),
                "group": f"{f.get('topology')} / {f.get('attack')} / {f.get('defense')} / seed={f.get('seed')}",
                "completed_runs": 1,
                "failed_runs": 0,
                "task_success_rate": 1.0 if f.get("task_success") else 0.0,
                "unauthorized_raw_leakage_mean": f.get("unauthorized_raw_leakage", NA),
                "external_leakage_mean": f.get("external_leakage", NA),
                "cascade_size_mean": f.get("cascade_size", NA),
                "privilege_reach_mean": f.get("privilege_reach", NA),
                "topology_effect_observed": overall.get("topology_effect_observed", NA),
                "failure_groups": f.get("failure_type", NA),
                "caveat": "Expected baseline failure; high-level metrics only, no raw output.",
                "evidence_path": str(MINIMAX_SOURCES["failure_breakdown"]),
            }
        )
    return rows


def build_table_4() -> list[dict[str, Any]]:
    return [
        {"claim_id": "C1/C2", "claim": "P0 adapted AgentPoison retrieval containment", "evidence_level": "P0", "evidence_type": "adapted comparator summary", "supported_status": "supported", "confidence": "medium", "ready_for_paper": "yes, with caveat", "caveat": "Adapted AgentPoison full-ReAct MiniMax comparator; not official reproduction.", "evidence_path": str(P0_SOURCES["main"])},
        {"claim_id": "C2", "claim": "P0 FlowFence quarantine-actioncanon containment", "evidence_level": "P0", "evidence_type": "adapted comparator summary", "supported_status": "supported", "confidence": "medium", "ready_for_paper": "yes, with caveat", "caveat": "Retrieval-memory axis only; exposed poisoned retrieval and attack manifestation zero in saved runs.", "evidence_path": str(P0_SOURCES["main"])},
        {"claim_id": "C3", "claim": "P0 utility roughly preserved/noisy", "evidence_level": "P0", "evidence_type": "summary metric", "supported_status": "partially supported", "confidence": "medium-low", "ready_for_paper": "yes, conservative wording only", "caveat": "MiniMax full-ReAct utility is noisy; do not claim utility improvement.", "evidence_path": str(P0_SOURCES["main"])},
        {"claim_id": "C12", "claim": "P0 static keyword same-axis caveat", "evidence_level": "P0", "evidence_type": "weak comparator", "supported_status": "supported as caveat", "confidence": "medium-low", "ready_for_paper": "yes, conservative wording only", "caveat": "Known-trigger same-axis static keyword filter is strong; structured containment should not be framed as uniquely necessary on this axis.", "evidence_path": str(P0_SOURCES["static"])},
        {"claim_id": "C9", "claim": "P1 deterministic topology effect", "evidence_level": "P1 synthetic", "evidence_type": "task-state validated sweep", "supported_status": "supported for deterministic synthetic only", "confidence": "medium", "ready_for_paper": "yes, synthetic benchmark wording only", "caveat": "No provider calls; not real-model topology generalization.", "evidence_path": str(P1_SOURCES["benchmark_strengthening"])},
        {"claim_id": "C10", "claim": "P1 deterministic FlowFence vs prompt_filter on indirect attacks", "evidence_level": "P1 synthetic", "evidence_type": "task-state validated sweep", "supported_status": "supported for deterministic synthetic only", "confidence": "medium", "ready_for_paper": "yes, synthetic benchmark wording only", "caveat": "Synthetic deterministic evidence only.", "evidence_path": str(P1_SOURCES["benchmark_strengthening"])},
        {"claim_id": "C22", "claim": "P1 MiniMax post-fix aggregate smoke", "evidence_level": "P1 MiniMax smoke", "evidence_type": "18-run smoke summary", "supported_status": "supported as small smoke", "confidence": "medium-low", "ready_for_paper": "yes, smoke evidence with caveat only", "caveat": "One-seed 18-run MiniMax smoke; not broad real-model robustness.", "evidence_path": str(MINIMAX_SOURCES["summary_18run"])},
        {"claim_id": "C23", "claim": "P1 MiniMax FlowFence clean subset", "evidence_level": "P1 MiniMax smoke", "evidence_type": "post-fix audit", "supported_status": "supported as small smoke", "confidence": "medium-low", "ready_for_paper": "yes, small MiniMax smoke wording only", "caveat": "Scoped to 6 FlowFence runs in saved smoke.", "evidence_path": str(MINIMAX_SOURCES["audit_summary"])},
        {"claim_id": "C24/C25", "claim": "P1 MiniMax prompt_filter indirect workspace poisoning failures", "evidence_level": "P1 MiniMax smoke", "evidence_type": "post-fix audit failure breakdown", "supported_status": "supported as small-smoke baseline caveat", "confidence": "medium-low", "ready_for_paper": "yes, audit/limitation evidence with caveat", "caveat": "Two prompt-filter workspace-poisoning failures; not broad prompt-filter evaluation.", "evidence_path": str(MINIMAX_SOURCES["failure_breakdown"])},
        {"claim_id": "U1", "claim": "Broad real-model robustness", "evidence_level": "unsupported", "evidence_type": "claim boundary", "supported_status": "unsupported", "confidence": "high confidence unsupported", "ready_for_paper": "no", "caveat": "Current real-provider evidence is only a small MiniMax smoke.", "evidence_path": str(CLAIM_SOURCES["claims_checklist"])},
        {"claim_id": "U2", "claim": "Non-MiniMax generalization", "evidence_level": "unsupported", "evidence_type": "claim boundary", "supported_status": "unsupported", "confidence": "high confidence unsupported", "ready_for_paper": "no", "caveat": "All real-provider evidence is MiniMax only.", "evidence_path": str(CLAIM_SOURCES["claims_checklist"])},
        {"claim_id": "U3", "claim": "Production safety claim", "evidence_level": "unsupported", "evidence_type": "claim boundary", "supported_status": "unsupported", "confidence": "high confidence unsupported", "ready_for_paper": "no", "caveat": "No production deployment evidence.", "evidence_path": str(CLAIM_SOURCES["claims_refresh_3"])},
        {"claim_id": "U4", "claim": "Official AgentPoison reproduction", "evidence_level": "unsupported", "evidence_type": "claim boundary", "supported_status": "unsupported", "confidence": "high confidence unsupported", "ready_for_paper": "no", "caveat": "P0 evidence is an adapted comparator only.", "evidence_path": str(CLAIM_SOURCES["claims_checklist"])},
    ]


def build_table_5() -> list[dict[str, Any]]:
    return [
        {"evidence_scope": "P0 AgentPoison retrieval-memory comparator", "what_it_supports": "Adapted MiniMax full-ReAct retrieval-memory containment and same-axis baseline caveats.", "what_it_does_not_support": "Official AgentPoison reproduction, broad provider generalization, or full multi-agent propagation.", "provider": "MiniMax", "provider_calls_enabled": "true in saved P0 runs", "run_count_or_scale": "3-run repeated summaries plus overhead slices", "main_caveat": "Adapted comparator; retrieval-memory only.", "next_required_evidence": "Table-ready presentation and optional additional baselines."},
        {"evidence_scope": "P1 deterministic synthetic MAS", "what_it_supports": "Scripted local MAS sweep and summary infrastructure.", "what_it_does_not_support": "Real-model behavior or topology claims by itself.", "provider": "MiniMax metadata only", "provider_calls_enabled": "false", "run_count_or_scale": "144-run initial deterministic matrix", "main_caveat": "Initial topology effects were absent before strengthening.", "next_required_evidence": "Use strengthened benchmark for topology/baseline claims."},
        {"evidence_scope": "P1 strengthened deterministic MAS", "what_it_supports": "Synthetic topology-dependent propagation and FlowFence-vs-baseline distinctions on indirect attacks.", "what_it_does_not_support": "Real-model robustness or deployment behavior.", "provider": "MiniMax metadata only", "provider_calls_enabled": "false", "run_count_or_scale": "252-run deterministic strengthened matrix", "main_caveat": "Deterministic scripted runtime only.", "next_required_evidence": "Map results into paper tables and compare with MiniMax smoke."},
        {"evidence_scope": "P1 MiniMax 18-run smoke", "what_it_supports": "Small real-MiniMax final-writer smoke, FlowFence clean subset, prompt-filter indirect workspace-poisoning failures.", "what_it_does_not_support": "Broad real-model robustness, multi-seed robustness, or non-MiniMax generalization.", "provider": "MiniMax", "provider_calls_enabled": "true", "run_count_or_scale": "18 runs, one seed", "main_caveat": "Small smoke only; raw traces and provider outputs uncommitted.", "next_required_evidence": "Manual table review, then optional broader MiniMax coverage."},
        {"evidence_scope": "Not yet done: broader MiniMax coverage", "what_it_supports": "NA", "what_it_does_not_support": "Real-model multi-seed robustness and broader topology/attack coverage.", "provider": "MiniMax", "provider_calls_enabled": "not run", "run_count_or_scale": "not done", "main_caveat": "Do not claim broad MiniMax robustness yet.", "next_required_evidence": "Broader but still scoped MiniMax matrix after table review."},
        {"evidence_scope": "Not yet done: non-MiniMax providers", "what_it_supports": "NA", "what_it_does_not_support": "Unsupported: non-MiniMax generalization.", "provider": "not done", "provider_calls_enabled": "not run", "run_count_or_scale": "not done", "main_caveat": "Provider rule remains MiniMax-only.", "next_required_evidence": "Human-approved provider scope change would be required."},
        {"evidence_scope": "Not yet done: real browser / desktop agents", "what_it_supports": "NA", "what_it_does_not_support": "Browser or desktop-agent robustness.", "provider": "not done", "provider_calls_enabled": "not run", "run_count_or_scale": "not done", "main_caveat": "No browser/multimodal experiments.", "next_required_evidence": "Separate scoped experiment design."},
        {"evidence_scope": "Not yet done: learned graph risk scorer", "what_it_supports": "NA", "what_it_does_not_support": "Learned graph-risk scoring claims.", "provider": "not done", "provider_calls_enabled": "not run", "run_count_or_scale": "not done", "main_caveat": "Current scoring is deterministic/runtime rule-based.", "next_required_evidence": "Separate model/scorer development and evaluation."},
    ]


def write_readme(path: Path) -> None:
    text = """# Paper Tables

These are paper-facing tables generated only from committed high-level summaries and evidence documents.

Raw traces, raw provider outputs, prompts, event JSONL files, policy JSONL files, individual per-run metrics, credentials, and secrets are intentionally not included.

MiniMax is the only real provider represented. Deterministic P1 synthetic tables use MiniMax as metadata only with provider calls disabled.

These tables must not be treated as final paper numbers until manually reviewed. Unsupported claims remain unsupported.
"""
    path.write_text(text, encoding="utf-8")


def write_summary(output_dir: Path, warnings: list[str], generated: list[str], source_paths: Iterable[Path]) -> None:
    summary_files = ["paper_tables_summary.json", "paper_tables_summary.md"]
    generated_with_summary = [*generated, *[name for name in summary_files if name not in generated]]
    summary = {
        "schema_version": "flowfence_paper_tables_v1",
        "generated_tables": generated_with_summary,
        "source_artifacts_used": [str(p) for p in source_paths],
        "warnings": warnings,
        "provider_boundary": "MiniMax is the only real provider represented; no non-MiniMax generalization is supported.",
        "raw_data_boundary": "Raw traces, provider outputs, prompts, event JSONL, policy JSONL, and per-run metrics are not read or included.",
        "recommended_next_step": "p1-paper-table-review",
    }
    (output_dir / "paper_tables_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# Paper Tables Summary",
        "",
        "## Generated tables",
    ]
    for name in generated:
        lines.append(f"- `{name}`")
    lines.extend(["", "## Source artifacts used"])
    for path in source_paths:
        lines.append(f"- `{path}`")
    lines.extend(["", "## Warnings"])
    if warnings:
        lines.extend(f"- {w}" for w in warnings)
    else:
        lines.append("- None")
    lines.extend([
        "",
        "## Evidence boundaries",
        "",
        "These tables use committed high-level summaries only. MiniMax is the only real provider represented. Unsupported claims remain unsupported.",
        "",
        "## Recommended next step",
        "",
        "`p1-paper-table-review`",
        "",
    ])
    (output_dir / "paper_tables_summary.md").write_text("\n".join(lines), encoding="utf-8")


def selected_outputs(format_arg: str) -> set[str]:
    if format_arg == "all":
        return {"csv", "markdown", "json"}
    return {part.strip() for part in format_arg.split(",") if part.strip()}


def export_tables(output_dir: Path, strict: bool, format_arg: str) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    warnings: list[str] = []
    formats = selected_outputs(format_arg)
    generated: list[str] = []

    # Touch all required claim text sources so missing evidence is recorded.
    for path in CLAIM_SOURCES.values():
        load_text(path, warnings, strict)
    # Touch overhead sources even though they are currently summarized as boundaries.
    for key in ["overhead_measured", "overhead_proxy"]:
        load_json(P0_SOURCES[key], warnings, strict)

    tables = [
        ("table_1_p0_agentpoison", "Table 1: P0 AgentPoison Containment", build_table_1(warnings, strict), [
            "evidence_axis", "provider", "condition", "runs", "clean_utility_rate_mean", "attacked_utility_rate_mean", "attack_manifestation_rate_mean", "exposed_poisoned_retrieval_case_rate_mean", "raw_poisoned_retrieval_case_rate_mean", "defense_intervention_event_rate_mean", "benign_false_block_proxy_rate_mean", "caveat", "evidence_path",
        ]),
        ("table_2_p1_synthetic", "Table 2: P1 Deterministic Synthetic MAS", build_table_2(warnings, strict), [
            "evidence_axis", "provider_metadata", "provider_calls_enabled", "run_count", "topology_effect_observed", "no_defense_meaningful_leakage", "flowfence_vs_no_defense_raw_leakage", "flowfence_vs_no_defense_external_leakage", "flowfence_vs_static_acl_indirect", "flowfence_vs_prompt_filter_indirect", "topology_claim_status", "caveat", "evidence_path",
        ]),
        ("table_3_minimax_postfix_smoke", "Table 3: P1 MiniMax Post-Fix Smoke", build_table_3(warnings, strict), [
            "evidence_axis", "provider", "provider_calls_enabled", "agent_backend", "group", "completed_runs", "failed_runs", "task_success_rate", "unauthorized_raw_leakage_mean", "external_leakage_mean", "cascade_size_mean", "privilege_reach_mean", "topology_effect_observed", "failure_groups", "caveat", "evidence_path",
        ]),
        ("table_4_claims_matrix", "Table 4: Claims Matrix", build_table_4(), [
            "claim_id", "claim", "evidence_level", "evidence_type", "supported_status", "confidence", "ready_for_paper", "caveat", "evidence_path",
        ]),
        ("table_5_evidence_boundaries", "Table 5: Evidence Boundaries", build_table_5(), [
            "evidence_scope", "what_it_supports", "what_it_does_not_support", "provider", "provider_calls_enabled", "run_count_or_scale", "main_caveat", "next_required_evidence",
        ]),
    ]

    for stem, title, rows, headers in tables:
        if "csv" in formats:
            write_csv(output_dir / f"{stem}.csv", rows, headers)
            generated.append(f"{stem}.csv")
        if "markdown" in formats:
            write_markdown_table(output_dir / f"{stem}.md", title, rows, headers)
            generated.append(f"{stem}.md")

    if "markdown" in formats:
        write_readme(output_dir / "README.md")
        generated.append("README.md")
    if "json" in formats:
        write_summary(output_dir, warnings, generated, ALL_REQUIRED.values())
        generated.extend(["paper_tables_summary.json", "paper_tables_summary.md"])
    elif "markdown" in formats:
        # Keep a Markdown summary available for markdown-only exports.
        write_summary(output_dir, warnings, generated, ALL_REQUIRED.values())
        generated.append("paper_tables_summary.md")

    return {"warnings": warnings, "generated": generated}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export paper-facing tables from committed FlowFence-Lite evidence summaries.")
    parser.add_argument("--output-dir", default="artifacts/paper_tables", help="Directory for generated table files.")
    parser.add_argument("--strict", action="store_true", help="Fail if a required committed evidence artifact is missing or malformed.")
    parser.add_argument("--format", default="all", help="Output formats: all, or comma-separated subset of markdown,csv,json.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    allowed = {"all", "markdown", "csv", "json", "markdown,csv", "csv,markdown", "markdown,json", "json,markdown", "csv,json", "json,csv", "markdown,csv,json", "markdown,json,csv", "csv,markdown,json", "csv,json,markdown", "json,markdown,csv", "json,csv,markdown"}
    if args.format not in allowed:
        raise SystemExit(f"unsupported --format {args.format!r}; use all or comma-separated markdown,csv,json")
    result = export_tables(Path(args.output_dir), strict=args.strict, format_arg=args.format)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
