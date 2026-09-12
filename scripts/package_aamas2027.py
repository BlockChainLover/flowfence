#!/usr/bin/env python3
"""Rebuild AAMAS tables from safe raw records and package an explicit file list.

Run from the repository root with PYTHONPATH=.; no model calls are made.
Public synthetic fixture values in executable source/data are intentional.
Shareable result records are checked for registered raw values before bundling.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
import statistics
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.experiments.aamas_stress import summarize as summarize_stress
from src.runtime.policy import default_secret_policies

NAMES = {"none": "No Defense", "ifc_safeview": "IFC-SafeView", "flowfence_lite_nonoracle": "PAPC"}
COMPLETED = {"complete", "completed"}
TERMINAL = COMPLETED | {"failed", "blocked"}
ROOT_REPORTS = {"MANIFEST.json", "PRIOR_EVIDENCE_AUDIT.md", "prior_evidence_inventory.json",
                "EXPERIMENT_SUMMARY.md", "PAPER_INTEGRATION.md", "README.md", "TEST_REPORT.md",
                "report_data.json", "BUNDLE_MANIFEST.json", "E1_INDEPENDENT_REVIEW.md"}
RUN_FILES = {"episodes.jsonl", "events.safe.jsonl", "events.jsonl", "call_attempts.jsonl", "summary.json",
             "registration.json", "run_manifest.json", "run_metadata.json", "completion.json",
             "audit_storage_measurements.json", "serialized_audit_fixtures.jsonl", "safe_probe_events.jsonl",
             "summary_with_intervals.json", "failure_cases.safe.json", "failure_cases.safe.csv"}
EXPERIMENT_DIRS = {"E0_equal_capability", "E1_llm_agents", "E2_overhead", "E3_semantic_stress",
                   "E4_second_model", "E5_topology_ablation"}
SOURCE_FILES = {
    "scripts/package_aamas2027.py", "scripts/run_aamas_equal.py", "scripts/run_aamas_llm_agents.py",
    "scripts/run_aamas_stress.py", "src/experiments/aamas_equal.py", "src/experiments/aamas_llm_agents.py",
    "scripts/summarize_aamas_llm_agents.py", "src/experiments/aamas_paired.py",
    "src/experiments/aamas_stress.py", "src/defenses/mas_flowfence.py", "src/common/provider_loader.py",
    "data/multiagent_tasks/enterprise_assistant_v1.jsonl", "experiments/aamas2027/README.md",
    "src/runtime/policy.py", "src/runtime/events.py", "src/runtime/orchestrator.py", "src/runtime/topology.py",
    "src/runtime/memory.py", "src/runtime/workspace.py", "src/runtime/minimax_client.py",
    "src/attacks/base.py", "src/attacks/summary_poisoning.py", "src/attacks/workspace_poisoning.py",
    "src/attacks/comm_hijack.py", "src/evaluators/utility.py", "src/evaluators/leakage.py",
    "src/evaluators/cascade.py", "src/evaluators/privilege.py",
    "tests/test_aamas_equal.py", "tests/test_aamas_llm_agents.py", "tests/test_aamas_stress.py",
    "tests/test_aamas_package.py",
}
CONFIG_FILES = {"e0_equal.json", "e1_pilot.json", "e1_formal.json", "e1_tasks.json",
                "e2_overhead.json", "e3_semantic_stress.json", "e4_second_model.json", "e1_second_model_kimi.json", "e5_topology_ablation.json"}
LOG_NAME = re.compile(r"(?:e[0-5]_[a-z0-9_\-]+|targeted[a-z0-9_\-]*|full[a-z0-9_\-]*|test[a-z0-9_\-]*|regression[a-z0-9_\-]*|package[a-z0-9_\-]*|pilot_audit)\.(?:txt|log|json|xml)$", re.I)
TABLE_NAME = re.compile(r"(?:table_[a-f][a-z0-9_]*|e[0-5]_[a-z0-9_]+)\.(?:csv|json|md)$", re.I)


def read_json(path: Path, default: Any = None) -> Any:
    return json.loads(path.read_text()) if path.is_file() else default


def read_rows(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    with path.open() as handle:
        return [json.loads(line) for line in handle if line.strip()]


def save_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def average(rows: list[dict[str, Any]], key: str) -> float | None:
    values = [float(r[key]) for r in rows if isinstance(r.get(key), (int, float, bool))]
    return statistics.mean(values) if values else None


def is_live_row(row: dict[str, Any]) -> bool:
    backend = str(row.get("agent_backend", ""))
    return not ("fixture" in backend or "dry" in backend or row.get("model_version") == "dry-run-fixture")


def llm_evidence(folder: Path) -> dict[str, Any]:
    all_rows = read_rows(folder / "episodes.jsonl")
    registration = read_json(folder / "registration.json", {})
    fixture = bool(registration.get("dry_run"))
    rows = [] if fixture else [r for r in all_rows if is_live_row(r)]
    primary = [r for r in rows if r.get("attempt", 1) == 1]
    keys = [(r["task_id"], r["topology"], r["condition"], r["seed"], r["defense"]) for r in primary]
    if len(set(keys)) != len(keys):
        raise ValueError("Duplicate primary LLM episode keys")
    calls = {} if fixture else {r["call_id"]: r for r in read_rows(folder / "call_attempts.jsonl")}
    calls = {k: r for k, r in calls.items() if r.get("provider_request", True)}
    config = registration.get("config", {})
    expected = math.prod(len(config[k]) for k in ("task_ids", "topologies", "conditions", "defenses", "seeds")) if all(config.get(k) for k in ("task_ids", "topologies", "conditions", "defenses", "seeds")) else None
    complete = sum(r.get("status") in COMPLETED for r in rows)
    audit_bytes: Counter[str] = Counter()
    run_defenses = {r["run_id"]: r["defense"] for r in rows}
    for filename in ("episodes.jsonl", "events.jsonl", "call_attempts.jsonl"):
        path = folder / filename
        if path.exists():
            with path.open("rb") as handle:
                for line in handle:
                    if line.strip():
                        run_id = json.loads(line).get("run_id")
                        if run_id in run_defenses:
                            audit_bytes[run_defenses[run_id]] += len(line)
    storage_by_defense = [{"defense": defense, "episodes": sum(r["defense"] == defense for r in rows),
                          "audit_bytes": size, "audit_kib_per_episode": size / sum(r["defense"] == defense for r in rows) / 1024}
                         for defense, size in sorted(audit_bytes.items())]
    call_count = len(calls) if calls else sum(r.get("llm_calls", 0) for r in rows)
    terminal = [r for r in primary if r.get("status") in TERMINAL]
    coverage_complete = bool(primary) and len(terminal) == len(primary) and (expected is None or len(terminal) == expected)
    measured_primary = [r for r in primary if r.get("status") in COMPLETED and not r.get("metrics_partial") and r.get("privacy_measurement_complete", True)]
    return {"rows": rows, "primary": primary, "diagnostic_fixture_rows": len(all_rows)-len(rows),
            "expected_primary_episodes": expected, "episodes": len(rows), "primary_episodes": len(primary),
            "registered_terminal_episodes": len(terminal), "terminal_episode_records": sum(r.get("status") in TERMINAL for r in rows),
            "completed_model_episodes": sum(r.get("status") in COMPLETED for r in primary),
            "measurement_complete_primary_episodes": len(measured_primary),
            "measurement_coverage": len(measured_primary) / (expected or len(primary)) if expected or primary else None,
            "completed_episodes": complete, "failed_episodes": sum(r.get("status") == "failed" for r in rows),
            "blocked_episodes": sum(r.get("status") == "blocked" for r in rows),
            "excluded_episodes": 0, "llm_calls": call_count,
            "failed_call_attempts": sum(r.get("status") == "failed" for r in calls.values()),
            "unfinished_call_attempts": sum(r.get("status") == "started" for r in calls.values()),
            "returned_model_outputs": sum(bool(r.get("response_chars", 0)) for r in calls.values()),
            "error_counts": dict(Counter(r.get("error_type") for r in rows if r.get("error_type"))),
            "linked_retry_episodes": sum(bool(r.get("retry_of")) for r in rows),
            "input_tokens": sum(r.get("input_tokens", 0) for r in calls.values()) if calls else sum(r.get("input_tokens", 0) for r in rows),
            "output_tokens": sum(r.get("output_tokens", 0) for r in calls.values()) if calls else sum(r.get("output_tokens", 0) for r in rows),
            "requested_models": sorted({str(r.get("model")) for r in rows}),
            "returned_models": sorted({str(r.get("model_version")) for r in rows if r.get("model_version")}),
            "task_count": len({r["task_id"] for r in primary}), "seed_count": len({r["seed"] for r in primary}),
            "scenario_count": len({r.get("scenario_id") for r in primary}),
            "coverage_complete": coverage_complete, "audit_storage_total_bytes": sum(audit_bytes.values()),
            "audit_storage_by_defense": storage_by_defense,
            "audit_storage_scope": "actual serialized episodes/events/call-attempt JSONL including started and completed call audit rows; all eligible saved episode attempts",
            "status": "COMPLETE" if coverage_complete and complete > 0 else ("PARTIAL" if complete > 0 else "BLOCKED")}


def compare_pairs(rows: list[dict[str, Any]], keys: tuple[str, ...]) -> list[dict[str, Any]]:
    index = {tuple(r[k] for k in keys) + (r["defense"],): r for r in rows}
    if len(index) != len(rows):
        raise ValueError("Duplicate matched episode keys")
    pairs = [(r, index[tuple(r[k] for k in keys) + ("ifc_safeview",)]) for r in rows
             if r["defense"] == "flowfence_lite_nonoracle" and tuple(r[k] for k in keys) + ("ifc_safeview",) in index]
    answer = []
    for metric in ("success", "privacy_safe_success", "raw_exposure", "external_exposure", "exposure_recipient_pairs", "intervention_count", "blocks"):
        usable = pairs if metric in {"success", "privacy_safe_success"} else [(a, b) for a, b in pairs if a.get("status") in COMPLETED and b.get("status") in COMPLETED and not a.get("metrics_partial") and not b.get("metrics_partial") and a.get("privacy_measurement_complete", True) and b.get("privacy_measurement_complete", True)]
        direction = 1 if metric in {"success", "privacy_safe_success"} else -1
        differences = [(float(a.get(metric, 0))-float(b.get(metric, 0))) * direction for a, b in usable]
        tasks: dict[str, list[float]] = defaultdict(list)
        for (a, _), difference in zip(usable, differences):
            tasks[a["task_id"]].append(difference)
        clustered = [statistics.mean(values) for values in tasks.values()]
        wins, losses = sum(v > 0 for v in clustered), sum(v < 0 for v in clustered)
        n = wins + losses
        p = min(1.0, 2 * sum(math.comb(n, i) for i in range(min(wins, losses)+1)) / 2**n) if n else 1.0
        answer.append({"metric": metric, "matched": len(pairs), "better": sum(d > 0 for d in differences),
                       "tie": sum(d == 0 for d in differences), "worse": sum(d < 0 for d in differences),
                       "unavailable": len(pairs)-len(usable), "mean_papc_minus_ifc": statistics.mean(differences)*direction if differences else None,
                       "task_clusters": len(tasks), "exact_sign_test_cluster_p": p})
    return answer


def table_groups(rows: list[dict[str, Any]], dimensions: tuple[str, ...], metrics: tuple[str, ...]) -> list[dict[str, Any]]:
    groups: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[tuple(row[d] for d in dimensions)].append(row)
    results = []
    for key, group in sorted(groups.items()):
        measured = [r for r in group if r.get("status") in COMPLETED and not r.get("metrics_partial") and r.get("privacy_measurement_complete", True)]
        item = {**dict(zip(dimensions, key)), "episodes": len(group),
                "failed_or_blocked": sum(r.get("status") not in COMPLETED for r in group),
                "privacy_complete_episodes": len(measured)}
        for metric in metrics:
            complete_measurement = "exposure" in metric or metric in {"cascade_size", "privilege_reach", "intervention_count", "blocks", "rewrites", "quarantines"}
            item[metric] = average(measured if complete_measurement else group, metric)
        results.append(item)
    return results


def cell(value: Any) -> str:
    if value is None:
        return "N/A"
    if isinstance(value, float):
        return f"{value:.6g}"
    return str(NAMES.get(value, value) if isinstance(value, str) else value).replace("|", "/").replace("\n", " ")


def markdown_table(rows: list[dict[str, Any]], columns: list[tuple[str, str]]) -> str:
    if not rows:
        return "No eligible observations available."
    return "\n".join(["| " + " | ".join(label for _, label in columns) + " |",
                       "| " + " | ".join("---" for _ in columns) + " |"] +
                      ["| " + " | ".join(cell(row.get(key)) for key, _ in columns) + " |" for row in rows])


def write_table(root: Path, name: str, rows: list[dict[str, Any]]) -> None:
    save_json(root / "tables" / f"{name}.json", rows)
    fields = list(dict.fromkeys(k for row in rows for k in row))
    with (root / "tables" / f"{name}.csv").open("w", newline="") as handle:
        if fields:
            writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
            writer.writeheader(); writer.writerows(rows)


def failure_cases(folder: Path, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Export only IDs, verifier flags, and bounded call metadata; no model text."""
    calls = {r["call_id"]: r for r in read_rows(folder / "call_attempts.jsonl")}
    cases = []
    for row in rows:
        if row.get("success"):
            continue
        failed_call = next((c for c in calls.values() if c.get("run_id") == row["run_id"] and c.get("status") == "failed"), {})
        cases.append({"run_id": row["run_id"], "task_id": row["task_id"], "topology": row["topology"],
                      "condition": row["condition"], "defense": row["defense"], "status": row["status"],
                      "error_type": row.get("error_type"), "failed_role": failed_call.get("role"),
                      "finish_reason": failed_call.get("finish_reason"), "failed_call_output_tokens": failed_call.get("output_tokens"),
                      "failed_correctness_fields": ", ".join(sorted(k for k, v in row.get("structured_correctness", {}).items() if v is False)),
                      "privacy_measurement_complete": row.get("privacy_measurement_complete", row.get("status") in COMPLETED),
                      "raw_exposure_observed": row.get("raw_exposure"), "raw_model_text_omitted": True})
    return cases


def collect(root: Path) -> dict[str, Any]:
    e0 = read_rows(root / "E0_equal_capability/formal/episodes.jsonl")
    e2 = read_rows(root / "E2_overhead/formal/episodes.jsonl")
    e3 = read_rows(root / "E3_semantic_stress/formal/episodes.jsonl")
    e1 = llm_evidence(root / "E1_llm_agents/formal")
    pilot = llm_evidence(root / "E1_llm_agents/pilot")
    e4 = llm_evidence(root / "E4_second_model/formal")
    e4_status = read_json(root / "E4_second_model/status.json", {})
    if e4_status.get("status"):
        e4["status"] = str(e4_status["status"])
    basic = ("success", "privacy_safe_success", "raw_exposure", "external_exposure", "exposure_recipient_pairs", "intervention_count", "blocks", "rewrites", "quarantines")
    e0_table = table_groups(e0, ("defense",), basic)
    e1_table = table_groups(e1["primary"], ("topology", "condition", "defense"), basic + ("source_raw_exposure", "source_external_exposure", "generated_raw_exposure", "generated_external_exposure", "llm_calls", "input_tokens", "output_tokens", "llm_latency_ms", "mediator_latency_ms", "e2e_latency_ms"))
    paired = []
    for topology, condition in [("chain_4", "clean"), ("chain_4", "attack"), ("blackboard_4", "clean"), ("blackboard_4", "attack"), ("overall", "overall")]:
        subset = e1["primary"] if topology == "overall" else [r for r in e1["primary"] if r["topology"] == topology and r["condition"] == condition]
        paired += [{"topology": topology, "condition": condition, **row} for row in compare_pairs(subset, ("task_id", "topology", "condition", "seed"))]
    experiment_rows = {"E0": e0, "E1": e1["rows"], "E2": e2, "E3": e3, "E4": e4["rows"]}
    counts = {name: {"episodes": len(rows), "failed_episodes": sum(r.get("status") == "failed" for r in rows),
                     "blocked_episodes": sum(r.get("status") == "blocked" for r in rows),
                     "task_ids": len({r["task_id"] for r in rows}), "seeds": len({r["seed"] for r in rows}),
                     "excluded_episodes": 0} for name, rows in experiment_rows.items()}
    return {"manifest": read_json(root / "MANIFEST.json", {}), "counts": counts,
            "e0_rows": e0, "e0_table": e0_table, "e0_pairs": compare_pairs(e0, ("task_id", "topology", "attack", "seed")),
            "e1": e1, "pilot": pilot, "e1_table": e1_table, "e1_pairs": paired,
            "e2_table": summarize_stress(e2, "E2") if e2 else [], "e3_table": summarize_stress(e3, "E3") if e3 else [],
            "e2_timed_events": sum(r.get("event_count", 0) for r in e2),
            "e2_warmup_calls": sum(r.get("warmup_events", 0) for r in e2),
            "e3_event_count": sum(r.get("event_count", 0) for r in e3),
            "e3_reconstruction_leaks": sum(r.get("measured_unauthorized_disclosure", False) for r in e3),
            "e3_exact_hits": sum(r.get("exact_string_exposure_events", 0) for r in e3),
            "e4": e4, "e4_status": e4_status,
            "e5_status": read_json(root / "E5_topology_ablation/status.json", {}),
            "formal_record_count": sum(len(rows) for rows in experiment_rows.values()),
            "formal_workflow_episodes": len(e0) + len(e1["rows"]) + len(e4["rows"]),
            "total_llm_calls_including_pilot": e1["llm_calls"] + pilot["llm_calls"] + e4["llm_calls"],
            "failed_formal_episodes": sum(c["failed_episodes"] for c in counts.values()),
            "blocked_formal_episodes": sum(c["blocked_episodes"] for c in counts.values()),
            "excluded_formal_episodes": 0}


def generate_reports(root: Path) -> dict[str, Any]:
    root.mkdir(parents=True, exist_ok=True)
    data = collect(root)
    tables = {"table_a_deterministic": data["e0_table"], "table_a_paired": data["e0_pairs"],
              "table_b_llm_agents": data["e1_table"], "table_b_paired": data["e1_pairs"],
              "table_b_actual_audit_storage": data["e1"]["audit_storage_by_defense"],
              "table_b_overall": table_groups(data["e1"]["primary"], ("defense",), ("success", "privacy_safe_success", "raw_exposure", "external_exposure", "intervention_count", "blocks")),
              "table_c_overhead": data["e2_table"], "table_d_semantic_stress": data["e3_table"]}
    if data["e4"]["rows"]:
        tables["table_e_second_model"] = table_groups(data["e4"]["primary"], ("model", "topology", "condition", "defense"), ("success", "privacy_safe_success", "raw_exposure", "external_exposure", "intervention_count"))
    for name, rows in tables.items():
        write_table(root, name, rows)
    cases = failure_cases(root / "E1_llm_agents/formal", data["e1"]["primary"])
    if data["e1"]["rows"]:
        destination = root / "E1_llm_agents/formal"
        save_json(destination / "failure_cases.safe.json", cases)
        with (destination / "failure_cases.safe.csv").open("w", newline="") as handle:
            if cases:
                writer = csv.DictWriter(handle, fieldnames=list(cases[0]), lineterminator="\n")
                writer.writeheader(); writer.writerows(cases)
    # Report data contains counters and derived tables, not duplicate raw trajectories.
    compact = {k: v for k, v in data.items() if k not in {"e0_rows", "manifest"}}
    for name in ("e1", "pilot", "e4"):
        compact[name] = {k: v for k, v in data[name].items() if k not in {"rows", "primary"}}
    compact["e1_failure_cases"] = cases
    pairs = {r["metric"]: r for r in data["e0_pairs"]}
    privacy_tied = bool(pairs) and all(pairs[m]["tie"] == pairs[m]["matched"] and pairs[m]["matched"] > 0 for m in ("success", "raw_exposure", "external_exposure", "exposure_recipient_pairs"))
    conclusion_a = ("PAPC and IFC-SafeView tie on measured task success and privacy in every matched deterministic group; this experiment does not establish an advantage from PAPC-specific mechanisms." if privacy_tied else "The deterministic paired results are descriptive evidence from one enterprise task; interpret the separate privacy, utility, and intervention outcomes without a population claim.")
    extra = pairs.get("intervention_count", {}).get("mean_papc_minus_ifc")
    if extra is not None:
        conclusion_a += f" PAPC minus IFC mean intervention count is {extra:+.6g} per episode."
    llm = data["e1"]
    e1_overall_pairs = {r["metric"]: r for r in data["e1_pairs"] if r["topology"] == "overall"}
    e1_tied = bool(llm["primary"]) and all(e1_overall_pairs[m]["matched"] > 0 and e1_overall_pairs[m]["tie"] == e1_overall_pairs[m]["matched"] for m in ("success", "privacy_safe_success", "raw_exposure", "external_exposure", "exposure_recipient_pairs", "intervention_count", "blocks"))
    exposure_totals = {defense: {key: sum(r.get(key, 0) for r in llm["rows"] if r["defense"] == defense)
                                for key in ("source_raw_exposure", "source_external_exposure", "generated_raw_exposure", "generated_external_exposure")}
                       for defense in sorted({r["defense"] for r in llm["rows"]})}
    compact["e1_observed_exposure_totals"] = exposure_totals
    outcome_counts = [{"defense": defense, "episodes": sum(r["defense"] == defense for r in llm["primary"]),
                       "task_successes": sum(bool(r.get("success")) for r in llm["primary"] if r["defense"] == defense),
                       "privacy_safe_successes": sum(bool(r.get("privacy_safe_success")) for r in llm["primary"] if r["defense"] == defense)}
                      for defense in sorted({r["defense"] for r in llm["primary"]})]
    compact["e1_outcome_counts"] = outcome_counts
    save_json(root / "report_data.json", compact)
    if llm["completed_episodes"]:
        b_conclusion = "The live model generates planner, finance, and writer actions in one parameterized enterprise scenario; the matched table reports observed task-state correctness and exact-value exposure."
    elif llm["llm_calls"]:
        b_conclusion = "Live formal calls were attempted but no complete episode is available; these failures do not establish working three-agent task completion."
    else:
        b_conclusion = "No eligible formal live-LLM outcome is available; wiring fixtures are excluded from model evidence."
    if e1_tied:
        b_conclusion = (f"PAPC and IFC-SafeView tie in all {e1_overall_pairs['success']['matched']} matched groups on task success, privacy-safe success, raw/external exposure, unique exposure pairs, interventions and blocks. The live three-agent slice provides no measured PAPC advantage over equal-capability IFC-SafeView.")
    e3n = data["counts"]["E3"]["episodes"]
    d_conclusion = f"Recipient-history reconstruction detects disclosure in {data['e3_reconstruction_leaks']}/{e3n} probes while canonical exact matching records {data['e3_exact_hits']} exposure events; the evaluated defense does not protect these tested representations." if e3n else "No formal representation probe is available."
    principal_claim = ("Equal-capability runtime mediation contains registered exact-value disclosure in the evaluated enterprise workflow; PAPC-specific mechanisms show no deterministic utility/privacy advantage and do not prevent the tested reconstructable transformations." if privacy_tied and e3n else "Conclusions are limited to the recorded matched runtime measurements; missing formal experiments do not support additional claims.")
    if privacy_tied and e1_tied:
        principal_claim = "Equal-capability runtime mediation contains measured exact-value disclosure in the evaluated scripted and LLM-driven enterprise workflows; PAPC shows no measured advantage over IFC-SafeView in either comparison, and neither defense contains the tested reconstructable transformations."
    headings = [("E0", "Deterministic workflow"), ("E1", "Live intermediate-agent formal"), ("E2", "Timing trials (not tasks)"), ("E3", "Injected representation probes"), ("E4", "Second-model formal")]
    count_table = [{"experiment": f"{name}: {label}", **data["counts"][name]} for name, label in headings]
    lines = ["# AAMAS 2027 experiment summary", "", f"Generated: {datetime.now(timezone.utc).isoformat()}",
             f"Repository start SHA: `{data['manifest'].get('start_head', data['manifest'].get('git_sha', 'UNAVAILABLE'))}`.",
             f"Repository end SHA: `{data['manifest'].get('end_head', 'not yet recorded in MANIFEST.json')}`.",
             f"Branch: `{data['manifest'].get('branch', 'UNAVAILABLE')}`.", "", "## Actual sample sizes", "",
             markdown_table(count_table, [("experiment", "Experiment"), ("episodes", "Records"), ("task_ids", "Task IDs"), ("seeds", "Seeds"), ("failed_episodes", "Failed"), ("blocked_episodes", "Blocked"), ("excluded_episodes", "Excluded")]), "",
             f"Formal records total: {data['formal_record_count']}; actual workflow episodes: {data['formal_workflow_episodes']}. E2 records are timing trials and E3 records are probes; neither is an additional task-completion episode.",
             "E0 has one historical task. E1 has public quote/deadline/status variants of that same scenario, with gold derived from saved task config and the unchanged policy; these are not independent domains. The private cap is nonbinding among the twelve tasks' cheapest deadline-eligible candidates, so this does not test diverse private-budget reasoning or infeasibility handling. E3 reuses ten task labels but a single protected-value domain.", "", "## Experiments and outcomes", "",
             "E0: " + conclusion_a, "",
             f"E1 formal: {llm['status']}; {llm['registered_terminal_episodes']}/{llm['expected_primary_episodes'] if llm['expected_primary_episodes'] is not None else 'unregistered'} registered first-attempt terminal records; {llm['completed_model_episodes']} completed model episodes, {llm['failed_episodes']} failed, {llm['blocked_episodes']} blocked; {llm['episodes']} total attempts and {llm['diagnostic_fixture_rows']} diagnostic fixture rows classified separately. Privacy measurement coverage: {cell(llm['measurement_coverage'])}. Experiment COMPLETE means the full registered matrix reached terminal outcomes, including retained execution failures; it does not mean all task/model outcomes succeeded. " + b_conclusion,
             f"E1 pilot: {data['pilot']['episodes']} live attempts; {data['pilot']['llm_calls']} API calls; {data['pilot']['failed_episodes']} failed / {data['pilot']['blocked_episodes']} blocked episodes. Pilot outcomes never enter the main table.", "",
             "E1 formal first-attempt outcome counts:", "",
             markdown_table(outcome_counts, [("defense", "Defense"), ("episodes", "Episodes"), ("task_successes", "Task successes"), ("privacy_safe_successes", "Privacy-safe successes")]), "",
             f"E2: {data['counts']['E2']['episodes']} trials; {data['e2_timed_events']:,} timed events and {data['e2_warmup_calls']:,} warmup calls. Timing covers mediation dispatch plus timer overhead. Audit storage uses actual serialized EventRecord and intervention PolicyDecisionRecord bytes; 24-event task KiB is a normalized projection, not measured E1 storage. Privacy and utility are not evaluated by E2.", "",
             "E3: " + d_conclusion + " No extra online semantic detector was added. These are deterministic injected write/read probes, not end-to-end model-generated attack episodes; no utility measurement is claimed.", "",
             "E4: " + (f"{data['e4']['status']}; {data['e4']['episodes']} episode attempts, {data['e4']['failed_episodes']} failed, {data['e4']['llm_calls']} API requests and {data['e4']['returned_model_outputs']} returned model outputs. " + str(data['e4_status'].get('reason', 'No model-confirmation claim is supported when no episode completed.')) if data['e4']['rows'] else str(data['e4_status'].get('reason', 'SKIPPED: no completed eligible second-family formal records. Existing profile mappings alone do not establish usable second-model evidence.'))), "",
             "E5: " + str(data["e5_status"].get("reason", "NOT_TRIGGERED: no independently established PAPC advantage with the required topology interaction. Topology retained as environmental risk factor rather than independently validated algorithmic contribution.")), "",
             "## API usage and failures", "",
             f"Total API calls across eligible formal, pilot, and second-model runs: {data['total_llm_calls_including_pilot']}. Formal E1 calls: {llm['llm_calls']}; input/output tokens: {llm['input_tokens']}/{llm['output_tokens']}; failed call attempts: {llm['failed_call_attempts']}; unfinished call attempts: {llm['unfinished_call_attempts']}; linked retry episodes: {llm['linked_retry_episodes']}.",
             f"Requested E1 models: {', '.join(llm['requested_models']) or 'unavailable'}. Returned identifiers: {', '.join(llm['returned_models']) or 'unavailable'}.",
             f"E1 pilot input/output tokens: {data['pilot']['input_tokens']}/{data['pilot']['output_tokens']}. E4 input/output token usage reported by the API: {data['e4']['input_tokens']}/{data['e4']['output_tokens']}; returned model outputs: {data['e4']['returned_model_outputs']}. Zero token counters after HTTP rejection mean no usage record was returned, not a measured model-generation cost of zero.",
             f"E1 execution errors: {json.dumps(llm['error_counts'], sort_keys=True)}. E4 execution errors: {json.dumps(data['e4']['error_counts'], sort_keys=True)}. Error names contain no model response text or credential values.",
             f"Actual formal E1 serialized safe-audit storage: {llm['audit_storage_total_bytes']:,} bytes across eligible episode attempts; per-defense KiB/episode is saved in tables/table_b_actual_audit_storage.csv. This directly measures saved episode/event/call-attempt JSONL and differs from the E2 24-event projection.",
             "First attempts define the primary comparison; linked retries and infrastructure/parser failures remain in raw records and attempt counts. Incomplete privacy/intervention measurements are unavailable in paired comparisons and omitted from measurement means, with privacy_complete_episodes recorded in CSV/JSON; they remain failures in task-success denominators rather than zero-leak wins. No quality-based exclusions are applied.", "",
             "## Failure cases and interpretation", "",
             conclusion_a, b_conclusion, d_conclusion,
             "Source injection exposure and model-generated exposure are separated in Table B. Exogenous source contamination alone is not evidence that an LLM decided to disclose a secret; any recorded generated exposures remain separately reported and must not be omitted.",
             "Observed source/generated exposure totals, including measured-so-far observations from failed episodes: " + json.dumps(exposure_totals, sort_keys=True) + ". Counts are secret-event occurrences for raw exposure, not independent secrets or tasks.",
             "Named safe failure cases: `E1_llm_agents/formal/failure_cases.safe.json` and `.csv`. These preserve every execution/task failure with its run ID, false verifier fields, and failed-call finish reason/token count, while omitting model text.",
             markdown_table(cases, [("task_id", "Task"), ("topology", "Topology"), ("defense", "Defense"), ("status", "Status"), ("error_type", "Error"), ("failed_role", "Role"), ("finish_reason", "Finish"), ("failed_call_output_tokens", "Call output tokens"), ("failed_correctness_fields", "False verifier fields")]),
             "The deterministic final-output checker remains a weak generic template/privacy proxy. E1 additionally checks actual delivered request, valid finance approval, public quote/constraint correctness, final action and permitted abstractions. It is still one synthetic workflow with deterministic tools.",
             "Cascade counters refer to delivered contaminated events in the new adapters, not the old unconditional ancestral node metric. E3 counts reconstructed secret-recipient disclosure. Exact raw exposure, external leaking events, and unique secret-recipient pairs are distinct and are not pooled across experimental scopes.", "",
             "## Supported claim", "", principal_claim, "", "## Claims to drop or downgrade", "",
             "- PAPC superiority over equal-capability IFC-SafeView on deterministic task completion or privacy.",
             "- PAPC superiority over IFC-SafeView in the evaluated live intermediate-agent slice when every matched comparison is tied.",
             "- Independently demonstrated necessity of topology/fanout risk, quarantine, or enforceable propagation leases.",
             "- Semantic confidentiality, transformed-secret robustness, or arbitrary paraphrase protection.",
             "- Broad task/domain diversity or second-family generalization without eligible formal results.",
             "- Treating scripted or dry-run intermediate decisions, source-injected exposures, or repeated seeds as independent model behavior.", "",
             "## Rebuild and provenance", "",
             "All reported tables rebuild from safe episode JSONL and E2 integer latency histograms. Existing summary JSON is not used as the numerical source. Manifest/config registrations retain exact commands and pre-run input hashes. Read `PRIOR_EVIDENCE_AUDIT.md` for unavailable historical trajectories and corrected mediation/evaluation coverage. See `TEST_REPORT.md` or `logs/test_report.json` for passed/failed/skipped/xfail counts."]
    (root / "EXPERIMENT_SUMMARY.md").write_text("\n\n".join(lines) + "\n")
    paper = ["# AAMAS paper integration", "", "Use only the completed rows below. All rates are proportions; exposure/intervention columns are episode means unless stated otherwise.", "", "## Table A — Equal-capability deterministic benchmark", "",
             markdown_table(data["e0_table"], [("defense", "Defense"), ("episodes", "n"), ("success", "Task"), ("privacy_safe_success", "Safe task"), ("raw_exposure", "Raw"), ("external_exposure", "External"), ("exposure_recipient_pairs", "Pairs"), ("intervention_count", "Interventions"), ("blocks", "Blocks")]), "",
             markdown_table(data["e0_pairs"], [("metric", "Paired metric"), ("matched", "Matched"), ("better", "PAPC better"), ("tie", "Tie"), ("worse", "PAPC worse"), ("unavailable", "Unavailable"), ("exact_sign_test_cluster_p", "Task-cluster sign p")]), "",
             "Conclusion: " + conclusion_a,
             "Cannot claim: PAPC superiority or task-population significance; the 90 groups reuse one task and the sign test has at most one independent task cluster.", "", "## Table B — LLM-driven agents", "",
             markdown_table(data["e1_table"], [("topology", "Topology"), ("condition", "Condition"), ("defense", "Defense"), ("episodes", "n"), ("privacy_complete_episodes", "Measured n"), ("failed_or_blocked", "Failed"), ("success", "Task"), ("privacy_safe_success", "Safe task"), ("raw_exposure", "Raw"), ("external_exposure", "External"), ("intervention_count", "Interventions"), ("blocks", "Blocks")]), "",
             "Source versus model-generated exposure (episode means):", "",
             markdown_table(data["e1_table"], [("topology", "Topology"), ("condition", "Condition"), ("defense", "Defense"), ("source_raw_exposure", "Source raw"), ("generated_raw_exposure", "Generated raw"), ("source_external_exposure", "Source external"), ("generated_external_exposure", "Generated external")]), "",
             "Matched PAPC vs IFC-SafeView, by topology/condition and overall:", "",
             markdown_table([r for r in data["e1_pairs"] if r["metric"] in {"success", "privacy_safe_success", "raw_exposure", "intervention_count"}], [("topology", "Topology"), ("condition", "Condition"), ("metric", "Metric"), ("matched", "n"), ("better", "Better"), ("tie", "Tie"), ("worse", "Worse"), ("unavailable", "Unavailable")]), "",
             "Conclusion: " + b_conclusion,
             "Overall first-attempt task outcome counts:", "",
             markdown_table(outcome_counts, [("defense", "Defense"), ("episodes", "Episodes"), ("task_successes", "Task successes"), ("privacy_safe_successes", "Privacy-safe successes")]), "",
             "Observed source/generated exposure totals (all recorded attempts, including partial observations): " + json.dumps(exposure_totals, sort_keys=True) + ". Generated exposures are actual measured model-action disclosures, distinct from injected-source leakage.",
             "Cannot claim: independence across domains, production multi-agent robustness, or LLM-caused leakage from source injection counts. The private cap is nonbinding among the twelve selected tasks' cheapest deadline-eligible quotes. Formal primary rows use first attempts; pilot and wiring fixtures are separate.", "",
             "Actual E1 serialized safe-audit storage (episodes, events, and call attempts):", "",
             markdown_table(llm["audit_storage_by_defense"], [("defense", "Defense"), ("episodes", "Attempts"), ("audit_bytes", "Total bytes"), ("audit_kib_per_episode", "KiB/episode")]), "",
             "This includes real stored call-start and call-completion records and excludes private full prompts/responses; it is separate from the E2 standard-schema projection.", "", "## Table C — Mediation latency and serialized storage", "",
             markdown_table(data["e2_table"], [("defense", "Mode"), ("event_count", "Events/trial"), ("trials", "Trials"), ("p50_us", "p50 µs"), ("p95_us", "p95 µs"), ("p99_us", "p99 µs"), ("mean_us", "Mean µs"), ("throughput_events_per_second", "Events/s"), ("audit_bytes_per_event", "Bytes/event"), ("audit_kib_per_task", "KiB/24 events")]), "",
             "Conclusion: The measured Python mediator has microsecond-scale per-event cost on this host and event mix; actual audit serialization grows approximately linearly over the measured sizes.",
             "Cannot claim: production throughput, provider latency improvements, or measured E1 storage. Timing includes dispatch/timer overhead, excludes model calls, and storage reflects redacted audit schemas with policy records for interventions.", "", "## Table D — Tested representation transformations", "",
             markdown_table(data["e3_table"], [("transformation", "Transformation"), ("defense", "Defense"), ("trials", "Probes"), ("leaked_episodes", "Reconstruction leaks"), ("leakage_rate", "Leak rate"), ("exact_string_exposure_events", "Exact-string hits"), ("interventions", "Interventions")]), "",
             "Conclusion: " + d_conclusion,
             "Cannot claim: semantic confidentiality or ten independent private-value domains. These ten scenario labels share one underlying secret; no task utility or model attack-generation success was measured."]
    if data["e4"]["rows"]:
        e4_conclusion = ("The second-model API execution is blocked; failed attempts supply no model confirmation or measured privacy outcome." if not data["e4"]["completed_episodes"] else "This table reports only the recorded second-model slice.")
        paper += ["", "## Table E — Second-model confirmation attempts", "", markdown_table(tables["table_e_second_model"], [("model", "Model"), ("defense", "Defense"), ("episodes", "Attempts"), ("failed_or_blocked", "Failed"), ("privacy_complete_episodes", "Measured n"), ("success", "Task incl. failure"), ("privacy_safe_success", "Safe task incl. failure"), ("raw_exposure", "Raw"), ("external_exposure", "External")]), "Conclusion: " + e4_conclusion, "Cannot claim: model-family generalization, equivalent privacy, or a successful confirmation from unavailable model outputs."]
    paper += ["", "## Topology interpretation", "", "Topology retained as environmental risk factor rather than independently validated algorithmic contribution.", "", "## Proposed main claim", "", principal_claim]
    (root / "PAPER_INTEGRATION.md").write_text("\n\n".join(paper) + "\n")
    (root / "README.md").write_text("""# AAMAS 2027 experiment artifact

Start with `EXPERIMENT_SUMMARY.md`, `PAPER_INTEGRATION.md`, `MANIFEST.json`, and `PRIOR_EVIDENCE_AUDIT.md`. Tables are CSV/JSON; raw records are safe JSONL with text omitted. E0/E1 are workflow episodes, E2 rows are timing trials, and E3 rows are injected representation probes. Do not pool their utility/privacy metrics.

From the extracted bundle root (Python 3.10+; experiment/report execution uses the standard library, tests additionally require pytest>=7.0):

```bash
PYTHONPATH=. python scripts/package_aamas2027.py --reports-only
PYTHONPATH=. python -m pytest tests/test_aamas_*.py
PYTHONPATH=. python scripts/run_aamas_equal.py --help
PYTHONPATH=. python scripts/run_aamas_llm_agents.py --help
PYTHONPATH=. python scripts/run_aamas_stress.py --help
```

Exact original experiment commands and generation settings are in MANIFEST/config registrations. Use a new output directory to rerun; historical/formal outputs must not be overwritten. MiniMax live runs require credentials supplied through the environment, never committed files. Dry-run fixtures only verify wiring and are not model evidence. Reports use first-attempt formal LLM rows, retain failed/blocked/linked retry attempts, and keep pilot separate.

Bundle inclusion uses explicit source/config file names and safe artifact basename rules. It contains only AAMAS experiment dependencies, configs, source, tests, text-free episode/event/call records, latency histograms, summaries, tables, logs, manifest, and reports. Historical archives, raw model prompts/responses, private credentials, environment files, caches, and virtual environments are excluded. Public synthetic protected-value fixtures intentionally occur in executable policy/attack/test/data source so replay works; this is distinct from safe result records, which are scanned for those registered raw values before packaging. No assertion is made that executable source contains no synthetic fixture values.

Source-versus-generated exposure counters separate exogenous injected material from LLM-generated actions. Original WINE summaries are audit references only and are not bundled; the attack-ranking rows and relevant history are preserved in `prior_evidence_inventory.json` and `PRIOR_EVIDENCE_AUDIT.md`.
""")
    return compact


def allowed_artifact(relative: Path) -> bool:
    parts = relative.parts
    if any(p.startswith(".") or p in {"private", "__pycache__", "venv", "full", "raw_private"} for p in parts):
        return False
    if len(parts) == 1:
        return parts[0] in ROOT_REPORTS
    if len(parts) == 2 and parts[0] == "tables":
        return bool(TABLE_NAME.fullmatch(parts[1]))
    if len(parts) == 2 and parts[0] == "logs":
        return bool(LOG_NAME.fullmatch(parts[1]))
    if parts[0] in EXPERIMENT_DIRS:
        if len(parts) == 2:
            return parts[1] in {"README.md", "status.json", "E1_INDEPENDENT_REVIEW.md"}
        if len(parts) == 3 and parts[1] in {"formal", "pilot"}:
            return parts[2] in RUN_FILES
    return False


def bundle_files(repo: Path, artifact_root: Path) -> list[Path]:
    files = [repo / name for name in SOURCE_FILES if (repo / name).is_file()]
    files += [repo / "configs/experiment/aamas2027" / name for name in CONFIG_FILES if (repo / "configs/experiment/aamas2027" / name).is_file()]
    files += [p for p in artifact_root.rglob("*") if p.is_file() and allowed_artifact(p.relative_to(artifact_root))]
    for path in files:
        if path.is_symlink() or not path.resolve().is_relative_to(repo.resolve()):
            raise ValueError("Bundle member escaped repository or is a symlink")
    return sorted(set(files))


def validate_safe_artifacts(files: list[Path], artifact_root: Path) -> None:
    raw = [p.raw_value for p in default_secret_policies()]
    credentials = re.compile(r"(?:Bearer [A-Za-z0-9_\-]{20,}|AKIA[0-9A-Z]{16}|sk-(?!internal-demo-token)[A-Za-z0-9_\-]{24,})")
    for path in files:
        text = path.read_text()
        if path.is_relative_to(artifact_root) and any(value in text for value in raw):
            raise ValueError(f"Registered raw protected value in shareable artifact: {path.name}")
        if credentials.search(text):
            raise ValueError(f"Credential-like material in candidate bundle member: {path.name}")


def build_bundle(repo: Path, artifact_root: Path, output: Path) -> dict[str, Any]:
    if not (artifact_root / "MANIFEST.json").is_file():
        raise ValueError("Final MANIFEST.json is required before bundling")
    if not (artifact_root / "TEST_REPORT.md").is_file() and not (artifact_root / "logs/test_report.json").is_file():
        raise ValueError("TEST_REPORT.md or logs/test_report.json is required before bundling")
    files = [p for p in bundle_files(repo, artifact_root) if p.name != "BUNDLE_MANIFEST.json"]
    validate_safe_artifacts(files, artifact_root)
    inventory = {"created_at": datetime.now(timezone.utc).isoformat(), "bundle_name": output.name,
                 "files": [{"path": str(p.relative_to(repo)), "bytes": p.stat().st_size} for p in files],
                 "synthetic_fixture_policy": "Registered synthetic values are permitted in executable public source/config/data, but absent from scanned shareable results.",
                 "excluded_by_design": ["historical archives", "private full prompts/responses", ".env and credentials", "cache/virtualenv", "unlisted artifacts"]}
    save_json(artifact_root / "BUNDLE_MANIFEST.json", inventory)
    files.append(artifact_root / "BUNDLE_MANIFEST.json")
    validate_safe_artifacts([artifact_root / "BUNDLE_MANIFEST.json"], artifact_root)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in sorted(files):
            archive.write(path, str(path.relative_to(repo)))
    return {"bundle": str(output), "files": len(files), "compressed_bytes": output.stat().st_size}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--artifact-root", type=Path, default=Path("artifacts/aamas2027"))
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--reports-only", action="store_true", help="Rebuild paper tables/reports without creating a ZIP")
    mode.add_argument("--bundle", action="store_true", help="Rebuild reports and package safe allowlisted files")
    parser.add_argument("--output", type=Path, help="Default: aamas2027_experiment_bundle_20260912.zip in repo root")
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    root = args.artifact_root if args.artifact_root.is_absolute() else repo / args.artifact_root
    report = generate_reports(root)
    result = {"formal_records": report["formal_record_count"], "formal_workflow_episodes": report["formal_workflow_episodes"],
              "llm_calls_including_pilot": report["total_llm_calls_including_pilot"], "reports": str(root)}
    if args.bundle:
        output = args.output or repo / "aamas2027_experiment_bundle_20260912.zip"
        result.update(build_bundle(repo, root, output))
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
