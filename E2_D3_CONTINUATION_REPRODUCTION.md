# D3 continuation reproduction and no-rerun rule

Prospective human authorization permits cells002–054 only. Cell001 stays immutable in artifacts/aamas2027_e2_v3_d3_live/run/ and the original private root. Never relaunch the old run; never dispatch001. Preserve scientific namespace E2_DEVELOPMENT_V3_D3 and distinguish run_instance_id E2_DEVELOPMENT_V3_D3_CONTINUATION_001.

First run the offline commands in D3_REGISTRATION_FIX_AUDIT.md. Commit and push the metadata fix. Then execute the following ONCE, substituting the verified remote full fix commit:
```sh
PYTHONPATH=.:/private/tmp/e2_s0_deps /opt/homebrew/bin/python3 scripts/run_e2_d3_live.py --source-root /private/tmp/e2_s0_sources --schema /private/tmp/e2_s1r_schema.json --provider-env /Users/crazy/Desktop/agent-privacy-defense/FlowFence-Lite/data/secrets/e2_development_20260920/provider.env --private-output /Users/crazy/Desktop/agent-privacy-defense/FlowFence-Lite/data/secrets/e2_development_v3_d3_continuation_20260921/raw --output artifacts/aamas2027_e2_v3_d3_continuation/run --first-runner-commit 792620bb7cea6ac1e697aaae5f2fe721a1ba37b5 --registration-fix-commit VERIFIED_REMOTE_FIX_COMMIT
```
The CLI refuses existing output paths, checks remote commit and frozen original evidence before dispatch, and writes corrected registration/preflight. It uses the existing authorized ignored credential in place, no copy/display. Private directories/files use700/600. Further implementation defects stop new cells; ordinary failures remain observations. Never patch/retry after another defect.

Combined analysis must read both roots without modifying either; a derived index maps each cell to run instance, original files and metadata-defect status. The original001 keeps metadata defect=true; continuation cells=false. No invented corrected historical registration. No model or evaluator call is permitted during recomputation. Final readiness stops at human review; no confirmatory run.

Actual registration fix commit: cdf4a26558ecad62c3799f91e243c69ae8a16c80 (verified remote before dispatch). Continuation preflightPASS is saved in its run/preflight.json. The live invocation has been started once; do not relaunch.

Combined saved-evidence audit:
```sh
PYTHONPATH=.:/private/tmp/e2_s0_deps /opt/homebrew/bin/python3 scripts/summarize_e2_d3_combined.py --continuation artifacts/aamas2027_e2_v3_d3_continuation/run --output artifacts/aamas2027_e2_v3_d3_combined
```
It creates only temporary derived input/link views, invokes the unchanged saved-evidence auditor, and maps every private index path back to its real original run root before publishing the combined index. No original registration, episode, trajectory or scientific outcome is edited. Cell001 metadata defect remains true in combined_index.json and summary.json. Other cells identify their actual continuation run instance.

## Completed continuation

Cells002–054 all completed once. Combined54observations retain original001and its metadata defect. Final report E2_D3_COMBINED_DEVELOPMENT_REPORT.md; combined evidence artifacts/aamas2027_e2_v3_d3_combined/. The live process has exited and its dedicated PostgreSQL cluster is stopped. Only the saved-evidence audit command is suitable for recomputation; neither live command may be relaunched under this completed authorization.
