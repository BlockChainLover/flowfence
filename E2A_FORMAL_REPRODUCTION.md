# E2-A reproduction and no-rerun instructions

Formal partial tranche:40 public tasks,720 observations, unchangedV3. All paths below are repository-relative except locally retained source/dependencies/private storage. Frozen historical source/dependency recovery instructions remain in E2_D3_CONTINUATION_REPRODUCTION.md and E2_S1R_REPRODUCTION.md.

Offline validation (zero provider calls; fixture outputs are not evidence):
```sh
PYTHONPATH=.:/private/tmp/e2_s0_deps /opt/homebrew/bin/python3 scripts/check_e2a_formal.py --source-root /private/tmp/e2_s0_sources --output /private/tmp/e2a_offline_validation.json
```

Live invocation ONCE ONLY after amendment/schedule/runner are committed and pushed. Substitute the exact preregistration commit, subsequently recorded in `artifacts/aamas2027_e2a_formal/run/registration.json`. Do not invoke this command again after any cell starts; no resume or scientific rerun is authorized.
```sh
PYTHONPATH=.:/private/tmp/e2_s0_deps /opt/homebrew/bin/python3 scripts/run_e2a_formal.py --source-root /private/tmp/e2_s0_sources --provider-env /Users/crazy/Desktop/agent-privacy-defense/FlowFence-Lite/data/secrets/e2_development_20260920/provider.env --private-output /Users/crazy/Desktop/agent-privacy-defense/FlowFence-Lite/data/secrets/e2a_formal_20260921 --output artifacts/aamas2027_e2a_formal/run --prereg-commit E2A_FORMAL_PREREG_COMMIT
```

Registration must contain `namespace=E2A_FORMAL_CONFIRMATORY`, formal evidence label, exact720schedule and remotely verified preregcommit. The frozen V3 module/config still contains historical development metadata; only the formal wrapper overrides public namespace/label after unchanged execution. No prompt, request, scoring, privacy, defense or treatment behavior is modified. PostgreSQL is not required or started.

Read-only saved-evidence recomputation, never a model/evaluator dispatch:
```sh
PYTHONPATH=.:/private/tmp/e2_s0_deps /opt/homebrew/bin/python3 scripts/summarize_e2a_formal.py --run artifacts/aamas2027_e2a_formal/run --private /Users/crazy/Desktop/agent-privacy-defense/FlowFence-Lite/data/secrets/e2a_formal_20260921 --output artifacts/aamas2027_e2a_formal/derived
```

`run/status.json` is progress only; `completion.json` marks terminal scheduler status. `STOP` stops new cells; preserve any already-in-flight cell. Any implementation defect requires human review, no live patches or reruns. Ordinary model/provider/policy/context failures remain formal observations. Privacy UNKNOWN is not safety. All full trajectories, evaluator inputs/outputs, request/response details remain in the ignored private root with700/600modes; safe results retain original metric vectors and digests. No credentials included in indices or Git.

After720attempts or hard stop, audit saved evidence, create E2A_FORMAL_REPORT.md, commit only safe summaries and return for human scientific review. E2-B remains DEFERRED_NOT_SELECTED. Do not use E2-A outcomes for later source/task/fact/evaluator selection.
