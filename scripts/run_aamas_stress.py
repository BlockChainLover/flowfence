#!/usr/bin/env python3
"""Run or re-summarize API-free AAMAS E2/E3 experiments."""
import argparse
import json
import shlex
import sys
from pathlib import Path

from src.experiments.aamas_stress import run, write_summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--tables", type=Path)
    parser.add_argument("--summarize-only", action="store_true", help="Rebuild summary from episodes.jsonl without executing probes")
    args = parser.parse_args()
    if args.summarize_only:
        rows = [json.loads(line) for line in (args.output / "episodes.jsonl").read_text().splitlines()]
        write_summary(rows, json.loads(args.config.read_text())["experiment"], args.output, args.tables)
    else:
        command = "PYTHONPATH=. " + shlex.join([sys.executable, *sys.argv])
        run(args.config, args.output, command, args.tables)


if __name__ == "__main__":
    main()
