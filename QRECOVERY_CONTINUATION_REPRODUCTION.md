# Authorized QRecovery continuation

Decision AUTHORIZED_PROSPECTIVE_REPORTING_FIX_AND_CONTINUATION. Amendment e55b1ed805e7104ccf2f535d168750d2ccd75337 was committed before reporting changes. Scientific implementation remains e9847b72da1db61d2e3d62837897259298614f98; prereg677f32ab81fa08f2d5541bbb2f9c1f9dc87884a2; hard stop7ae4b5986ba7655f1f0b7f4be2a4dfd6ecdf99ad. REPORTING_FIX_SHA is the commit containing the corrected scripts and validated before dispatch; it must never replace the scientific SHA.

Original artifacts/aamas2027_qrecovery/run (including STOP),26original safe evidence files and86private files remain byte-identical. New observations go into continuation/run and a separate private root. No retained cell can appear in the dispatch set: it is computed by membership in original attempt IDs. Original10plus remaining270retain the same280identities and order. No retries, repairs or replacements.

Validation:
```sh
PYTHONPATH=.:/private/tmp/e2_s0_deps /opt/homebrew/bin/python3 scripts/check_qrecovery_reporting_fix.py
PYTHONPATH=.:/private/tmp/e2_s0_deps /opt/homebrew/bin/python3 scripts/run_qrecovery.py --source-root /private/tmp/e2_s0_sources --output artifacts/aamas2027_qrecovery/continuation_preflight --private-output /private/tmp/unused_qrecovery_continuation_preflight --continue-from artifacts/aamas2027_qrecovery/run --preflight-only
```

Once only after reporting-fix commit (substitute full SHA):
```sh
PYTHONPATH=.:/private/tmp/e2_s0_deps /opt/homebrew/bin/python3 scripts/run_qrecovery.py --source-root /private/tmp/e2_s0_sources --provider-env /Users/crazy/Desktop/agent-privacy-defense/FlowFence-Lite/data/secrets/e2_development_20260920/provider.env --private-output /private/tmp/flowfence_qrecovery_continuation_private_20260922 --output artifacts/aamas2027_qrecovery/continuation/run --implementation-commit e9847b72da1db61d2e3d62837897259298614f98 --continue-from artifacts/aamas2027_qrecovery/run --reporting-fix-commit REPORTING_FIX_SHA
```

Read-only combined audit:
```sh
PYTHONPATH=.:/private/tmp/e2_s0_deps /opt/homebrew/bin/python3 scripts/summarize_qrecovery.py --continuation artifacts/aamas2027_qrecovery/continuation/run --output artifacts/aamas2027_qrecovery/combined/derived --report artifacts/aamas2027_qrecovery/combined/report.md
```

All counts use distinct scheduled/attempted/finished ID sets; duplicates raise an integrity error. Finished/in-flight/unattempted are a strict partition. Safe originals and raw prefix are verified before dispatch. Runtime stage requests, recovery policy/provenance, evaluator, privacy and transport remain unchanged. New implementation/provenance/reporting defect means STOP and another human decision; do not automatically patch/resume. Original STOP is historical and never deleted. No paper modification or merge.
