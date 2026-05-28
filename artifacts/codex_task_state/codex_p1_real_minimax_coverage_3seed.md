# Codex Task State: p1-real-minimax-coverage-3seed

## Goal

Run the prepared MiniMax-only P1 MAS 3-seed coverage matrix and commit only high-level summaries, seed breakdowns, FlowFence clean matrix, aggregate tables, and run manifest.

## Branch

`codex/p1-real-minimax-coverage-3seed`

## Credential Availability Check

- Local MiniMax credentials: absent.
- Remote MiniMax credentials on `wentian-server`: present after sourcing the existing remote provider environment.
- No credential values were printed or copied locally.

## Config Check

- Config: `configs/experiment/mas_p1_minimax_coverage_3seed.yaml`
- Expected run count: 252
- Matrix: 3 topologies x 7 attacks x 4 defenses x 3 seeds
- Topologies: `chain_4`, `star_4`, `blackboard_4`
- Attacks: `none`, `summary_poisoning_direct`, `summary_poisoning_indirect`, `workspace_poisoning_direct`, `workspace_poisoning_indirect`, `comm_hijack_direct`, `comm_hijack_indirect`
- Defenses: `none`, `static_acl`, `prompt_filter`, `flowfence_lite`
- Seeds: `1`, `2`, `3`
- Provider: `minimax`
- Provider calls enabled: true
- Agent backend: `minimax_final_writer`

## Provider-call Safety Check

The coverage sweep without `--allow-provider-calls` failed before any MiniMax request, as expected.

Command:

```bash
PYTHONPATH=. python3 src/runner/sweep_mas.py --config configs/experiment/mas_p1_minimax_coverage_3seed.yaml --output-root /tmp/flowfence_mas_p1_coverage_3seed_safety --max-runs 1
```

Observed result:

- Exit code: 2
- Message: `provider_calls_enabled=true requires --allow-provider-calls before any MiniMax request`

## Pilot 12-run Result

- Executed: yes
- Output root: `/tmp/flowfence_mas_p1_coverage_3seed_pilot12`
- Completed runs: 12
- Failed runs: 0
- Task success rate: 1.0
- Unauthorized raw leakage mean: 0.0
- External leakage mean: 0.0
- Cascade size mean: 0.0
- Privilege reach mean: 0.0

## Coverage 252-run Result

- Executed: yes
- Output root: `/tmp/flowfence_mas_p1_coverage_3seed_252run`
- Completed runs: 251
- Failed runs: 1
- Failed run: `mas_p1__enterprise_assistant_001__chain_4__summary_poisoning_direct__prompt_filter__seed1`
- Failure category: MiniMax read timeout
- Provider: MiniMax
- Provider calls enabled: true
- Agent backend: `minimax_final_writer`
- Task success rate: 0.964143
- Unauthorized raw leakage mean: 2.840637
- External leakage mean: 0.326693
- Cascade size mean: 4.183267
- Privilege reach mean: 2.689243
- Topology effect observed: true
- FlowFence clean runs: 63/63

## Committed Evidence Files

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

## Validation Commands

```bash
PYTHONPATH=. python src/runner/sweep_mas.py --help
PYTHONPATH=. python src/runner/summarize_mas_p1.py --help
python scripts/audit_minimax_coverage.py --help
python -m unittest tests/test_minimax_coverage_config.py
python -m unittest tests/test_audit_minimax_coverage.py
python -m unittest tests/test_mas_minimax_smoke_config.py
python -m compileall scripts src
git diff --check
git status --short
```

## Known Limitations

- This is MiniMax-only evidence.
- One configured run failed due to a MiniMax read timeout.
- Raw traces and raw provider outputs are intentionally not committed.
- Non-MiniMax generalization and production safety remain unsupported.
- Claims should be refreshed before paper-facing use.

## Resume Instructions

Use `artifacts/minimax_p1_coverage_3seed/coverage_summary.json`, the seed breakdown, and the FlowFence clean matrix for evidence review. Do not inspect or commit raw provider outputs. Because one run timed out, the likely next step is either a targeted debug/rerun decision or a conservative claims refresh that records the timeout.
