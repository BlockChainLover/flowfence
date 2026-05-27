# Codex Task State: p1-claims-refresh-2

## Goal

Refresh evidence docs and claims checklist after the P1 MiniMax debug run, clearly separating pre-debug smoke evidence from post-debug debug-smoke evidence while avoiding broad paper claims.

## Branch

codex/p1-claims-refresh-2

## Inputs Inspected

- `AGENTS.md`
- `research/contract/`
- `research/logs/roadmap.md`
- `research/logs/progress.md`
- `results/evidence_index/current_evidence_index.md`
- `papers/claims_checklist.md`
- `artifacts/evidence_index/p1_claims_refresh.md`
- `artifacts/codex_task_state/codex_p1_claims_refresh.md`
- `artifacts/codex_task_state/codex_p1_real_minimax_debug.md`
- `artifacts/minimax_p1_smoke/README.md`
- `artifacts/minimax_p1_smoke/run_manifest.json`
- `artifacts/minimax_p1_smoke/summary_18run.json`
- `artifacts/minimax_p1_smoke/summary_18run.md`
- `artifacts/minimax_p1_smoke_debug/README.md`
- `artifacts/minimax_p1_smoke_debug/run_manifest.json`
- `artifacts/minimax_p1_smoke_debug/debug_summary.json`
- `artifacts/minimax_p1_smoke_debug/debug_summary.md`

## Completed

- Updated the current evidence index to distinguish P0 retrieval-memory evidence, P1 deterministic synthetic evidence, pre-debug MiniMax smoke evidence, and post-debug MiniMax debug-smoke evidence.
- Updated the claims checklist with conservative post-debug MiniMax debug-smoke claims and unsupported-claim boundaries.
- Added `artifacts/evidence_index/p1_claims_refresh_2.md`.
- Updated MiniMax smoke README files to point from the pre-debug smoke to the debug evidence and to state the next clean rerun step.

## Changed Files

- `results/evidence_index/current_evidence_index.md`
- `papers/claims_checklist.md`
- `artifacts/evidence_index/p1_claims_refresh_2.md`
- `artifacts/minimax_p1_smoke/README.md`
- `artifacts/minimax_p1_smoke_debug/README.md`
- `artifacts/codex_task_state/codex_p1_claims_refresh_2.md`

## Validation Commands

- `git diff --check`
- `python -m compileall scripts src`
- `git status --short`

## Claim Status Changes

- Supported as debugging evidence: the initial low task success was primarily due to final-writer prompt shape plus utility-evaluator strictness.
- Supported as debug-smoke evidence: the post-debug MiniMax 18-run debug smoke completed 18/18 runs with `task_success_rate=1.0`.
- Partially supported: MiniMax task success and leakage observations remain small-smoke evidence only.
- Still unsupported: broad real-model robustness, non-MiniMax generalization, full paper-ready MiniMax MAS evidence, broad superiority over all baselines, and full real-model multi-seed robustness.
- Remaining risk: post-debug leakage remains non-zero with `unauthorized_raw_leakage_mean=3.333333` and `external_leakage_mean=0.222222`.

## Known Limitations

- This goal did not run experiments or call MiniMax.
- This goal did not inspect raw traces, raw prompts, raw provider outputs, provider logs, or `.env` files.
- The post-debug evidence remains a small MiniMax-only debug smoke, not a full real-model experiment.

## Resume Instructions

Resume from branch `codex/p1-claims-refresh-2`.

First run:

- `git branch --show-current`
- `git status --short`

Then inspect:

- `results/evidence_index/current_evidence_index.md`
- `papers/claims_checklist.md`
- `artifacts/evidence_index/p1_claims_refresh_2.md`
- `artifacts/codex_task_state/codex_p1_claims_refresh_2.md`

Recommended next goal: `p1-real-minimax-18run-rerun`.
