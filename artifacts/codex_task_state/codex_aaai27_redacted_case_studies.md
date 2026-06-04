# Codex Task State: aaai27-redacted-case-studies

## Goal

Create redacted qualitative case studies for the FlowFence-Lite AAAI-27 draft from committed high-level evidence. First synchronize the working tree after the human copied polished AAAI draft files into the repository, then generate case-study artifacts without running experiments or calling providers.

## Branch

`codex/aaai27-redacted-case-studies`

## Working Tree Sync

The goal started from `codex/aaai27-draft-v1-substantive-rewrite` with dirty files limited to expected AAAI draft files under `papers/aaai27_flowfence_draft/`. No forbidden raw traces, provider outputs, prompts, policy logs, per-run metrics, `.env` files, or LaTeX build outputs were staged.

The human-copied polished AAAI draft state was committed first:

- Commit: `eb84cb2`
- Message: `docs: import polished AAAI draft state`

## Inputs Inspected

- `AGENTS.md`
- `results/evidence_index/current_evidence_index.md`
- `papers/claims_checklist.md`
- `artifacts/paper_tables/table_3_minimax_3seed_coverage.md`
- `artifacts/paper_tables/table_7_nonoracle_heldout_validation.md`
- `artifacts/paper_tables/table_8_nonoracle_mechanism_ablation.md`
- `artifacts/minimax_p1_coverage_3seed/coverage_summary.json`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_attack_defense.csv`
- `artifacts/minimax_p1_coverage_3seed/failure_breakdown.jsonl`
- `artifacts/nonoracle_heldout_deterministic/summary.json`
- `artifacts/nonoracle_heldout_deterministic/comparison_by_attack_defense.csv`
- `artifacts/nonoracle_heldout_deterministic/failure_breakdown.jsonl`
- `artifacts/minimax_nonoracle_heldout_targeted/summary.json`
- `artifacts/minimax_nonoracle_heldout_targeted/comparison_by_attack_defense.csv`

## Completed Work

- Added `scripts/export_redacted_case_studies.py`.
- Added `tests/test_export_redacted_case_studies.py`.
- Generated four redacted case studies under `artifacts/case_studies/`.
- Generated JSON, combined Markdown, individual case files, traceability notes, and review notes.
- Verified exported artifacts do not contain configured synthetic secret markers.

## Case Studies Created

- Case 1: no-defense workspace propagation leak in blackboard shared-state setting.
- Case 2: prompt-filter failure on held-out paraphrased shared-state exfiltration.
- Case 3: FlowFence safe-view/quarantine containment for workspace poisoning.
- Case 4: non-oracle FlowFence prevention on held-out paraphrase without attack labels.

## Safe Trace Availability

Safe trace snippets were requested from `/tmp/flowfence_mas_p1_coverage_3seed_252run`, but that run root was not available locally. The generated case studies therefore use committed high-level summaries only and record `safe trace unavailable`.

## Validation Commands

- `python scripts/export_redacted_case_studies.py --help`
- `python -m unittest tests/test_export_redacted_case_studies.py`
- `python scripts/export_redacted_case_studies.py --output-dir artifacts/case_studies --summary-root artifacts --runs-root /tmp/flowfence_mas_p1_coverage_3seed_252run --include-safe-trace-snippets --strict`

Additional validation should include:

- `python -m compileall scripts src`
- `git diff --check`
- `git status --short`

## Known Limitations

- Case studies are qualitative drafting aids, not new experiment evidence.
- Safe trace snippets were unavailable locally, so the cases are summary-only.
- Evidence remains MiniMax-only where real-provider evidence is represented.
- Evidence remains scoped to synthetic deterministic MAS runtime.
- No production safety, real browser/desktop computer-use, arbitrary attack robustness, or non-MiniMax generalization is supported.

## Resume Instructions

If continuing this goal, inspect `artifacts/case_studies/`, rerun the exporter if safe trace snippets become available, and keep all outputs redacted. Do not read full traces, prompts, provider responses, policy logs, per-run metrics from generated run directories, or secrets.
