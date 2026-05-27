# Codex Task State: p1-claims-refresh

## Goal

Refresh the evidence index and claims checklist after the P1 deterministic MAS benchmark, strengthened synthetic benchmark, and MiniMax 18-run smoke. Update claim status conservatively and explicitly separate synthetic evidence, MiniMax smoke evidence, unsupported claims, and next evidence required.

## Branch

codex/p1-claims-refresh

## Inputs Inspected

- `AGENTS.md`
- `results/evidence_index/current_evidence_index.md`
- `papers/claims_checklist.md`
- `artifacts/codex_task_state/codex_p1_mas_sweep.md`
- `artifacts/codex_task_state/codex_p1_benchmark_strengthening.md`
- `artifacts/codex_task_state/codex_p1_real_minimax_small.md`
- `artifacts/codex_task_state/codex_p1_real_minimax_small_run.md`
- `artifacts/minimax_p1_smoke/README.md`
- `artifacts/minimax_p1_smoke/run_manifest.json`
- `artifacts/minimax_p1_smoke/summary_2run.json`
- `artifacts/minimax_p1_smoke/summary_2run.md`
- `artifacts/minimax_p1_smoke/summary_18run.json`
- `artifacts/minimax_p1_smoke/summary_18run.md`

## Completed

- Updated the current evidence index to distinguish P0 AgentPoison evidence, P1 deterministic synthetic evidence, P1 strengthened deterministic evidence, and P1 MiniMax smoke evidence.
- Updated the claims checklist with conservative P1 synthetic and MiniMax-smoke claim rows.
- Added a concise P1 claims refresh artifact.
- Updated the MiniMax smoke README with the low-task-success caveat and next-step guidance.

## Changed Files

- `results/evidence_index/current_evidence_index.md`
- `papers/claims_checklist.md`
- `artifacts/minimax_p1_smoke/README.md`
- `artifacts/evidence_index/p1_claims_refresh.md`
- `artifacts/codex_task_state/codex_p1_claims_refresh.md`

## Validation Commands

- `git diff --check`
- `python -m compileall scripts src`
- `git status --short`

## Claim Status Changes

- Supported: deterministic synthetic topology effects, scoped to the strengthened deterministic MAS benchmark.
- Supported: deterministic synthetic FlowFence improvements over `prompt_filter` on indirect attacks, scoped to the synthetic benchmark.
- Partially supported: MiniMax 18-run smoke leakage-reduction observations and observed topology effect, smoke-only and not paper-ready.
- Limitation recorded: MiniMax final-writer task success is `0.055556`.
- Still unsupported: non-MiniMax generalization, broad real-model robustness, paper-ready MiniMax topology claims, utility preservation under real MiniMax, broad superiority over all baselines, and full official AgentPoison reproduction.

## Known Limitations

- This goal changed documentation only.
- No raw traces, provider outputs, or event JSONL files were inspected.
- No experiments were run and no provider was called.
- MiniMax smoke evidence remains low-confidence until task success is debugged.

## Resume Instructions

Resume from branch `codex/p1-claims-refresh`.

First run:

- `git branch --show-current`
- `git status --short`

Then inspect:

- `artifacts/evidence_index/p1_claims_refresh.md`
- `results/evidence_index/current_evidence_index.md`
- `papers/claims_checklist.md`

Do not start MiniMax debugging in this branch.
