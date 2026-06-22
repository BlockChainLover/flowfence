# Codex Task State: rebuttal-repo-organization

## Goal

Organize the repository around the completed EMNLP paper and the WINE draft so rebuttal work can quickly locate experimental methods, results, metrics, claims, caveats, and raw evidence roots.

## Branch

`codex/aaai27-claims-results-sync`

## Completed Work

- Reread `research/contract/`, `research/logs/roadmap.md`, and `research/logs/progress.md`.
- Confirmed current phase: paper drafting.
- Identified the next decision: evidence retention and cleanup approval for the two-paper rebuttal structure.
- Imported the WINE revised draft source under `papers/wine2026_flowfence/`.
- Added the EMNLP evidence map at `experiments/emnlp2026_flowfence/README.md`.
- Added the WINE evidence map at `experiments/wine2026_flowfence/README.md`.
- Added concrete retained-result and cleanup-candidate manifests for the current `results/` directory.
- Added `scripts/rebuttal_cleanup.py`, a dry-run-first cleanup helper requiring `--execute --confirm DELETE_REBUTTAL_CLEANUP` before deleting.
- Added `research/notes/paper_cleanup_candidates_manifest.csv` and `research/notes/rebuttal_organization_completion_audit_2026-06-22.md`.
- Added `research/notes/rebuttal_quick_lookup_2026-06-22.md` as the top-level rebuttal navigation index.
- Added paper-specific contracts under `research/contract/`.
- Updated top-level experiment/result/paper navigation.
- Added `research/notes/rebuttal_cleanup_manifest_2026-06-22.md` with exact cleanup candidates.
- Updated `research/logs/roadmap.md` and `research/logs/progress.md`.
- Executed the reviewed paper cleanup and result cleanup with `scripts/rebuttal_cleanup.py`.
- Removed legacy top-level experiment planning files so `experiments/` has one canonical evidence-map folder per retained paper.
- Updated cleanup manifests, completion audit, roadmap, and result navigation after physical cleanup.

## Changed Files

- `experiments/README.md`
- `experiments/emnlp2026_flowfence/`
- `experiments/wine2026_flowfence/`
- `papers/README.md`
- `papers/emnlp2026_flowfence/`
- `papers/wine2026_flowfence/`
- `research/contract/emnlp2026_flowfence.md`
- `research/contract/wine2026_flowfence.md`
- `research/logs/roadmap.md`
- `research/logs/progress.md`
- `research/notes/rebuttal_cleanup_manifest_2026-06-22.md`
- `research/notes/paper_cleanup_candidates_manifest.csv`
- `research/notes/rebuttal_organization_completion_audit_2026-06-22.md`
- `research/notes/rebuttal_quick_lookup_2026-06-22.md`
- `results/README.md`
- `results/canonical_evidence_manifest.csv`
- `results/cleanup_candidates_manifest.csv`
- `results/evidence_manifest_summary.md`
- `scripts/rebuttal_cleanup.py`

## Validation Commands

- `git branch --show-current`
- `git status --short`
- `find papers -maxdepth 2 -mindepth 1 -type d -print | sort`
- `find experiments -maxdepth 2 -type f -print | sort`
- `find results -maxdepth 1 -mindepth 1 -type d -print | sort`
- `find artifacts -maxdepth 2 -type f -print | sort`
- `sed -n '1,80p' artifacts/emnlp2026_p0/results/emnlp_p0_cross_provider_runs.csv`
- `sed -n '1,120p' artifacts/icde2027_supplemental/results/poison_pressure_runs.csv`
- `sed -n '1,120p' artifacts/icde2027_supplemental/results/paraphrase_family_runs.csv`
- `sed -n '1,80p' artifacts/icde2027_supplemental/results/false_positive_runs.csv`
- `python3` inline manifest generation over `results/` and cited summary artifacts
- `python3 scripts/rebuttal_cleanup.py --help`
- `python3 scripts/rebuttal_cleanup.py --scope papers`
- `python3 scripts/rebuttal_cleanup.py --scope results`
- `python3 scripts/rebuttal_cleanup.py --scope all`
- `python3 scripts/rebuttal_cleanup.py --scope papers --execute --confirm DELETE_REBUTTAL_CLEANUP`
- `python3 scripts/rebuttal_cleanup.py --scope results --execute --confirm DELETE_REBUTTAL_CLEANUP`
- `find papers -maxdepth 1 -mindepth 1 -print | sort`
- `find experiments -maxdepth 2 -type f -print | sort`
- `python3` inline verification that retained result manifests have zero missing paths and cleanup manifests have zero existing candidates
- `PYTHONPYCACHEPREFIX=.pycache python3 -m py_compile scripts/rebuttal_cleanup.py`

## Known Limitations

- The cleanup has many tracked deletions and new organization files in the worktree; no commit has been created yet.
- Current `results/` classification is complete at the top level: 155 retained canonical entries and 97 removed cleanup candidates, with zero unclassified candidates.
- Current paper cleanup classification lists 17 removed cleanup candidates.
- WINE P1 raw provider outputs and raw traces are intentionally not committed; rebuttal should cite committed high-level summaries and safe traces.

## Resume Instructions

1. Review `experiments/emnlp2026_flowfence/README.md` and `experiments/wine2026_flowfence/README.md` for evidence-map correctness.
2. Use `research/notes/rebuttal_quick_lookup_2026-06-22.md` as the front door for rebuttal lookup.
3. If a claim or table changes, update the relevant per-paper evidence map and `research/logs/progress.md`.
4. Before committing, inspect the large deletion set with `git status --short` and `git diff --stat`.
5. End each follow-up task with `git status --short`.
