#!/usr/bin/env python3
"""Audit no-API pilot runs and action counts."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs-root", action="append", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows: list[dict[str, Any]] = []
    for root in args.runs_root:
        rows.extend(json.loads(path.read_text(encoding="utf-8")) for path in root.glob("*/metrics.json"))
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["defense"])].append(row)
    report = {
        "runs": len(rows),
        "provider_call_count": sum(int(row["provider_call_count"]) for row in rows),
        "oracle_annotation_use_count": sum(int(row["oracle_annotation_use_count"]) for row in rows),
        "by_defense": {
            defense: {
                "runs": len(defense_rows),
                "safe_view_count": sum(int(row["safe_view_count"]) for row in defense_rows),
                "quarantine_count": sum(int(row["quarantine_count"]) for row in defense_rows),
                "block_count": sum(int(row["block_count"]) for row in defense_rows),
                "propagation_right_downgrade_count": sum(
                    int(row["propagation_right_downgrade_count"]) for row in defense_rows
                ),
                "acl_block_count": sum(int(row["acl_block_count"]) for row in defense_rows),
                "runtime_content_block_count": sum(
                    int(row["runtime_content_block_count"]) for row in defense_rows
                ),
                "final_content_block_count": sum(int(row["final_content_block_count"]) for row in defense_rows),
            }
            for defense, defense_rows in sorted(grouped.items())
        },
    }
    payload = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 1 if report["provider_call_count"] or report["oracle_annotation_use_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
