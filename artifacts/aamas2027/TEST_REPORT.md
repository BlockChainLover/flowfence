# Validation report

- Targeted AAMAS:64passed,0failed,0skipped,0xfail.
- Relevant MAS/runtime regression:98passed,0failed,0skipped,0xfail (before3additional packaging tests; those pass in final targeted/full runs).
- Full repository:132passed,1failed,0skipped,0xfail.
- Known pre-existing failure: `tests/test_export_paper_tables.py::ExportPaperTablesTest::test_help_and_strict_mode`; unchanged strict exporter requires `papers/claims_checklist.md`, absent at START_HEAD. `git diff --exit-code START_HEAD -- scripts/export_paper_tables.py tests/test_export_paper_tables.py` passes; `git ls-tree START_HEAD papers/claims_checklist.md` is empty. No unrelated WINE paper files were restored or altered to hide this failure.

Commands: `PYTHONPATH=. /Users/crazy/anaconda3/bin/python -m pytest -q tests/test_aamas_equal.py tests/test_aamas_llm_agents.py tests/test_aamas_stress.py tests/test_aamas_package.py --junitxml=artifacts/aamas2027/logs/targeted_tests.xml`; full: same interpreter `-m pytest -q tests --junitxml=artifacts/aamas2027/logs/full_regression.xml`. Explicit relevant test file list is saved in MANIFEST.json. `git diff --check` passed.

An extracted provisional bundle passed63tests, all five script help paths, E0 270-episode and E3 90-probe exact nonlatency reproduction, and8-episode E1 dry-run with0APIcalls. See `logs/package_replay_validation.json`. This replay used the final executable source but predates completed E1 data; final ZIP integrity/inclusion checks are recorded separately after assembly.

Experiment scripts use the Python standard library; tests require pytest>=7. Test runtime versions are recorded in MANIFEST.json.

## R1 validation

Preregistration: 93 targeted / 120 relevant passed, 161 full-suite passed + one historical exporter failure. Final additions: 96 targeted / 123 relevant passed, 164 full-suite passed + the same missing papers/claims_checklist.md failure. No skipped/xfail. Detailed logs: R1_validation/final_*.txt. Generated pytest log trailing whitespace normalized; git diff --check passes. No experiment implementation/config/defense logic changed after preregistration.
