# Codex Task State: rq2-topology-table-review

## Goal

Extract an auditable RQ2 topology table for the current AAAI paper draft using existing fixed FlowFence-Lite benchmark settings.

## Branch

`codex/aaai27-claims-results-sync`

## Completed Work

- Reread `research/contract/`, `research/logs/roadmap.md`, and `research/logs/progress.md` per repo instructions.
- Inspected the current AAAI draft RQ2 wording in `papers/aaai27_flowfence_draft/sections/05_results.tex`.
- Confirmed that the repo had claim-audit references for deterministic topology evidence, but no ready-to-paste topology table with `cascade_depth`.
- Reran the fixed deterministic strengthened MAS matrix locally with provider calls disabled.
- Summarized the rerun and extracted three candidate topology slices:
  - recommended no-defense attack-positive aggregate,
  - alternate `workspace_poisoning_indirect` no-defense slice,
  - full mixed 252-run by-topology aggregate for sanity only.
- Saved the review tables under `artifacts/paper_tables/`.

## Changed Files

- `artifacts/mas_p1_deterministic_matrix/status.json`
- `artifacts/paper_tables/table_rq2_topology_candidate.md`
- `artifacts/paper_tables/table_rq2_topology_candidate.csv`
- `artifacts/codex_task_state/codex_rq2_topology_table_review.md`
- `research/logs/progress.md`

## Validation Commands

- `PYTHONPATH=. python3 src/runner/sweep_mas.py --config configs/experiment/mas_p1_strengthened_matrix.yaml --output-root /private/tmp/flowfence_rq2_topology_strengthened --force`
- `PYTHONPATH=. python3 src/runner/summarize_mas_p1.py --runs-root /private/tmp/flowfence_rq2_topology_strengthened --output-dir /private/tmp/flowfence_rq2_topology_strengthened_summary --matrix-config configs/experiment/mas_p1_strengthened_matrix.yaml`
- `python3` inline aggregation over `/private/tmp/flowfence_rq2_topology_strengthened_summary/summary.json`
- `git status --short`

## Known Limitations

- The extracted RQ2 table is deterministic synthetic-runtime evidence only.
- `privilege_reach` saturates at `5.0` in the recommended no-defense attack-positive slice, so the current table does not show topology separation on that metric.
- The committed historical artifacts did not expose a ready-to-use per-topology `cascade_depth` table, so the local deterministic rerun was needed to reconstruct it cleanly.
- The full 252-run mixed by-topology aggregate is not recommended for main text because it mixes topology with defense effects and includes `attack=none` rows.

## Resume Instructions

1. Check branch and worktree state with `git branch --show-current` and `git status --short`.
2. Review the candidate table artifact at `artifacts/paper_tables/table_rq2_topology_candidate.md`.
3. If the user approves one slice, wire that slice into the AAAI draft as a new table or inline mini-table near RQ2.
4. Keep the caveat that the evidence is deterministic synthetic-runtime only unless a MiniMax-backed topology-specific table is added separately.
