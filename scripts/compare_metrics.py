#!/usr/bin/env python3
"""Compare top-level numeric metrics in two JSON files."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return payload


def numeric(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def parse_keys(value: str | None) -> list[str] | None:
    if not value:
        return None
    return [item.strip() for item in value.split(",") if item.strip()]


def compare(a_path: Path, b_path: Path, *, keys: list[str] | None, tolerance: float) -> tuple[list[dict[str, Any]], bool]:
    a = load_json(a_path)
    b = load_json(b_path)
    if keys is None:
        keys = sorted(key for key in set(a) & set(b) if numeric(a.get(key)) and numeric(b.get(key)))
    rows: list[dict[str, Any]] = []
    ok = True
    for key in keys:
        av = a.get(key)
        bv = b.get(key)
        if not (numeric(av) and numeric(bv)):
            rows.append({"key": key, "a": av, "b": bv, "delta": None, "status": "SKIP_NON_NUMERIC"})
            continue
        delta = float(bv) - float(av)
        status = "OK" if abs(delta) <= tolerance else "DIFF"
        ok = ok and status == "OK"
        rows.append({"key": key, "a": av, "b": bv, "delta": delta, "status": status})
    return rows, ok


def print_rows(rows: list[dict[str, Any]]) -> None:
    print("key\ta\tb\tdelta\tstatus")
    for row in rows:
        print(f"{row['key']}\t{row['a']}\t{row['b']}\t{row['delta']}\t{row['status']}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare top-level numeric metrics between two JSON files.")
    parser.add_argument("--a", required=True, type=Path, help="First metrics JSON file.")
    parser.add_argument("--b", required=True, type=Path, help="Second metrics JSON file.")
    parser.add_argument("--keys", help="Comma-separated top-level keys to compare.")
    parser.add_argument("--tolerance", type=float, default=1e-6, help="Numeric tolerance.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    rows, ok = compare(args.a, args.b, keys=parse_keys(args.keys), tolerance=args.tolerance)
    print_rows(rows)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
