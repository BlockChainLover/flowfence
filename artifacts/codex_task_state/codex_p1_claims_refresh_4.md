# Codex Task State: p1-claims-refresh-4

## Goal

Refresh the evidence index and claims checklist after the completed MiniMax-only 3-seed P1 MAS coverage experiment and timeout retry. This goal is documentation-only and records conservative claim boundaries for the 252/252 completed MiniMax synthetic-runtime coverage.

## Branch

`codex/p1-claims-refresh-4`

## Inputs Inspected

- `AGENTS.md`
- `results/evidence_index/current_evidence_index.md`
- `papers/claims_checklist.md`
- `artifacts/evidence_index/p1_claims_refresh_3.md`
- `artifacts/codex_task_state/codex_p1_real_minimax_coverage_3seed.md`
- `artifacts/codex_task_state/codex_p1_real_minimax_coverage_3seed_debug.md`
- `artifacts/minimax_p1_coverage_3seed/README.md`
- `artifacts/minimax_p1_coverage_3seed/run_manifest.json`
- `artifacts/minimax_p1_coverage_3seed/coverage_summary.json`
- `artifacts/minimax_p1_coverage_3seed/coverage_summary.md`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_defense.csv`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_defense.md`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_topology.csv`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_topology.md`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_attack.csv`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_attack.md`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_attack_defense.csv`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_attack_defense.md`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_seed.csv`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_seed.md`
- `artifacts/minimax_p1_coverage_3seed/flowfence_clean_matrix.csv`
- `artifacts/minimax_p1_coverage_3seed/flowfence_clean_matrix.md`
- `artifacts/minimax_p1_coverage_3seed/failure_breakdown.jsonl`
- `artifacts/minimax_p1_coverage_3seed_debug/README.md`
- `artifacts/minimax_p1_coverage_3seed_debug/debug_summary.json`
- `artifacts/minimax_p1_coverage_3seed_debug/debug_summary.md`
- `artifacts/minimax_p1_coverage_3seed_debug/failed_run_diagnosis.json`
- `artifacts/minimax_p1_coverage_3seed_debug/retry_manifest.json`

## Completed

- Updated the current evidence index with a 252-run MiniMax 3-seed coverage section.
- Added conservative claims checklist rows for 252/252 completion, FlowFence 63/63 clean subset, configured leakage comparisons, topology effects, and unsupported boundaries.
- Created `artifacts/evidence_index/p1_claims_refresh_4.md`.
- Updated MiniMax 3-seed coverage README caveats.
- Updated timeout debug README outcome notes.
- Did not run experiments or call MiniMax.

## Changed Files

- `results/evidence_index/current_evidence_index.md`
- `papers/claims_checklist.md`
- `artifacts/evidence_index/p1_claims_refresh_4.md`
- `artifacts/minimax_p1_coverage_3seed/README.md`
- `artifacts/minimax_p1_coverage_3seed_debug/README.md`
- `artifacts/codex_task_state/codex_p1_claims_refresh_4.md`

## Validation Commands

- `git diff --check`
- `python -m compileall scripts src`
- `git status --short`

## Claim Status Changes

- Supported: 252/252 configured MiniMax-only synthetic-runtime coverage completion after retrying one transient MiniMax timeout.
- Supported: FlowFence-Lite clean subset across 63/63 configured FlowFence runs, with task success 1.0 and zero raw/external leakage.
- Supported: FlowFence-Lite improves or ties no-defense, static ACL, and prompt-filter on configured raw/external leakage comparisons.
- Supported with caveat: topology effects observed in the 252-run MiniMax synthetic-runtime benchmark.
- Still unsupported: non-MiniMax generalization, production safety, real browser/desktop/computer-use agent evidence, broad real-world robustness, learned graph risk scorer, full official AgentPoison reproduction, and coverage larger than the completed 252-run MiniMax matrix.

## Known Limitations

- The 252-run evidence is MiniMax-only.
- The runtime is a synthetic deterministic MAS benchmark with MiniMax final-writer calls, not a real-world agent deployment.
- Raw traces, prompts, provider outputs, event JSONL, policy JSONL, and per-run metrics remain intentionally uncommitted.
- The update is documentation-only and does not regenerate paper-facing tables.

## Resume Instructions

Next recommended goal: `p1-paper-tables-refresh-2`.

Regenerate paper-facing tables from the refreshed 252-run coverage artifacts before drafting the results section. Continue to avoid non-MiniMax, production-safety, or real-world computer-use claims unless new evidence is explicitly added.
