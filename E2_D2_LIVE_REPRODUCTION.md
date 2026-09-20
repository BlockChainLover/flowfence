# E2 V2 D2 live reproduction and admission

Human authorized exactly the frozen54 E2_DEVELOPMENT_V2_D2 cells on 2026-09-20. D1 head6c56e87bc7111e38502dd83f6f5ca1b094b6af9a and selection rule2acf2059c6b572f85188461cd50e1ad06627334d are immutable. No V1 continuation/rerun or confirmatory dispatch. All ordinary failures remain observations. No automatic retry, repair or resume.

The new CLI binds D2-only IDs, exact full cell objects, V2 Episode and LiveProviderV2, original evaluators and frozen schedule. Admission rejects all69 V1/confirmatory IDs plus arbitrary IDs and malformed cell identities. ObservedD2Episode only observes calls to the original V2 service once; it does not change scheduler, prompts, release or scoring. It separately captures submitted-to-B2, released, delivered and quarantined treatment states. Surface reachability is actual B2 entry, including quarantine, never mere intention. A handoff without required treatment entry is an implementation stop. Public summaries contain no payloads; raw evidence is local mode600/700 only.

Pre-run:
```bash
PYTHONPATH=.:/private/tmp/e2_s0_deps python3 scripts/check_e2_d2_admission.py --source-root /private/tmp/e2_s0_sources --schema /private/tmp/e2_s1r_schema.json --output artifacts/aamas2027_e2_v2_d2_live/admission_validation.json
PYTHONPATH=.:/private/tmp/e2_s0_deps python3 scripts/check_e2_d2_environment.py --source-root /private/tmp/e2_s0_sources --schema /private/tmp/e2_s1r_schema.json --output artifacts/aamas2027_e2_v2_d2_live/environment_validation.json
```

Live command, exactly once after runner commit (substitute recorded full commit):
```bash
PYTHONPATH=.:/private/tmp/e2_s0_deps python3 scripts/run_e2_d2_live.py --source-root /private/tmp/e2_s0_sources --schema /private/tmp/e2_s1r_schema.json --provider-env /Users/crazy/Desktop/agent-privacy-defense/FlowFence-Lite/data/secrets/e2_development_20260920/provider.env --private-output /Users/crazy/Desktop/agent-privacy-defense/FlowFence-Lite/data/secrets/e2_development_v2_d2_20260920/raw --output artifacts/aamas2027_e2_v2_d2_live/run --first-runner-commit RECORDED_D2_FIRST_LIVE_RUNNER_COMMIT
```

Credentials are read in place from the previously authorized local ignored file; no copy or display. This command refuses existing outputs and cannot resume. Do not relaunch it. STOP in the run directory stops the next cell while the current episode finishes. Any implementation defect stops new cells automatically; preserve raw and safe observations, no patch/rerun after first D2 outcome. Read-only postrun audits may add reports without changing live code. No live execution beyond54cells, even if review-ready.
