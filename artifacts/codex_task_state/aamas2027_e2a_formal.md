Goal: execute human-approved E2-A partial confirmatory tranche, 40 existing tasks/720 cells; BIRD withdrawn, E2-B deferred.
Branch: codex/aamas2027-e2a-formal, based on585143c.
Completed work: located intact V3/C0 worktree and frozen IDs; added prospective amendment, balanced deterministic schedule, formal admission/metadata adapter, serial once-only runner, saved-evidence auditor. No model calls yet.
Changed files: E2A_PREREGISTRATION_AMENDMENT.md; E2A_FORMAL_CELL_SCHEDULE.json; src/e2_live/e2a.py; scripts/run_e2a_formal.py; scripts/summarize_e2a_formal.py; formal validation/reproduction/report artifacts; research logs; this state.
Validation commands: pending offline formal tests and frozen integrity verification.
Known limitations: E2-A has no P4; only40 semantic tasks; original evaluator/source dependency paths required. V3 frozen files unchanged; formal wrapper corrects only hardcoded historical output metadata. No E2-B authorization.
Resume instructions: before dispatch verify pushed prereg commit. After dispatch NEVER relaunch the runner or rerun cells. Inspect run/status.json and completion.json; implementation defect requires human review, no live repair. Preserve private evidence; regenerate reports from saved evidence only.
