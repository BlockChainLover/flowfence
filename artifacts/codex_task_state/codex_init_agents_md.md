# Codex Task State: init-agents-md

## Goal

Create or update repository-level `AGENTS.md` so future Codex tasks follow stable project rules, MiniMax-only experiment constraints, safe version control, and evidence-based claim discipline.

## Branch

codex/init-agents-md

## Completed

- Preserved the existing research operating guide in `AGENTS.md`.
- Added FlowFence-Lite project identity, current phase sequence, MiniMax-only provider constraint, version-control rules, research discipline, engineering discipline, safety/privacy discipline, durable task-state requirements, and final response format.
- Created this durable task-state file.

## Changed Files

- `AGENTS.md`
- `artifacts/codex_task_state/codex_init_agents_md.md`

## Validation Commands

- `git diff --check`
- `python -m compileall src scripts || true`
- `git status --short`

## Known Limitations

- This goal only initializes repository-level Codex instructions.
- It does not create the P0 evidence index.
- It does not modify implementation code.
- It does not run experiments.
- It does not edit results or paper drafts.

## Resume Instructions

Resume on branch `codex/init-agents-md`.

First run:

- `git branch --show-current`
- `git status --short`

Then inspect:

- `AGENTS.md`
- `artifacts/codex_task_state/codex_init_agents_md.md`

Do not start the next goal in this branch.
