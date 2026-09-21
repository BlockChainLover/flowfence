# E2-A authorized continuation and combined audit

Human authorizes only reporting correction plus cells054–720. Original001–053 are immutable valid formal evidence. Never relaunch the original run, remove its STOP, rewrite its registration, or rerun a completed cell.

First execute the zero-call regression command in E2A_REPORTING_FIX_AUDIT.md. Commit and push correction/tests/continuation tooling. Record verified remote commit as E2A_REPORTING_FIX_COMMIT.

Invoke ONCE after the fix is pushed, substituting its exact full commit:
```sh
PYTHONPATH=.:/private/tmp/e2_s0_deps /opt/homebrew/bin/python3 scripts/run_e2a_continuation.py --source-root /private/tmp/e2_s0_sources --provider-env /Users/crazy/Desktop/agent-privacy-defense/FlowFence-Lite/data/secrets/e2_development_20260920/provider.env --private-output /Users/crazy/Desktop/agent-privacy-defense/FlowFence-Lite/data/secrets/e2a_formal_continuation_054_720_20260921 --output artifacts/aamas2027_e2a_continuation/run --reporting-fix-commit E2A_REPORTING_FIX_COMMIT
```

The runner requires new output/private directories, correct pushed branch HEAD and unchanged original evidence/scientific files. It schedules only054..720; zero retries/repairs/replacements. Another implementation defect stops new cells for human review. Never automatically patch/resume. No PostgreSQL/BIRD/E2-B execution.

Read-only combined audit, allowed during or after execution:
```sh
PYTHONPATH=.:/private/tmp/e2_s0_deps /opt/homebrew/bin/python3 scripts/summarize_e2a_combined.py --continuation artifacts/aamas2027_e2a_continuation/run --output artifacts/aamas2027_e2a_combined
PYTHONPATH=. /opt/homebrew/bin/python3 scripts/report_e2a_formal.py --root artifacts/aamas2027_e2a_combined --report E2A_FORMAL_REPORT.md
```

The combined_index.json maps each cell to its immutable run and private trajectory. Original artifacts/aamas2027_e2a_formal/ is NEVER overwritten; corrected or combined summaries go to a new root. Original raw root is taken from original registration; continuation raw root from its registration. Raw requests/responses/evaluator inputs stay local/ignored, directories700/files600. Retain safe provider metadata, trajectory digests, source metric vectors, stage/release/treatment/privacy/task/failure summaries. No secrets or large full trajectories in Git.

Final expected720observations from40tasks; after completion stop for human scientific review. Report historical reporting defect corrected, and any new defects separately. Do not select E2-B based on E2-A outcomes or change frozen acceptance criteria.
