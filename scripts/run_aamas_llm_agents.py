#!/usr/bin/env python3
"""Run or summarize the AAMAS intermediate-agent pilot/formal matrix."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.common.provider_loader import load_provider_profile
from src.experiments.aamas_llm_agents import load_config, run_matrix, summarize_episodes


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--provider-env", type=Path, help="Existing local/remote provider env; never printed or copied")
    parser.add_argument("--private-output", type=Path, help="Optional full synthetic traces outside safe artifact root; files mode0600, never bundle/commit")
    parser.add_argument("--dry-run", action="store_true", help="Deterministic wiring fixture; NOT LLM evidence")
    parser.add_argument("--summarize-only", action="store_true")
    parser.add_argument("--retry-run-id", help="Retry a saved unsuccessful episode, retaining and linking the original")
    args = parser.parse_args()
    config, tasks, hashes = load_config(args.config)
    if args.summarize_only:
        rows = [json.loads(line) for line in (args.output / "episodes.jsonl").read_text().splitlines() if line]
        summary = summarize_episodes(rows)
        summary_path = args.output / "summary.json"
        if summary_path.exists():
            prior = json.loads(summary_path.read_text())
            for key in ("dry_run", "evidence_status"):
                if key in prior:
                    summary[key] = prior[key]
        summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    else:
        profile = None
        if args.provider_env is not None:
            profile = load_provider_profile(str(args.provider_env), config.get("provider_profile", "minimax27"))
            if profile["model_name"] != config["model"]:
                raise ValueError("Registered model differs from the existing provider profile")
        if config["phase"] == "second_model" and profile is None and not args.dry_run:
            raise ValueError("E4 requires the existing provider profile; do not reuse MiniMax credentials")
        summary = run_matrix(config, tasks, args.output, dry_run=args.dry_run, config_hashes=hashes, retry_run_id=args.retry_run_id, provider_settings=profile, private_output=args.private_output)
    print(json.dumps({key: summary[key] for key in ("episodes", "failed_episodes", "blocked_episodes", "llm_calls")}))


if __name__ == "__main__":
    main()
