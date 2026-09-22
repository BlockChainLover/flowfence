# QRecovery reproduction and no-rerun record

Worktree: /private/tmp/flowfence-qrecovery. Branch: codex/aamas2027-qrecovery. Python: /opt/homebrew/bin/python3 (3.14.7), PYTHONPATH=.:/private/tmp/e2_s0_deps. Public pinned source root: /private/tmp/e2_s0_sources. Model/provider/request configuration remains experiments/e2_pilot_config_p1/LIVE_MODEL_CONFIG.json, MiniMax-M2.7, original temperature0/top_p0.9/8192token limit, zero retries. Original source evaluators and all historical source pins unchanged.

Preregistration commit:677f32a (resolve via git rev-parse); implementation SHA is recorded in run/registration.json and must match dispatch HEAD. Historical base342599f8e6884bafb333fa0bf99b0543352d88ed. Artifact root artifacts/aamas2027_qrecovery. Private traces live outside Git under /private/tmp/flowfence_qrecovery_private_20260922, directories700/files600. Keep this directory for raw-evidence audit. No credentials are copied into it or Git.

Zero-call validation:
```sh
PYTHONPATH=.:/private/tmp/e2_s0_deps /opt/homebrew/bin/python3 scripts/check_qrecovery.py --output artifacts/aamas2027_qrecovery/unit_preflight.json
PYTHONPATH=.:/private/tmp/e2_s0_deps /opt/homebrew/bin/python3 scripts/run_qrecovery.py --source-root /private/tmp/e2_s0_sources --output artifacts/aamas2027_qrecovery --private-output /private/tmp/unused_qrecovery_preflight --preflight-only
```

Single live invocation AFTER implementation commit (replace IMPLEMENTATION_SHA with actual HEAD, recorded before dispatch):
```sh
PYTHONPATH=.:/private/tmp/e2_s0_deps /opt/homebrew/bin/python3 scripts/run_qrecovery.py --source-root /private/tmp/e2_s0_sources --provider-env /Users/crazy/Desktop/agent-privacy-defense/FlowFence-Lite/data/secrets/e2_development_20260920/provider.env --private-output /private/tmp/flowfence_qrecovery_private_20260922 --output artifacts/aamas2027_qrecovery/run --implementation-commit IMPLEMENTATION_SHA
```

Expected280: clean40first, then contaminated240. Existing720never run. Each identity once. STOP/implementation defect means preserve all files and wait for human review; never remove STOP, relaunch, retry, repair or replace. Existing output directories intentionally prevent resumption. Store full actual command and resolved SHAs with final delivery. Hashes are retained in episode trajectory references and historical pin manifests.
