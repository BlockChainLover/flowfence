#!/usr/bin/env python3
"""Dry-run-first cleanup helper for the two-paper rebuttal organization.

The script reads reviewed cleanup manifests and prints what would be removed.
Deletion requires both --execute and --confirm DELETE_REBUTTAL_CLEANUP.
"""

from __future__ import annotations

import argparse
import csv
import shutil
from dataclasses import dataclass
from pathlib import Path


CONFIRM_TOKEN = "DELETE_REBUTTAL_CLEANUP"
PAPER_MANIFEST = Path("research/notes/paper_cleanup_candidates_manifest.csv")
RESULTS_MANIFEST = Path("results/cleanup_candidates_manifest.csv")
PROTECTED_PATHS = {
    Path("papers/emnlp2026_flowfence"),
    Path("papers/wine2026_flowfence"),
    Path("papers/README.md"),
}


@dataclass(frozen=True)
class CleanupEntry:
    entry: Path
    entry_type: str
    reason: str
    exists_recorded: str
    manifest: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Review or execute the approved rebuttal cleanup manifests. "
            "Default mode is a dry run."
        )
    )
    parser.add_argument(
        "--scope",
        choices=("papers", "results", "all"),
        default="all",
        help="Cleanup manifest scope to process. Default: all.",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="Repository root. Default: current working directory.",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually delete manifest entries. Omit for dry run.",
    )
    parser.add_argument(
        "--confirm",
        default="",
        help=f"Required token for --execute: {CONFIRM_TOKEN}",
    )
    return parser.parse_args()


def load_manifest(repo_root: Path, manifest: Path) -> list[CleanupEntry]:
    path = repo_root / manifest
    if not path.exists():
        raise FileNotFoundError(f"Missing cleanup manifest: {manifest}")
    entries: list[CleanupEntry] = []
    with path.open(newline="") as handle:
        for row in csv.DictReader(handle):
            raw_entry = row.get("entry", "").strip()
            if not raw_entry:
                continue
            entry_path = Path(raw_entry)
            if manifest == RESULTS_MANIFEST and (
                not entry_path.parts or entry_path.parts[0] != "results"
            ):
                entry_path = Path("results") / entry_path
            entries.append(
                CleanupEntry(
                    entry=entry_path,
                    entry_type=row.get("type", "").strip(),
                    reason=row.get("reason", "").strip(),
                    exists_recorded=row.get("exists", "").strip(),
                    manifest=manifest,
                )
            )
    return entries


def selected_entries(repo_root: Path, scope: str) -> list[CleanupEntry]:
    entries: list[CleanupEntry] = []
    if scope in ("papers", "all"):
        entries.extend(load_manifest(repo_root, PAPER_MANIFEST))
    if scope in ("results", "all"):
        entries.extend(load_manifest(repo_root, RESULTS_MANIFEST))
    return entries


def ensure_safe(repo_root: Path, entry: CleanupEntry) -> Path:
    target = (repo_root / entry.entry).resolve()
    root = repo_root.resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"Refusing path outside repo: {entry.entry}") from exc

    rel = target.relative_to(root)
    if rel in PROTECTED_PATHS:
        raise ValueError(f"Refusing protected retained path: {rel}")
    if rel.parts and rel.parts[0] not in {"papers", "results"}:
        raise ValueError(f"Refusing non-paper/result cleanup path: {rel}")
    return target


def remove_target(path: Path) -> str:
    if not path.exists() and not path.is_symlink():
        return "missing"
    if path.is_symlink() or path.is_file():
        path.unlink()
        return "deleted_file"
    if path.is_dir():
        shutil.rmtree(path)
        return "deleted_dir"
    raise ValueError(f"Unsupported path type: {path}")


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    entries = selected_entries(repo_root, args.scope)
    if args.execute and args.confirm != CONFIRM_TOKEN:
        raise SystemExit(
            f"--execute requires --confirm {CONFIRM_TOKEN}; refusing deletion"
        )

    print(f"scope={args.scope}")
    print(f"mode={'execute' if args.execute else 'dry-run'}")
    print(f"entries={len(entries)}")

    planned = []
    missing = []
    for entry in entries:
        target = ensure_safe(repo_root, entry)
        status = "exists" if target.exists() or target.is_symlink() else "missing"
        planned.append((entry, target, status))
        if status == "missing":
            missing.append(entry.entry.as_posix())

    print(f"existing={len(planned) - len(missing)}")
    print(f"missing={len(missing)}")
    for entry, target, status in planned:
        rel = target.relative_to(repo_root)
        print(f"{status}\t{rel}\t{entry.reason}")

    if not args.execute:
        print("dry-run only; no files deleted")
        return 0

    deleted = []
    for entry, target, _status in planned:
        deleted.append((entry.entry.as_posix(), remove_target(target)))
    print("delete summary:")
    for rel, status in deleted:
        print(f"{status}\t{rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
