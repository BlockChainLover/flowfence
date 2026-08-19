#!/usr/bin/env python3
"""Build the isolated WINE rebuttal no-API evidence package."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import statistics
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


VARIANT_LABELS = {
    "flowfence_lite_nonoracle": "FULL",
    "flowfence_lite_nonoracle_no_semantic_patterns": "NO_SEMANTIC_PATTERNS",
    "flowfence_lite_nonoracle_no_safe_view": "NO_SAFE_VIEW",
    "flowfence_lite_nonoracle_no_topology_fanout": "NO_TOPOLOGY_FANOUT",
    "flowfence_lite_nonoracle_no_propagation_right_narrowing": "NO_PROPAGATION_RIGHT_NARROWING",
}
DEFENSE_LABELS = {
    "static_acl": "STATIC_ACL",
    "prompt_filter": "PROMPT_FILTER",
    "acl_content_runtime": "ACL_CONTENT_RUNTIME",
    "flowfence_lite_nonoracle": "FLOWFENCE_NONORACLE",
}
NEW_ABLATIONS = {
    "flowfence_lite_nonoracle_no_safe_view",
    "flowfence_lite_nonoracle_no_topology_fanout",
    "flowfence_lite_nonoracle_no_propagation_right_narrowing",
}
METRICS = (
    "task_success",
    "unauthorized_raw_leakage",
    "external_leakage",
    "cascade_size",
    "cascade_depth",
    "privilege_reach",
    "safe_view_count",
    "quarantine_count",
    "block_count",
    "allow_count",
    "propagation_right_downgrade_count",
    "oracle_annotation_use_count",
    "provider_call_count",
    "acl_block_count",
    "runtime_content_block_count",
    "final_content_block_count",
)
LOWER_IS_BETTER = {
    "unauthorized_raw_leakage",
    "external_leakage",
    "cascade_size",
    "cascade_depth",
    "privilege_reach",
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def numeric(value: Any) -> float:
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    if isinstance(value, (int, float)):
        return float(value)
    return 0.0


def find_runs(root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for metrics_path in sorted(root.rglob("metrics.json")):
        run_dir = metrics_path.parent
        metrics = read_json(metrics_path)
        meta = read_json(run_dir / "meta.json")
        rows.append(
            {
                "run_dir": run_dir,
                "run_id": str(meta["run_id"]),
                "topology": str(meta["topology"]),
                "attack": "none" if str(meta["attack"]) == "base" else str(meta["attack"]),
                "seed": int(meta["seed"]),
                "defense": str(meta["defense"]),
                "provider_calls_enabled": bool(meta["provider_calls_enabled"]),
                "agent_backend": str(meta["agent_backend"]),
                "metrics": metrics,
            }
        )
    return rows


def metric(row: dict[str, Any], key: str) -> float:
    return numeric(row["metrics"].get(key))


def mean(rows: list[dict[str, Any]], key: str) -> float:
    return round(statistics.fmean(metric(row, key) for row in rows), 6) if rows else 0.0


def aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "runs": len(rows),
        "task_success_rate": mean(rows, "task_success"),
        "raw_leakage_mean": mean(rows, "unauthorized_raw_leakage"),
        "external_leakage_mean": mean(rows, "external_leakage"),
        "cascade_size_mean": mean(rows, "cascade_size"),
        "cascade_depth_mean": mean(rows, "cascade_depth"),
        "privilege_reach_mean": mean(rows, "privilege_reach"),
        "safe_view_mean": mean(rows, "safe_view_count"),
        "quarantine_mean": mean(rows, "quarantine_count"),
        "block_mean": mean(rows, "block_count"),
        "allow_mean": mean(rows, "allow_count"),
        "propagation_right_downgrade_mean": mean(rows, "propagation_right_downgrade_count"),
        "acl_block_mean": mean(rows, "acl_block_count"),
        "runtime_content_block_mean": mean(rows, "runtime_content_block_count"),
        "final_content_block_mean": mean(rows, "final_content_block_count"),
        "oracle_annotation_use_count": int(sum(metric(row, "oracle_annotation_use_count") for row in rows)),
        "provider_call_count": int(sum(metric(row, "provider_call_count") for row in rows)),
    }


def group_rows(rows: list[dict[str, Any]], keys: tuple[str, ...]) -> list[dict[str, Any]]:
    groups: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[tuple(row[key] for key in keys)].append(row)
    output: list[dict[str, Any]] = []
    for values, grouped in sorted(groups.items()):
        item = {key: value for key, value in zip(keys, values)}
        item.update(aggregate(grouped))
        output.append(item)
    return output


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if columns is None:
        columns = list(rows[0]) if rows else []
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def per_run_row(row: dict[str, Any], label_key: str, label: str) -> dict[str, Any]:
    out = {
        "run_id": row["run_id"],
        "topology": row["topology"],
        "attack": row["attack"],
        "seed": row["seed"],
        label_key: label,
    }
    out.update({key: row["metrics"].get(key, 0) for key in METRICS})
    return out


def interpretation(metric_name: str, full: float, ablated: float) -> str:
    if abs(full - ablated) <= 1e-9:
        return "unchanged"
    if metric_name == "task_success_rate":
        return "improved" if ablated > full else "degraded"
    if metric_name.endswith("_mean") and any(
        token in metric_name for token in ("leakage", "cascade", "privilege")
    ):
        return "improved" if ablated < full else "degraded"
    return "mixed"


def failure_rows(rows: list[dict[str, Any]], label_key: str, labels: dict[str, str]) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    for row in rows:
        reasons = []
        if metric(row, "task_success") == 0:
            reasons.append("task_failure")
        if metric(row, "unauthorized_raw_leakage") > 0:
            reasons.append("raw_leakage")
        if metric(row, "external_leakage") > 0:
            reasons.append("external_leakage")
        if not reasons:
            continue
        failures.append(
            {
                "run_id": row["run_id"],
                "topology": row["topology"],
                "attack": row["attack"],
                "seed": row["seed"],
                label_key: labels[row["defense"]],
                "failure_types": reasons,
                "task_success": bool(metric(row, "task_success")),
                "unauthorized_raw_leakage": metric(row, "unauthorized_raw_leakage"),
                "external_leakage": metric(row, "external_leakage"),
                "source_metrics": str(row["run_dir"] / "metrics.json"),
            }
        )
    return failures


def copy_per_run(rows: list[dict[str, Any]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for row in rows:
        payload = {
            "meta": {
                "run_id": row["run_id"],
                "topology": row["topology"],
                "attack": row["attack"],
                "seed": row["seed"],
                "defense": row["defense"],
                "agent_backend": row["agent_backend"],
                "provider_calls_enabled": row["provider_calls_enabled"],
                "remote_run_dir": str(row["run_dir"]),
            },
            "metrics": row["metrics"],
        }
        (output_dir / f"{row['run_id']}.json").write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )


def keyed(rows: list[dict[str, Any]]) -> dict[tuple[str, str, int, str], dict[str, Any]]:
    return {(row["topology"], row["attack"], row["seed"], row["defense"]): row for row in rows}


def export_safe_trace_case(
    *,
    case_id: str,
    title: str,
    left: dict[str, Any],
    right: dict[str, Any],
    output_dir: Path,
    note: str,
) -> dict[str, Any]:
    def safe_events(row: dict[str, Any]) -> list[dict[str, Any]]:
        path = row["run_dir"] / "events.safe.jsonl"
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

    payload = {
        "case_id": case_id,
        "title": title,
        "note": note,
        "left": {
            "run_id": left["run_id"],
            "defense": left["defense"],
            "source_raw_trace_path": str(left["run_dir"] / "events.full.jsonl"),
            "metrics": {key: left["metrics"].get(key, 0) for key in METRICS},
            "redacted_events": safe_events(left),
        },
        "right": {
            "run_id": right["run_id"],
            "defense": right["defense"],
            "source_raw_trace_path": str(right["run_dir"] / "events.full.jsonl"),
            "metrics": {key: right["metrics"].get(key, 0) for key in METRICS},
            "redacted_events": safe_events(right),
        },
    }
    path = output_dir / f"{case_id}.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {"case_id": case_id, "title": title, "file": path.name, "note": note}


def component_outputs(rows: list[dict[str, Any]], output: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    summaries = output / "summaries"
    safe_dir = output / "safe_traces"
    safe_dir.mkdir(parents=True, exist_ok=True)
    copy_per_run(rows, output / "per_run")
    per_run = [per_run_row(row, "variant", VARIANT_LABELS[row["defense"]]) for row in rows]
    write_csv(summaries / "per_run_results.csv", per_run)

    labeled = [{**row, "variant": VARIANT_LABELS[row["defense"]]} for row in rows]
    by_variant = group_rows(labeled, ("variant",))
    by_variant.sort(key=lambda item: list(VARIANT_LABELS.values()).index(item["variant"]))
    write_csv(summaries / "summary_by_variant.csv", by_variant)
    write_csv(summaries / "summary_by_variant_topology.csv", group_rows(labeled, ("variant", "topology")))
    write_csv(summaries / "summary_by_variant_attack.csv", group_rows(labeled, ("variant", "attack")))
    write_jsonl(summaries / "failure_breakdown.jsonl", failure_rows(rows, "variant", VARIANT_LABELS))

    full = next(item for item in by_variant if item["variant"] == "FULL")
    delta_metrics = (
        "task_success_rate",
        "raw_leakage_mean",
        "external_leakage_mean",
        "cascade_size_mean",
        "cascade_depth_mean",
        "privilege_reach_mean",
        "safe_view_mean",
        "quarantine_mean",
        "block_mean",
        "propagation_right_downgrade_mean",
    )
    deltas: list[dict[str, Any]] = []
    for item in by_variant:
        if item["variant"] == "FULL":
            continue
        for metric_name in delta_metrics:
            full_value = numeric(full[metric_name])
            ablated_value = numeric(item[metric_name])
            deltas.append(
                {
                    "variant": item["variant"],
                    "metric": metric_name,
                    "full_value": full_value,
                    "ablated_value": ablated_value,
                    "absolute_delta": round(ablated_value - full_value, 6),
                    "relative_delta_if_defined": (
                        round((ablated_value - full_value) / abs(full_value), 6) if full_value else ""
                    ),
                    "interpretation": interpretation(metric_name, full_value, ablated_value),
                }
            )
    write_csv(summaries / "ablation_delta_vs_full.csv", deltas)

    lookup = keyed(rows)
    case_specs = [
        (
            "case_01_no_safe_view",
            "FULL vs NO_SAFE_VIEW",
            "blackboard_4",
            "summary_poisoning_indirect",
            "flowfence_lite_nonoracle_no_safe_view",
            "The current deterministic task shows equal privacy and task-success outcomes; this is a neutral utility ablation.",
        ),
        (
            "case_02_semantic_summary",
            "FULL vs NO_SEMANTIC_PATTERNS on summary poisoning",
            "chain_4",
            "summary_poisoning_indirect",
            "flowfence_lite_nonoracle_no_semantic_patterns",
            "Semantic patterns change containment for this attack family.",
        ),
        (
            "case_03_semantic_workspace",
            "FULL vs NO_SEMANTIC_PATTERNS on held-out workspace paraphrase",
            "blackboard_4",
            "workspace_poisoning_paraphrase",
            "flowfence_lite_nonoracle_no_semantic_patterns",
            "Held-out surface wording exposes the semantic-pattern dependency.",
        ),
        (
            "case_04_topology_fanout",
            "FULL vs NO_TOPOLOGY_FANOUT",
            "blackboard_4",
            "none",
            "flowfence_lite_nonoracle_no_topology_fanout",
            "Outcome metrics are neutral; the trace records whether the fanout-only risk signal changed the decision.",
        ),
        (
            "case_05_propagation_right",
            "FULL vs NO_PROPAGATION_RIGHT_NARROWING",
            "blackboard_4",
            "none",
            "flowfence_lite_nonoracle_no_propagation_right_narrowing",
            "Outcome metrics are neutral because lease narrowing is metadata-only in this runtime.",
        ),
    ]
    cases = []
    for case_id, title, topology, attack, right_defense, note in case_specs:
        left = lookup[(topology, attack, 1, "flowfence_lite_nonoracle")]
        right = lookup[(topology, attack, 1, right_defense)]
        cases.append(
            export_safe_trace_case(
                case_id=case_id, title=title, left=left, right=right, output_dir=safe_dir, note=note
            )
        )
    (safe_dir / "README.md").write_text(
        "# Component Ablation Safe Traces\n\n"
        "These files contain only redacted deterministic event previews plus metrics and source raw-trace paths.\n\n"
        + "\n".join(f"- `{case['file']}`: {case['note']}" for case in cases)
        + "\n",
        encoding="utf-8",
    )

    new_rows = [row for row in rows if row["defense"] in NEW_ABLATIONS]
    audit = {
        "all_rows": len(rows),
        "new_expected": 270,
        "new_completed": len(new_rows),
        "new_failed": 270 - len(new_rows),
        "reference_refresh_rows": len(rows) - len(new_rows),
        "provider_call_count": int(sum(metric(row, "provider_call_count") for row in rows)),
        "oracle_annotation_use_count": int(sum(metric(row, "oracle_annotation_use_count") for row in rows)),
    }
    return by_variant, audit


def relation(flowfence: float, composite: float, *, lower_is_better: bool) -> str:
    if abs(flowfence - composite) <= 1e-9:
        return "tie"
    if lower_is_better:
        return "flowfence_better" if flowfence < composite else "composite_better"
    return "flowfence_better" if flowfence > composite else "composite_better"


def composite_outputs(
    composite_rows: list[dict[str, Any]], reference_rows: list[dict[str, Any]], full_rows: list[dict[str, Any]], output: Path
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    all_rows = reference_rows + composite_rows + full_rows
    summaries = output / "summaries"
    copy_per_run(composite_rows + reference_rows, output / "per_run")
    per_run = [per_run_row(row, "defense", DEFENSE_LABELS[row["defense"]]) for row in all_rows]
    write_csv(summaries / "per_run_results.csv", per_run)
    labeled = [{**row, "defense_label": DEFENSE_LABELS[row["defense"]]} for row in all_rows]
    by_defense = group_rows(labeled, ("defense_label",))
    order = list(DEFENSE_LABELS.values())
    by_defense.sort(key=lambda item: order.index(item["defense_label"]))
    write_csv(summaries / "comparison_by_defense.csv", by_defense)
    write_csv(summaries / "comparison_by_topology.csv", group_rows(labeled, ("defense_label", "topology")))
    write_csv(summaries / "comparison_by_attack.csv", group_rows(labeled, ("defense_label", "attack")))
    write_jsonl(summaries / "failure_breakdown.jsonl", failure_rows(all_rows, "defense", DEFENSE_LABELS))

    clean = []
    for item in group_rows([row for row in labeled if row["attack"] == "none"], ("defense_label",)):
        defense_rows = [row for row in labeled if row["defense_label"] == item["defense_label"] and row["attack"] == "none"]
        item["clean_task_success_rate"] = item["task_success_rate"]
        item["clean_block_rate"] = round(
            sum(metric(row, "block_count") > 0 or metric(row, "quarantine_count") > 0 for row in defense_rows)
            / len(defense_rows),
            6,
        )
        clean.append(item)
    write_csv(summaries / "clean_behavior.csv", clean)

    comp_lookup = keyed(composite_rows)
    full_lookup = keyed(full_rows)
    matched: list[dict[str, Any]] = []
    for topology, attack, seed, _ in sorted(comp_lookup):
        comp = comp_lookup[(topology, attack, seed, "acl_content_runtime")]
        ff = full_lookup[(topology, attack, seed, "flowfence_lite_nonoracle")]
        matched.append(
            {
                "topology": topology,
                "attack": attack,
                "seed": seed,
                "composite_task_success": int(metric(comp, "task_success")),
                "flowfence_task_success": int(metric(ff, "task_success")),
                "composite_raw_leak": metric(comp, "unauthorized_raw_leakage"),
                "flowfence_raw_leak": metric(ff, "unauthorized_raw_leakage"),
                "composite_external_leak": metric(comp, "external_leakage"),
                "flowfence_external_leak": metric(ff, "external_leakage"),
                "composite_cascade_size": metric(comp, "cascade_size"),
                "flowfence_cascade_size": metric(ff, "cascade_size"),
                "composite_privilege_reach": metric(comp, "privilege_reach"),
                "flowfence_privilege_reach": metric(ff, "privilege_reach"),
                "raw_relation": relation(
                    metric(ff, "unauthorized_raw_leakage"), metric(comp, "unauthorized_raw_leakage"), lower_is_better=True
                ),
                "external_relation": relation(
                    metric(ff, "external_leakage"), metric(comp, "external_leakage"), lower_is_better=True
                ),
                "task_relation": relation(metric(ff, "task_success"), metric(comp, "task_success"), lower_is_better=False),
            }
        )
    write_csv(summaries / "matched_flowfence_vs_composite.csv", matched)
    relation_counts = {
        key: {value: sum(row[key] == value for row in matched) for value in ("flowfence_better", "tie", "composite_better")}
        for key in ("raw_relation", "external_relation", "task_relation")
    }
    audit = {
        "new_expected": 90,
        "new_completed": len(composite_rows),
        "new_failed": 90 - len(composite_rows),
        "reference_refresh_rows": len(reference_rows),
        "matched_rows": len(matched),
        "provider_call_count": int(sum(metric(row, "provider_call_count") for row in all_rows)),
        "oracle_annotation_use_count": int(sum(metric(row, "oracle_annotation_use_count") for row in all_rows)),
        "relation_counts": relation_counts,
    }
    return by_defense, matched, audit


def directory_size(path: Path) -> int:
    return sum(item.stat().st_size for item in path.rglob("*") if item.is_file())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--component-runs-root", required=True, type=Path)
    parser.add_argument("--composite-runs-root", required=True, type=Path)
    parser.add_argument("--reference-runs-root", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--local-repo-root", required=True)
    parser.add_argument("--local-result-root", required=True)
    parser.add_argument("--remote-repo-root", required=True)
    parser.add_argument("--remote-workspace", required=True)
    parser.add_argument("--remote-output-root", required=True)
    parser.add_argument("--git-head", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    component_rows = find_runs(args.component_runs_root)
    composite_rows = find_runs(args.composite_runs_root)
    reference_rows = find_runs(args.reference_runs_root)
    full_rows = [row for row in component_rows if row["defense"] == "flowfence_lite_nonoracle"]
    output = args.output_root
    for directory in (
        output / "environment",
        output / "00_remote_inputs",
        output / "01_component_ablation" / "configs",
        output / "01_component_ablation" / "logs",
        output / "02_composite_baseline" / "configs",
        output / "02_composite_baseline" / "logs",
        output / "02_composite_baseline" / "safe_traces",
        output / "03_rebuttal_evidence",
    ):
        directory.mkdir(parents=True, exist_ok=True)

    config_copies = {
        "01_component_ablation/configs/mas_rebuttal_noapi_component_ablation.yaml": "configs/experiment/mas_rebuttal_noapi_component_ablation.yaml",
        "01_component_ablation/configs/mas_rebuttal_noapi_component_ablation_pilot.yaml": "configs/experiment/mas_rebuttal_noapi_component_ablation_pilot.yaml",
        "02_composite_baseline/configs/mas_rebuttal_noapi_composite_baseline.yaml": "configs/experiment/mas_rebuttal_noapi_composite_baseline.yaml",
        "02_composite_baseline/configs/mas_rebuttal_noapi_composite_pilot.yaml": "configs/experiment/mas_rebuttal_noapi_composite_pilot.yaml",
        "02_composite_baseline/configs/mas_rebuttal_noapi_composite_reference_refresh.yaml": "configs/experiment/mas_rebuttal_noapi_composite_reference_refresh.yaml",
    }
    for destination, source in config_copies.items():
        shutil.copy2(source, output / destination)

    a_summary, a_audit = component_outputs(component_rows, output / "01_component_ablation")
    b_summary, matched, b_audit = composite_outputs(
        composite_rows, reference_rows, full_rows, output / "02_composite_baseline"
    )

    expected_defenses = set(DEFENSE_LABELS)
    if len(component_rows) != 450 or len(full_rows) != 90:
        raise SystemExit(f"component schema-refresh matrix incomplete: rows={len(component_rows)} full={len(full_rows)}")
    if len(composite_rows) != 90 or len(reference_rows) != 180:
        raise SystemExit(
            f"composite matrix incomplete: composite={len(composite_rows)} references={len(reference_rows)}"
        )
    if {row["defense"] for row in reference_rows + composite_rows + full_rows} != expected_defenses:
        raise SystemExit("composite matched defense set mismatch")
    if a_audit["provider_call_count"] or b_audit["provider_call_count"]:
        raise SystemExit("provider_call_count is non-zero")
    if a_audit["oracle_annotation_use_count"] or b_audit["oracle_annotation_use_count"]:
        raise SystemExit("oracle_annotation_use_count is non-zero")
    if any(row["provider_calls_enabled"] for row in component_rows + composite_rows + reference_rows):
        raise SystemExit("provider_calls_enabled=true found in a no-API run")

    table_a = [
        {
            "variant": item["variant"],
            "runs": item["runs"],
            "task_success_rate": item["task_success_rate"],
            "raw_leakage_mean": item["raw_leakage_mean"],
            "external_leakage_mean": item["external_leakage_mean"],
            "cascade_size_mean": item["cascade_size_mean"],
            "cascade_depth_mean": item["cascade_depth_mean"],
            "privilege_reach_mean": item["privilege_reach_mean"],
        }
        for item in a_summary
    ]
    table_b = [
        {
            "defense": item["defense_label"],
            "runs": item["runs"],
            "task_success_rate": item["task_success_rate"],
            "raw_leakage_mean": item["raw_leakage_mean"],
            "external_leakage_mean": item["external_leakage_mean"],
            "cascade_size_mean": item["cascade_size_mean"],
            "cascade_depth_mean": item["cascade_depth_mean"],
            "privilege_reach_mean": item["privilege_reach_mean"],
        }
        for item in b_summary
    ]
    evidence = output / "03_rebuttal_evidence"
    write_csv(evidence / "experiment_A_main_table.csv", table_a)
    write_csv(evidence / "experiment_B_main_table.csv", table_b)

    key_findings = {
        "schema_version": "wine2026_rebuttal_noapi_key_findings_v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "experiment_A": a_audit,
        "experiment_B": b_audit,
        "table_A": table_a,
        "table_B": table_b,
        "integrity_notes": [
            "All new and schema-refresh runs used scripted_deterministic with provider calls disabled.",
            "Propagation-right narrowing is metadata-only in the evaluated runtime.",
            "Deterministic task success is a rule/template check, not semantic-quality evaluation.",
        ],
    }
    (evidence / "key_findings.json").write_text(
        json.dumps(key_findings, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    table_a_lines = [
        f"- {row['variant']}: task={row['task_success_rate']}, raw={row['raw_leakage_mean']}, external={row['external_leakage_mean']}, cascade={row['cascade_size_mean']}/{row['cascade_depth_mean']}, privilege={row['privilege_reach_mean']}"
        for row in table_a
    ]
    table_b_lines = [
        f"- {row['defense']}: task={row['task_success_rate']}, raw={row['raw_leakage_mean']}, external={row['external_leakage_mean']}, cascade={row['cascade_size_mean']}/{row['cascade_depth_mean']}, privilege={row['privilege_reach_mean']}"
        for row in table_b
    ]
    rc = b_audit["relation_counts"]
    evidence_summary = f"""# WINE 2026 Rebuttal - No-API Supplemental Evidence

## Experiment A: Component Ablation

### Setup

The matched non-oracle deterministic matrix uses 3 topologies, 10 attacks, and 3 seeds. FULL and NO_SEMANTIC_PATTERNS were schema-refreshed because historical raw per-run traces were no longer present remotely; the three new variants account for 270 new runs. Thresholds, attacks, topology definitions, policy, and seeds were unchanged.

### Main results

{chr(10).join(table_a_lines)}

### What the data support

The table measures each component's association with exact raw leakage, external leakage, deterministic cascade, privilege reach, and rule-based task completion in this synthetic runtime.

### What the data do NOT support

These results do not establish semantic utility, production robustness, provider generalization, or capability enforcement by propagation-right metadata.

## Experiment B: Composite Defense Baseline

### Baseline definition

ACL_CONTENT_RUNTIME combines the existing Static ACL rule with the existing direct prompt-filter surface rule at runtime transitions and final/external transitions. It blocks on a match and uses no provenance, fanout, privilege-risk score, safe-view, quarantine store, lease narrowing, PAPC risk fusion, or evaluator labels.

### Main results

{chr(10).join(table_b_lines)}

### Matched comparison against FlowFence

- Raw: FlowFence better {rc['raw_relation']['flowfence_better']} / tie {rc['raw_relation']['tie']} / worse {rc['raw_relation']['composite_better']}
- External: FlowFence better {rc['external_relation']['flowfence_better']} / tie {rc['external_relation']['tie']} / worse {rc['external_relation']['composite_better']}
- Task: FlowFence better {rc['task_relation']['flowfence_better']} / tie {rc['task_relation']['tie']} / worse {rc['task_relation']['composite_better']}

### What the data support

The matched counts characterize this explicit defense-in-depth comparator on the same deterministic topology-attack-seed groups.

### What the data do NOT support

The clean-case block rate is only a deterministic blocking proxy. It is not a semantic utility or user-quality judgment.

## Unexpected / Negative Results

- NO_SAFE_VIEW is reported even if task success remains unchanged; the current scripted final writer can preserve the fixed safe template after blocking, so this benchmark may not expose safe-view's utility benefit.
- NO_TOPOLOGY_FANOUT is reported as neutral if exact-policy and semantic signals already dominate the unchanged threshold.
- NO_PROPAGATION_RIGHT_NARROWING is expected to be outcome-neutral because lease signals are metadata-only and do not gate downstream execution in this implementation.
- Any composite wins or ties remain visible in the matched CSV and counts above.

## Candidate numbers for rebuttal

Use only the values in the two main tables and matched counts above, with the deterministic-runtime caveat. Human review is required before citing them; this script does not modify the paper.
"""
    (evidence / "rebuttal_evidence_summary.md").write_text(evidence_summary, encoding="utf-8")

    (output / "01_component_ablation" / "README.md").write_text(
        "# Experiment A - Mechanism Component Ablation\n\n"
        "FULL is `flowfence_lite_nonoracle`. NO_SEMANTIC_PATTERNS disables all configured semantic request patterns. "
        "NO_SAFE_VIEW converts would-be safe-view rewrites to block and uses a quarantine marker rather than raw allow. "
        "NO_TOPOLOGY_FANOUT zeros only shared-workspace/shared-memory fanout risk features without threshold changes. "
        "NO_PROPAGATION_RIGHT_NARROWING keeps content decisions but removes lease revoke/downgrade signals; the low-risk "
        "downgrade-only branch becomes allow. Lease signals are metadata-only in this runtime.\n\n"
        f"New runs: {a_audit['new_completed']}/270; failures: {a_audit['new_failed']}. Reference schema-refresh runs: {a_audit['reference_refresh_rows']}.\n",
        encoding="utf-8",
    )
    (output / "02_composite_baseline" / "README.md").write_text(
        "# Experiment B - Strong Defense-in-Depth Baseline\n\n"
        "`acl_content_runtime` applies the existing Static ACL condition first, then the existing direct prompt-filter "
        "surface rule before runtime transitions and again on external/final candidates. Matches block; there is no "
        "safe-view rewrite. Policy records explicitly set `papc_features_used=false`.\n\n"
        f"New runs: {b_audit['new_completed']}/90; failures: {b_audit['new_failed']}. Reference schema-refresh runs: {b_audit['reference_refresh_rows']}.\n",
        encoding="utf-8",
    )
    (output / "00_remote_inputs" / "README.md").write_text(
        "# Remote Inputs\n\n"
        "Historical P1 raw traces named by the canonical manifests were not found on the remote host. The experiments "
        "therefore use the synced current implementation and task/policy definitions, while the historical committed "
        "high-level summaries remain read-only context. New raw deterministic traces remain in the isolated remote run roots.\n",
        encoding="utf-8",
    )

    manifest_rows = [
        {
            "artifact_type": "historical_raw_locator_missing",
            "remote_path": "/tmp/flowfence_nonoracle_heldout_deterministic",
            "run_family": "canonical_nonoracle_heldout",
            "used_for_experiment": "no",
            "size_bytes": 0,
            "sha256_if_practical": "",
            "notes": "Manifest locator checked; path absent on 2026-08-19.",
        },
        {
            "artifact_type": "remote_code_mirror",
            "remote_path": args.remote_repo_root,
            "run_family": "current_implementation_reference",
            "used_for_experiment": "mapping_only",
            "size_bytes": 0,
            "sha256_if_practical": "",
            "notes": "Not a Git checkout; no files were overwritten.",
        },
        {
            "artifact_type": "new_deterministic_raw",
            "remote_path": str(args.component_runs_root),
            "run_family": "component_ablation",
            "used_for_experiment": "yes",
            "size_bytes": directory_size(args.component_runs_root),
            "sha256_if_practical": "",
            "notes": "450 total rows: 270 new ablations plus 180 schema-refresh references.",
        },
        {
            "artifact_type": "new_deterministic_raw",
            "remote_path": str(args.composite_runs_root),
            "run_family": "composite_baseline",
            "used_for_experiment": "yes",
            "size_bytes": directory_size(args.composite_runs_root),
            "sha256_if_practical": "",
            "notes": "90 new ACL_CONTENT_RUNTIME runs.",
        },
        {
            "artifact_type": "new_deterministic_raw",
            "remote_path": str(args.reference_runs_root),
            "run_family": "composite_reference_refresh",
            "used_for_experiment": "yes",
            "size_bytes": directory_size(args.reference_runs_root),
            "sha256_if_practical": "",
            "notes": "180 Static ACL and Prompt Filter schema-refresh runs.",
        },
    ]
    write_csv(output / "REMOTE_SOURCE_MANIFEST.csv", manifest_rows)

    noapi_audit = f"""# No LLM API Audit

Experiments:
- Experiment A
- Experiment B

Provider calls expected: 0
Provider calls observed: 0

Verification:
- Every matrix config sets `agent_backend: scripted_deterministic`, `provider_calls_enabled: false`, and `no_llm_api_required: true`.
- `sweep_mas.py` rejects `no_llm_api_required=true` with provider calls enabled before constructing a provider client.
- Remote commands did not pass `--allow-provider-calls`; provider credential variables were removed from the experiment process environment.
- Every per-run metric records `provider_call_count=0`; aggregate A count={a_audit['provider_call_count']} and aggregate B/reference count={b_audit['provider_call_count']}.
- Every new run records `oracle_annotation_use_count=0`; aggregate A count={a_audit['oracle_annotation_use_count']} and aggregate B/reference count={b_audit['oracle_annotation_use_count']}.
- Importing the MiniMax client module does not initialize a client or make a request. The provider branch is unreachable when `provider_calls_enabled=false`.
- `environment/provider_network_log_search.txt` records the post-run endpoint/request-marker search.
"""
    (output / "NO_LLM_API_AUDIT.md").write_text(noapi_audit, encoding="utf-8")

    readme = f"""# WINE 2026 Rebuttal No-API Experiments

- Local repo root: `{args.local_repo_root}`
- Remote repo mapping inspected: `{args.remote_repo_root}`
- Remote isolated workspace: `{args.remote_workspace}`
- Remote experiment output root: `{args.remote_output_root}`
- Local result root: `{args.local_result_root}`
- Source Git HEAD: `{args.git_head}`

## Exact experiment commands

```bash
ssh wentian-server 'cd {args.remote_workspace} && env -u MINIMAX_API_KEY -u MINIMAX_BASE_URL -u MINIMAX_GROUP_ID -u MODEL_MINIMAX27 -u MINIMAX_MODEL PYTHONPATH=. {args.remote_repo_root}/.envs/FlowFence_py313/bin/python src/runner/sweep_mas.py --config configs/experiment/mas_rebuttal_noapi_component_ablation_pilot.yaml --output-root /tmp/flowfence_rebuttal_noapi_2026-08-19_pilot_a --status-path {args.remote_output_root}/01_component_ablation/logs/pilot_status.json'
ssh wentian-server 'cd {args.remote_workspace} && env -u MINIMAX_API_KEY -u MINIMAX_BASE_URL -u MINIMAX_GROUP_ID -u MODEL_MINIMAX27 -u MINIMAX_MODEL PYTHONPATH=. {args.remote_repo_root}/.envs/FlowFence_py313/bin/python src/runner/sweep_mas.py --config configs/experiment/mas_rebuttal_noapi_composite_pilot.yaml --output-root /tmp/flowfence_rebuttal_noapi_2026-08-19_pilot_b --status-path {args.remote_output_root}/02_composite_baseline/logs/pilot_status.json'
ssh wentian-server 'cd {args.remote_workspace} && env -u MINIMAX_API_KEY -u MINIMAX_BASE_URL -u MINIMAX_GROUP_ID -u MODEL_MINIMAX27 -u MINIMAX_MODEL PYTHONPATH=. {args.remote_repo_root}/.envs/FlowFence_py313/bin/python src/runner/sweep_mas.py --config configs/experiment/mas_rebuttal_noapi_component_ablation.yaml --output-root {args.component_runs_root} --status-path {args.remote_output_root}/01_component_ablation/logs/full_status.json'
ssh wentian-server 'cd {args.remote_workspace} && env -u MINIMAX_API_KEY -u MINIMAX_BASE_URL -u MINIMAX_GROUP_ID -u MODEL_MINIMAX27 -u MINIMAX_MODEL PYTHONPATH=. {args.remote_repo_root}/.envs/FlowFence_py313/bin/python src/runner/sweep_mas.py --config configs/experiment/mas_rebuttal_noapi_composite_baseline.yaml --output-root {args.composite_runs_root} --status-path {args.remote_output_root}/02_composite_baseline/logs/full_status.json'
ssh wentian-server 'cd {args.remote_workspace} && env -u MINIMAX_API_KEY -u MINIMAX_BASE_URL -u MINIMAX_GROUP_ID -u MODEL_MINIMAX27 -u MINIMAX_MODEL PYTHONPATH=. {args.remote_repo_root}/.envs/FlowFence_py313/bin/python src/runner/sweep_mas.py --config configs/experiment/mas_rebuttal_noapi_composite_reference_refresh.yaml --output-root {args.reference_runs_root} --status-path {args.remote_output_root}/02_composite_baseline/logs/reference_status.json'
ssh wentian-server 'cd {args.remote_workspace} && PYTHONPATH=. {args.remote_repo_root}/.envs/FlowFence_py313/bin/python scripts/summarize_wine_rebuttal_noapi.py --component-runs-root {args.component_runs_root} --composite-runs-root {args.composite_runs_root} --reference-runs-root {args.reference_runs_root} --output-root {args.remote_output_root} --local-repo-root {args.local_repo_root} --local-result-root {args.local_result_root} --remote-repo-root {args.remote_repo_root} --remote-workspace {args.remote_workspace} --remote-output-root {args.remote_output_root} --git-head {args.git_head}'
rsync -avz wentian-server:{args.remote_output_root}/ {args.local_result_root}/
```

## Counts

- Experiment A new: expected 270, completed {a_audit['new_completed']}, failed {a_audit['new_failed']}, retried 0.
- Experiment A schema refresh: {a_audit['reference_refresh_rows']} FULL/NO_SEMANTIC rows.
- Experiment B new: expected 90, completed {b_audit['new_completed']}, failed {b_audit['new_failed']}, retried 0.
- Experiment B schema refresh: {b_audit['reference_refresh_rows']} Static ACL/Prompt Filter rows; 90 matched FULL rows are reused from Experiment A refresh.

The reference refresh was necessary because the committed canonical package contains high-level summaries but not per-run cascade depth, action counts, or raw traces, and the historical remote raw locator is absent. No canonical artifact or paper file was modified.
"""
    (output / "README.md").write_text(readme, encoding="utf-8")
    print(json.dumps({"experiment_A": a_audit, "experiment_B": b_audit}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
