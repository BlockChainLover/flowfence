# Codex Task State: p0-audit-and-recompute

## Goal

Add P0 event audit and metric recomputation scripts for AgentPoison event traces produced by the existing p0-eventization adapter.

## Branch

codex/p0-audit-and-recompute

## Completed

- Added `scripts/audit_events.py` for JSONL parseability, schema-field, policy-decision alignment, safe-trace hygiene, exposure traceability, event ordering, and event-count audits.
- Added `scripts/recompute_agentpoison_metrics_from_events.py` for lightweight event-derived containment metric recomputation.
- Added `scripts/compare_metrics.py` for top-level numeric JSON metric comparison.
- Added `tests/test_audit_and_recompute_agentpoison_events.py` using the existing synthetic fixture and converter.
- Kept all scripts offline; no provider calls, model calls, new experiments, or runner modifications are performed.

## Changed Files

- `scripts/audit_events.py`
- `scripts/recompute_agentpoison_metrics_from_events.py`
- `scripts/compare_metrics.py`
- `tests/test_audit_and_recompute_agentpoison_events.py`
- `artifacts/codex_task_state/codex_p0_audit_and_recompute.md`

## Validation Commands

- `python scripts/audit_events.py --help`
- `python scripts/recompute_agentpoison_metrics_from_events.py --help`
- `python scripts/compare_metrics.py --help`
- `python -m unittest tests/test_audit_and_recompute_agentpoison_events.py`
- `python -m compileall scripts src`
- `git diff --check`
- `git status --short`

## Known Limitations

- Recomputed metrics are event-derived containment metrics only.
- Official ACC/EM are not recomputed from events.
- This goal does not export failure cases.
- This goal does not modify or validate the existing AgentPoison runner.
- This goal does not create or commit real-result event traces.
- P1 multi-agent propagation, topology, cascade, privilege-reach, and channel-level evaluations remain unimplemented.

## Resume Instructions

Resume on branch `codex/p0-audit-and-recompute`.

First run:

- `git branch --show-current`
- `git status --short`

Then inspect:

- `scripts/audit_events.py`
- `scripts/recompute_agentpoison_metrics_from_events.py`
- `scripts/compare_metrics.py`
- `tests/test_audit_and_recompute_agentpoison_events.py`

Do not start failure-case export in this branch.
