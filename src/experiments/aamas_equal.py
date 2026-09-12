"""Equal-capability deterministic comparison; historical WINE runs are immutable.

This adapter uses WINE's task, attacks, topology paths and scripted response
functions. It mediates every delivery, passes delivered content onward, and
evaluates untruncated delivered text before writing text-free audit records.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import platform
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.defenses.mas_flowfence import contains_poison_instruction, inspect_mas_event, validate_safe_view
from src.evaluators.utility import is_vendor_safe_update
from src.runtime.orchestrator import SyntheticMASOrchestrator, attack_for
from src.runtime.policy import channel_forbidden, is_recipient_allowed, privilege_level

DEFENSES = {"none", "ifc_safeview", "flowfence_lite_nonoracle"}
EXTERNAL_CHANNELS = {"external_message", "vendor_send_tool", "final_output"}
EPISODE_FIELDS = ("run_id task_id scenario_id model model_version topology condition attack defense seed success "
                  "privacy_safe_success raw_exposure external_exposure exposure_recipient_pairs cascade_size "
                  "privilege_reach blocks rewrites quarantines retries llm_calls input_tokens output_tokens "
                  "mediator_latency_ms e2e_latency_ms error_type status").split()


def validate_config(config: dict[str, Any]) -> None:
    if config.get("provider_calls_enabled") or config.get("agent_backend") != "scripted_deterministic":
        raise ValueError("E0 requires scripted_deterministic with provider calls disabled")
    if config.get("provider") != "minimax":
        raise ValueError("Keep existing MiniMax provider alignment")
    if not config.get("defense") or set(config["defense"]) - DEFENSES:
        raise ValueError("Unknown E0 defense")
    if not config.get("seed") or len(set(config["seed"])) != len(config["seed"]):
        raise ValueError("Unique, nonempty seeds required")
    if not config.get("task_id") or not config.get("attack") or not config.get("topology"):
        raise ValueError("Task, attacks and topologies are required")
    for key in ["topology", "attack", "defense"]:
        if len(config[key]) != len(set(config[key])):
            raise ValueError(f"Duplicate {key}")
    if set(config["topology"]) - {"chain_4", "star_4", "blackboard_4"}:
        raise ValueError("Unknown topology")
    for name in config["attack"]:
        attack_for(name)


class EqualMediationRunner(SyntheticMASOrchestrator):
    def __init__(self, config: dict[str, Any], repo_root: Path | None = None):
        super().__init__(config, repo_root=repo_root)
        self.audit: list[dict[str, Any]] = []
        self.mediator_ns = 0

    def deliver(self, content: str, *, event_type: str, channel: str, actor: str,
                recipient: str, parent: str | None = None) -> tuple[str, dict[str, Any]]:
        start = time.perf_counter_ns()
        result = inspect_mas_event(
            defense_mode=self.defense, event_type=event_type, actor_id=actor,
            recipient_id=recipient, channel=channel, target_zone=channel,
            content=content, topology=self.topology, secret_policies=self.secrets,
            attack_annotation=None,
        )
        elapsed = time.perf_counter_ns() - start
        self.mediator_ns += elapsed
        action = result.decision["decision"]
        delivered = "" if action in {"block", "quarantine"} else result.content
        disclosed = [s.secret_id for s in self.secrets if s.raw_value in delivered and
                     (channel_forbidden(s, channel) or not is_recipient_allowed(s, recipient))]
        poison = contains_poison_instruction(delivered)
        contaminated = bool(disclosed or poison)
        row = {
            "run_id": self.run_id, "event_id": f"evt_{len(self.audit)+1:06d}",
            "event_type": event_type, "channel": channel, "actor_id": actor,
            "recipient_id": recipient, "causal_parents": [parent] if parent else [],
            "decision": action, "lease_signal": result.decision["lease_signal"],
            "exposed_secret_ids": disclosed, "contains_poison_delivered": poison,
            "contaminated_delivered": contaminated,
            "external": recipient == "external_vendor_agent" or channel in EXTERNAL_CHANNELS,
            "privilege_reach": max(privilege_level(actor), privilege_level(recipient),
                                   privilege_level("vendor_send_tool") if channel in EXTERNAL_CHANNELS else 0) if contaminated else 0,
            "intervention": bool(result.decision["defense_fired"]),
            "mediator_latency_ns": elapsed, "input_bytes": len(content.encode()),
            "delivered_bytes": len(delivered.encode()),
            "oracle_annotation_used": result.decision.get("oracle_annotation_used", False),
        }
        self.audit.append(row)
        # Quarantine contains the raw source; only its validated generated safe
        # view can be read in a separate mediated event. IFC uses the same view.
        if action == "quarantine" and validate_safe_view(result.content, self.secrets):
            return result.content, row
        return delivered, row

    def run_equal(self) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        start = time.perf_counter_ns()
        source, _ = self._shared_seed_content()
        event_type, channel, _ = self._storage_channel_for_attack()
        actor = "external_vendor_agent" if self.attack.attack_id.startswith("comm_hijack") else "planner_agent"
        stored, seed = self.deliver(source, event_type=event_type, channel=channel,
                                    actor=actor, recipient="doc_writer_agent")
        writer_context = stored
        if seed["decision"] != "block":
            read_channel = "safe_view" if seed["decision"] in {"quarantine", "rewrite_safe_view"} else channel
            if self.topology.name == "chain_4":
                current, parent = stored, seed
                for actor, recipient in [("planner_agent", "finance_agent"), ("finance_agent", "doc_writer_agent")]:
                    current, parent = self.deliver(current, event_type="SEND_MESSAGE", channel="internal_message",
                                                   actor=actor, recipient=recipient, parent=parent["event_id"])
                writer_context = current
            elif self.topology.name == "star_4":
                for recipient in ["finance_agent", "doc_writer_agent", "external_vendor_agent"]:
                    message, _ = self.deliver(stored, event_type="SEND_MESSAGE",
                                             channel="external_message" if recipient == "external_vendor_agent" else "internal_message",
                                             actor="planner_agent", recipient=recipient, parent=seed["event_id"])
                    if recipient == "doc_writer_agent":
                        writer_context = message
            else:
                for recipient in ["finance_agent", "doc_writer_agent", "external_vendor_agent"]:
                    message, _ = self.deliver(stored, event_type="WORKSPACE_READ" if channel == "shared_doc" else "MEMORY_READ",
                                             channel=read_channel, actor=recipient, recipient=recipient, parent=seed["event_id"])
                    if recipient == "doc_writer_agent":
                        writer_context = message
                self.deliver(writer_context, event_type="SEND_MESSAGE", channel="internal_message",
                             actor="doc_writer_agent", recipient="finance_agent", parent=seed["event_id"])
        # Identical scripted response rule for all defenses; no method label is
        # consulted. E1 supplies genuinely model-generated decisions instead.
        candidate = self._leaky_vendor_update() if contains_poison_instruction(writer_context) else self._safe_vendor_update()
        sent, send = self.deliver(candidate, event_type="SEND_MESSAGE", channel="external_message",
                                  actor="doc_writer_agent", recipient="external_vendor_agent", parent=self.audit[-1]["event_id"])
        final, _ = self.deliver(sent, event_type="FINAL_OUTPUT", channel="final_output",
                                actor="external_vendor_agent", recipient="external_vendor_agent", parent=send["event_id"])
        success = is_vendor_safe_update(final, self.secrets)
        measured = aggregate_events(self.audit)
        episode = {
            "run_id": self.run_id, "task_id": self.case_id, "scenario_id": self.case_id,
            "model": "scripted_deterministic", "model_version": None,
            "topology": self.topology.name, "condition": "clean" if self.attack.attack_id == "none" else "attack",
            "attack": self.attack.attack_id, "defense": self.defense, "seed": int(self.config["seed"]),
            "success": success, "legacy_task_success": success,
            "privacy_safe_success": success and not measured["raw_exposure"],
            **measured, "retries": 0, "llm_calls": 0, "input_tokens": 0, "output_tokens": 0,
            "mediator_latency_ms": self.mediator_ns / 1e6,
            "e2e_latency_ms": (time.perf_counter_ns()-start) / 1e6,
            "error_type": None, "status": "complete",
        }
        return episode, self.audit


def aggregate_events(events: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "raw_exposure": sum(len(e["exposed_secret_ids"]) for e in events),
        "external_exposure": sum(bool(e["exposed_secret_ids"]) and e["external"] for e in events),
        "exposure_recipient_pairs": len({(s, e["recipient_id"]) for e in events for s in e["exposed_secret_ids"]}),
        "cascade_size": sum(e["contaminated_delivered"] for e in events),
        "privilege_reach": max((e["privilege_reach"] for e in events), default=0),
        "intervention_count": sum(e["intervention"] for e in events),
        "blocks": sum(e["decision"] == "block" for e in events),
        "rewrites": sum(e["decision"] == "rewrite_safe_view" for e in events),
        "quarantines": sum(e["decision"] == "quarantine" for e in events),
        "event_count": len(events),
    }


def execute_episode(config: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    started = time.perf_counter_ns()
    runner = None
    try:
        runner = EqualMediationRunner(config)
        return runner.run_equal()
    except Exception as exc:
        events = runner.audit if runner is not None else []
        return {
            "run_id":config['run_name'],"task_id":config['task_id'],"scenario_id":config['task_id'],
            "model":"scripted_deterministic","model_version":None,"topology":config['topology'],
            "condition":"clean" if config['attack']=='none' else "attack","attack":config['attack'],
            "defense":config['defense'],"seed":config['seed'],"success":False,"privacy_safe_success":False,
            **aggregate_events(events),"retries":0,"llm_calls":0,"input_tokens":0,"output_tokens":0,
            "mediator_latency_ms":runner.mediator_ns/1e6 if runner else 0,
            "e2e_latency_ms":(time.perf_counter_ns()-started)/1e6,
            "error_type":type(exc).__name__,"status":"failed","metrics_partial":True,
        }, events


def paired_summary(rows: list[dict[str, Any]], baseline: str = "ifc_safeview") -> dict[str, Any]:
    metrics = {"success": 1, "privacy_safe_success": 1, "raw_exposure": -1, "external_exposure": -1,
               "exposure_recipient_pairs": -1, "intervention_count": -1, "blocks": -1}
    index = {(r["task_id"],r["topology"],r["attack"],r["seed"],r["defense"]):r for r in rows}
    if len(index) != len(rows):
        raise ValueError("Duplicate matched episode keys")
    pairs = [(r, index[(r["task_id"],r["topology"],r["attack"],r["seed"],baseline)])
             for r in rows if r["defense"] == "flowfence_lite_nonoracle" and
             (r["task_id"],r["topology"],r["attack"],r["seed"],baseline) in index]
    result: dict[str, Any] = {"matched_groups":len(pairs), "independent_task_count":len({r["task_id"] for r,_ in pairs}),
                              "inference_note":"Seeds/attacks/topologies are not independent tasks; no task-population significance claimed."}
    for metric,direction in metrics.items():
        measured_pairs = [(a,b) for a,b in pairs if metric in {"success","privacy_safe_success"}
                          or not (a.get("metrics_partial") or b.get("metrics_partial"))]
        diffs = [(float(a[metric])-float(b[metric]))*direction for a,b in measured_pairs]
        by_task = {}
        for (a,b),diff in zip(measured_pairs,diffs): by_task.setdefault(a["task_id"],[]).append(diff)
        task_diffs = [statistics.mean(values) for values in by_task.values()]
        wins, losses = sum(x>0 for x in task_diffs),sum(x<0 for x in task_diffs)
        n = wins+losses
        p = min(1., 2*sum(math.comb(n,k) for k in range(min(wins,losses)+1))/2**n) if n else 1.
        result[metric] = {"better":sum(x>0 for x in diffs),"tie":sum(x==0 for x in diffs),"worse":sum(x<0 for x in diffs),
                          "unavailable_pairs":len(pairs)-len(measured_pairs),
                          "papc_minus_ifc_mean":statistics.mean(diffs)*direction if diffs else None,
                          "exact_sign_test_task_cluster_p":p, "independent_non_tied_task_clusters":n}
    return result


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    metrics = ["success","privacy_safe_success","raw_exposure","external_exposure","exposure_recipient_pairs",
               "cascade_size","privilege_reach","intervention_count","blocks","rewrites","quarantines","event_count"]
    return {"episode_count":len(rows), "failed_episodes":sum(r['status']!='complete' for r in rows),
            "task_count":len({r['task_id'] for r in rows}),
            "seed_count":len({r['seed'] for r in rows}),
            "by_defense":{d:{"episodes":len(group),**{m:statistics.mean(float(r[m]) for r in group) for m in metrics}}
                          for d in sorted({r["defense"] for r in rows}) for group in [[r for r in rows if r["defense"]==d]]},
            "paired":paired_summary(rows)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--summarize-only",action="store_true")
    args = parser.parse_args()
    if args.summarize_only:
        rows = [json.loads(line) for line in (args.output/"episodes.jsonl").read_text().splitlines()]
    else:
        config = json.loads(args.config.read_text()); validate_config(config)
        args.output.mkdir(parents=True,exist_ok=True)
        # Exclusive output creation protects earlier formal evidence from overwrite.
        with (args.output/"run_manifest.json").open("x") as handle:
            json.dump({"config":config,"config_sha256":hashlib.sha256(args.config.read_bytes()).hexdigest(),
                       "command":sys.argv,"started_at":datetime.now(timezone.utc).isoformat(),
                       "python":platform.python_version()},handle,indent=2)
        rows=[]
        with (args.output/"episodes.jsonl").open("x") as episodes, (args.output/"events.safe.jsonl").open("x") as audit:
            for topology,attack,seed,defense in itertools.product(config["topology"],config["attack"],config["seed"],config["defense"]):
                single={**config,"topology":topology,"attack":attack,"seed":seed,"defense":defense,
                        "run_name":f"E0__{config['task_id']}__{topology}__{attack}__{defense}__seed{seed}"}
                row,events=execute_episode(single)
                rows.append(row); episodes.write(json.dumps(row,sort_keys=True)+"\n"); episodes.flush()
                for event in events: audit.write(json.dumps(event,sort_keys=True)+"\n")
    summary=summarize(rows)
    (args.output/"summary.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"episodes":len(rows),"paired":summary["paired"]},sort_keys=True))


if __name__ == "__main__":
    main()
