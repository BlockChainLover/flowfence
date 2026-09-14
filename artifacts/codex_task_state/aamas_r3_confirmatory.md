# AAMAS R3 — preregistration preparation, no provider calls yet

- Goal: final held-out confirmation of frozen PAPC-R2 versus IFC;108 episodes, then NO MORE EXPERIMENTS.
- Branch: codex/aamas2027-experiment-extension; START_HEAD89fbb3e68655d82877b73c7cd5837b3019b64215, clean local/fetched remote equal.
- Checkout: /private/tmp/flowfence-aamas-r11-w4EWq4Ac. Original desktop dirty checkout untouched.
- Completed: frozen input inventory, exact user A/B attack configuration, additive R3 inherited episode/paired runner/summary/audit, full54-pair schedule,108-cell zeroAPI dry run, freeze/fairness/old-artifact assertions and tests. No live pilot permitted.
- Changed files: src/experiments/aamas_binding_r3.py; scripts/run_aamas_binding_r3.py, summarize_aamas_binding_r3.py, audit_aamas_binding_r3.py; r3_formal/r3_heldout_attacks configs; tests/test_aamas_binding_r3.py; R3_EXPERIMENT_PREREGISTRATION.md/R3_FROZEN_INPUTS.json/R3_SCHEDULE.json/R3_validation; roadmap/progress and this state.
- Validation commands: PYTHONPATH=. /private/tmp/flowfence-r11-python/bin/python -m pytest tests/test_aamas_*.py -q; relevant MAS/runtime suite; full pytest; R3 runner --dry-run; R3 summarizer/auditor; source SHA256/prior-config/old-artifact/safe scan; git diff --check.
- Known limitations: one enterprise task family; held out from experimental wording, not detector vocabulary; task-critical structured input separate from quarantined note; no novel/general confidentiality; unchanged legacy exporter missing claims_checklist failure.
- Resume: commit/push preregistration and verify remote SHA BEFORE R3 API. New isolated server clone from retained R2 clone plus incremental Git bundle; existing external credential env referenced in place. Then only108 formal episodes, fresh output and private directory,54 pairs sequentially with two concurrent defenses. No live pilot, replacements, E5, second model, extra wording/replicate, paper edit or merge. Retain all evidence, final push, stop for Independent Review.

- Final pre-API validation:26 R3 /208 AAMAS /44 relevant passed; full276 passed,1 pre-existing exporter failure;0 skipped/xfail. Dry108/108, no API.
