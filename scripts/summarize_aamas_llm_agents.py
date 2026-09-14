#!/usr/bin/env python3
"""Rebuild E1/E4 summaries and paired parameter-cluster intervals from safe JSONL."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.experiments.aamas_llm_agents import summarize_episodes
from src.experiments.aamas_paired import paired_parameter_inference


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Saved episodes.jsonl")
    parser.add_argument("--output", type=Path, required=True, help="New/rebuilt summary JSON")
    parser.add_argument("--bootstrap-draws", type=int, default=10000)
    args = parser.parse_args()
    rows = [json.loads(line) for line in args.input.read_text().splitlines() if line]
    summary = summarize_episodes(rows)
    summary["paired_parameter_cluster_inference"] = paired_parameter_inference(rows, args.bootstrap_draws)
    summary["dry_run"] = any(r.get("agent_backend") == "deterministic_wiring_fixture" for r in rows)
    if summary["dry_run"]:
        summary["evidence_status"] = "WIRING_ONLY_NOT_LLM_EVIDENCE"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"episodes": len(rows), "independent_historical_scenarios": summary["paired_parameter_cluster_inference"]["independent_historical_scenarios"]}))


if __name__ == "__main__":
    main()
