# Codex Task State: p1-real-minimax-coverage

## Goal

Run a bounded MiniMax-only P1 MAS coverage experiment beyond the prior 18-run smoke, then commit only high-level summaries, tables, and a run manifest.

## Branch

`codex/p1-real-minimax-coverage`

## Credential Availability Check

- Local MiniMax credentials: absent.
- Remote MiniMax credentials on `wentian-server`: present after sourcing the existing remote provider environment.
- No credential values were printed or copied locally.

## Config Check

- Main config: `configs/experiment/mas_p1_minimax_coverage.yaml`
- Expected run count: 84
- Matrix: 3 topologies x 7 attacks x 4 defenses x seed 1
- Provider: `minimax`
- Provider calls enabled: true
- Agent backend: `minimax_final_writer`
- Optional config prepared but not run: `configs/experiment/mas_p1_minimax_coverage_3seed.yaml`
- Optional expected run count: 252

## Provider-call Safety Check

The coverage sweep without `--allow-provider-calls` failed before any MiniMax request, as expected.

Command:

```bash
PYTHONPATH=. python3 src/runner/sweep_mas.py --config configs/experiment/mas_p1_minimax_coverage.yaml --output-root /tmp/flowfence_mas_p1_coverage_safety --max-runs 1
```

Observed result:

- Exit code: 2
- Message: `provider_calls_enabled=true requires --allow-provider-calls before any MiniMax request`

## Pilot 6-run Result

- Executed: yes
- Output root: `/tmp/flowfence_mas_p1_coverage_pilot6`
- Completed runs: 6
- Failed runs: 0
- Task success rate: 1.0
- Unauthorized raw leakage mean: 0.666667
- External leakage mean: 0.0
- Cascade size mean: 1.666667
- Privilege reach mean: 1.666667

## Coverage 84-run Result

- Executed: yes
- Output root: `/tmp/flowfence_mas_p1_coverage_84run`
- Completed runs: 84
- Failed runs: 0
- Provider: MiniMax
- Provider calls enabled: true
- Agent backend: `minimax_final_writer`
- Task success rate: 0.952381
- Unauthorized raw leakage mean: 2.988095
- External leakage mean: 0.380952
- Cascade size mean: 4.178571
- Privilege reach mean: 2.678571
- Topology effect observed: true

## Committed Evidence Files

- `artifacts/minimax_p1_coverage/README.md`
- `artifacts/minimax_p1_coverage/run_manifest.json`
- `artifacts/minimax_p1_coverage/coverage_summary.json`
- `artifacts/minimax_p1_coverage/coverage_summary.md`
- `artifacts/minimax_p1_coverage/coverage_by_defense.csv`
- `artifacts/minimax_p1_coverage/coverage_by_defense.md`
- `artifacts/minimax_p1_coverage/coverage_by_topology.csv`
- `artifacts/minimax_p1_coverage/coverage_by_topology.md`
- `artifacts/minimax_p1_coverage/coverage_by_attack.csv`
- `artifacts/minimax_p1_coverage/coverage_by_attack.md`
- `artifacts/minimax_p1_coverage/coverage_by_attack_defense.csv`
- `artifacts/minimax_p1_coverage/coverage_by_attack_defense.md`
- `artifacts/minimax_p1_coverage/failure_breakdown.jsonl`

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
- The coverage uses one seed only.
- The 252-run three-seed config was created but not run.
- Raw traces and raw provider outputs are intentionally not committed.
- Non-MiniMax generalization and production safety remain unsupported.

## Resume Instructions

Use `artifacts/minimax_p1_coverage/coverage_summary.json` and the coverage tables for high-level evidence review. Do not inspect or commit raw provider outputs. The likely next step is a claims refresh if the 84-run evidence is accepted, or a 252-run follow-up only under a separate explicit goal.
