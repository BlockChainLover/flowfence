# AAMAS R2 — semantic-request quarantine repair

- Goal: post-observation PAPC quarantine repair and fixed36-episode MiniMax discrimination test, then Independent Review.
- Branch: codex/aamas2027-experiment-extension.
- START_HEAD: 5a900505548a1315c40c7ba3f6529c08829079d3. Local and fetched GitHub equal, clean.
- Checkout: /private/tmp/flowfence-aamas-r11-w4EWq4Ac (the clean isolated clone retained from R1.1). Original desktop dirty checkout untouched.
- Completed work: R1.1 safe-record diagnosis; versioned marker-only quarantine inspector; additive episode/runner/summary/private-audit; fixed R2 configs;40 new tests;36-cell zero-API dry run; fairness and byte-preservation checks; preregistration documents.
- Changed files: src/defenses/mas_flowfence_r2.py; src/experiments/aamas_binding_r2.py; four R2 scripts (run, summarize, diagnose, audit); tests/test_aamas_binding_r2.py; configs r2_formal/r2_pilot; R2 docs/validation/compact dry artifacts; .gitignore; roadmap/progress; this state. All old source/config/artifacts unchanged.
- Validation commands: PYTHONPATH=. /private/tmp/flowfence-r11-python/bin/python -m pytest tests/test_aamas_*.py -q; relevant MAS/runtime suite; full pytest; scripts/diagnose_aamas_r2.py; scripts/run_aamas_binding_r2.py --dry-run; scripts/summarize_aamas_binding_r2.py; --help; direct byte/fairness/safe scan.
- Known limitations: method changed after observing R1.1; configured-pattern scope only; unrecognized representations still evade unchanged detector. Existing full-suite exporter failure on missing papers/claims_checklist.md. No R2 provider calls yet.
- Resume instructions: commit/push preregistration and verify remote before live pilot. Stage only pushed Git source in fresh remote R2 clone, reference existing external provider env, private output outside repo. Pilot must be3/3 correct with no length; P2 marker-only/no residual/zero reconstructable delivered. Otherwise STOP. On pass run only36 formal cells; no E5, second model, old E6-v2 formal, paper-body edits or merge. Preserve R1/R1.1 negatives and final normal push, PR OPEN/Draft.
