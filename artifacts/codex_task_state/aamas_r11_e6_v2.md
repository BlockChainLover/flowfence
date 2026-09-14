# AAMAS R1.1 E6-v2 completion

- Goal: complete the approved engineering-only E6-v2 work package, then stop for independent review.
- Branch: codex/aamas2027-experiment-extension.
- Isolated checkout: /private/tmp/flowfence-aamas-r11-w4EWq4Ac; starting local/remote 393fbf98e96cf6306aac2904529c13d6598ef71f; initially clean.
- Original directory touched: NO; mutations: 0. Never resume in the dirty original checkout.
- Completed work: verified clean remote source and frozen inputs; v2 configs, transport-only retries, parsed-action instrumentation, pilot gate, dry-run and regression tests.
- Changed files: src/experiments/aamas_binding_v2.py; scripts/run_aamas_binding_v2.py; tests/test_aamas_binding_v2.py; two e6_v2 configs; R1_1_ENGINEERING_AMENDMENT.md; R1_1_validation/; this state; progress/roadmap; dry-run registration/completion; .gitignore for v2 local dry traces.
- Validation commands: PYTHONPATH=. /private/tmp/flowfence-r11-python/bin/python -m pytest tests/test_aamas_*.py -q; relevant MAS/runtime suite; full pytest; scripts/run_aamas_binding_v2.py --help and --dry-run; direct hashes and Git byte comparisons.
- Known limitations: no R1.1 model calls yet. One existing exporter failure missing papers/claims_checklist.md. No second-model/domain/general semantic claim. Provider credentials exist only on wentian-server and are read there in place.
- Resume instructions: push preregistration before any API. Stage the pushed Git revision in a fresh isolated remote execution clone; use external provider env. Pilot 3/3 is required before 108-cell formal. Stop on insufficient pilot. Preserve evidence, final normal push, keep PR OPEN/Draft. No E5, second model, paper body changes or merge.
