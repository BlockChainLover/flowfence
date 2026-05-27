# Codex Task State: p0-failure-case-export

## Goal

Add P0 failure-case and false-positive export for AgentPoison event traces produced by `scripts/convert_agentpoison_to_events.py` and audited by `scripts/audit_events.py`.

## Branch

codex/p0-failure-case-export

## Completed

- Added `scripts/export_agentpoison_failure_cases.py`.
- Added deterministic JSONL, Markdown, and summary JSON report generation.
- Added false-positive and adversarial-failure taxonomy handling.
- Added privacy hygiene that consumes converted event previews only and avoids raw trajectory fields.
- Added `tests/test_export_agentpoison_failure_cases.py`.
- Kept the goal offline; no provider calls, no model runs, no runner changes, and no result JSON edits.

## Changed Files

- `scripts/export_agentpoison_failure_cases.py`
- `tests/test_export_agentpoison_failure_cases.py`
- `artifacts/codex_task_state/codex_p0_failure_case_export.md`

## Validation Commands

- `python scripts/export_agentpoison_failure_cases.py --help`
- `python -m unittest tests/test_export_agentpoison_failure_cases.py`
- `python -m compileall scripts src`
- `git diff --check`
- `git status --short`

## Known Limitations

- Exported failure rows are derived from converted event traces only.
- This goal does not inspect original raw result files or trajectories.
- This goal does not compute new metrics beyond report summary counts.
- This goal does not start P1 synthetic MAS runtime.
- Real-result validation outputs, if generated, are local-only and not committed.

## Resume Instructions

Resume on branch `codex/p0-failure-case-export`.

First run:

- `git branch --show-current`
- `git status --short`

Then inspect:

- `scripts/export_agentpoison_failure_cases.py`
- `tests/test_export_agentpoison_failure_cases.py`

Do not start P1 synthetic MAS runtime in this branch.
