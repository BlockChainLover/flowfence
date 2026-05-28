# Codex Task State: p1-claims-refresh-3

## Goal

Refresh the evidence index and claims checklist after the post-fix MiniMax 18-run smoke audit. The refresh documents that the aggregate task-success gap is baseline-driven, not FlowFence-driven, while keeping all claims conservative and scoped.

## Branch

`codex/p1-claims-refresh-3`

## Inputs Inspected

- `AGENTS.md`
- `results/evidence_index/current_evidence_index.md`
- `papers/claims_checklist.md`
- `artifacts/evidence_index/p1_claims_refresh_2.md`
- `artifacts/codex_task_state/codex_p1_claims_refresh_2.md`
- `artifacts/minimax_p1_smoke_postfix/README.md`
- `artifacts/minimax_p1_smoke_postfix/run_manifest.json`
- `artifacts/minimax_p1_smoke_postfix/summary_18run.json`
- `artifacts/minimax_p1_smoke_postfix/summary_18run.md`
- `artifacts/minimax_p1_smoke_postfix_audit/README.md`
- `artifacts/minimax_p1_smoke_postfix_audit/audit_summary.json`
- `artifacts/minimax_p1_smoke_postfix_audit/audit_summary.md`
- `artifacts/minimax_p1_smoke_postfix_audit/failure_breakdown.jsonl`
- `artifacts/codex_task_state/codex_p1_real_minimax_debug_2.md`

## Completed

- Added clean post-fix MiniMax 18-run smoke and audit evidence to the current evidence index.
- Added conservative paper-facing claim rows for the clean post-fix smoke, FlowFence clean subset, baseline-driven task-success gap, and prompt-filter indirect workspace-poisoning failures.
- Created `artifacts/evidence_index/p1_claims_refresh_3.md`.
- Updated MiniMax post-fix README files to point to the audit interpretation and claim boundaries.
- Did not run experiments or call MiniMax.
- Did not modify implementation code, raw result files, event traces, provider outputs, prompts, or research logs.

## Changed Files

- `results/evidence_index/current_evidence_index.md`
- `papers/claims_checklist.md`
- `artifacts/evidence_index/p1_claims_refresh_3.md`
- `artifacts/minimax_p1_smoke_postfix/README.md`
- `artifacts/minimax_p1_smoke_postfix_audit/README.md`
- `artifacts/codex_task_state/codex_p1_claims_refresh_3.md`

## Validation Commands

- `git diff --check`
- `python -m compileall scripts src`
- `git status --short`

## Claim Status Changes

- Now supported as small MiniMax smoke evidence: the clean post-fix 18-run smoke completed 18/18 runs and observed `topology_effect_observed=true`.
- Now supported as small MiniMax smoke evidence: FlowFence-Lite was clean across all 6 FlowFence runs, with `task_success_rate=1.0`, `unauthorized_raw_leakage_mean=0.0`, and `external_leakage_mean=0.0`.
- Now supported as audit evidence: the aggregate `task_success_rate=0.888889` gap is baseline-driven, not FlowFence-driven.
- Now supported as small-smoke baseline evidence: prompt-filter has two `workspace_poisoning_indirect` failures with non-zero raw and external leakage.
- Still unsupported: broad real-model robustness, non-MiniMax generalization, real-model multi-seed robustness, full 252-run real MiniMax matrix, production safety claims, and full official AgentPoison reproduction.

## Known Limitations

- The clean post-fix MiniMax evidence is a small 18-run smoke with one seed.
- The FlowFence clean-subset claim is scoped to 6 saved MiniMax smoke runs.
- The prompt-filter failure claim is scoped to the tested indirect workspace-poisoning smoke cases.
- No broad provider, topology, or deployment generalization is supported.

## Resume Instructions

Next recommended goal: `p1-results-table-export`.

Use the current evidence index, claims checklist, P0 summaries, deterministic P1 task-state files, strengthened synthetic summaries, clean post-fix MiniMax smoke summaries, and post-fix audit summaries to produce paper-facing tables. Continue to avoid raw traces, provider outputs, prompts, secrets, and non-MiniMax claims.
