# Codex Task State: p0-eventization

## Goal

Add a P0 eventization adapter for existing adapted AgentPoison full-ReAct results. The adapter converts existing run outputs into unified event traces without changing the existing AgentPoison runner.

## Branch

codex/p0-eventization

## Completed

- Added event and policy-decision JSON schemas.
- Added `scripts/convert_agentpoison_to_events.py`.
- Added a small synthetic AgentPoison fixture.
- Added a standard-library unittest covering converter outputs, MEMORY_READ event creation, policy decision creation, parseability, metric output, and safe-trace redaction.
- Kept the implementation offline and MiniMax-assumption-only; no provider calls or experiments are run.

## Changed Files

- `schemas/event_record.schema.json`
- `schemas/policy_decision.schema.json`
- `scripts/convert_agentpoison_to_events.py`
- `tests/fixtures/agentpoison_case_result_minimal.json`
- `tests/test_convert_agentpoison_to_events.py`
- `artifacts/codex_task_state/codex_p0_eventization.md`

## Validation Commands

- `python scripts/convert_agentpoison_to_events.py --help`
- `python -m unittest tests/test_convert_agentpoison_to_events.py`
- `python -m compileall scripts src`
- `git diff --check`
- `git status --short`

## Known Limitations

- The converter-level metrics are lightweight and are not the final audit/recompute implementation.
- Official ACC/EM are not recomputed from events.
- No real-result event traces are committed.
- No raw trajectories are emitted into safe traces.
- P1 multi-agent event graph, cascade, topology, privilege-reach, and channel-level evaluators are not implemented in this goal.

## Resume Instructions

Resume on branch `codex/p0-eventization`.

First run:

- `git branch --show-current`
- `git status --short`

Then inspect:

- `scripts/convert_agentpoison_to_events.py`
- `tests/test_convert_agentpoison_to_events.py`
- `schemas/event_record.schema.json`
- `schemas/policy_decision.schema.json`

Do not start audit/recompute in this branch.
