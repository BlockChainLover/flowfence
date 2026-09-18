# E2 S1-F task state

- Goal: human-approved quota amendment and deterministic 9/60 split freeze; no pilot/model run.
- Branch: codex/aamas2027-e2-source-s1f, based on accepted S1-R 406440eb82e588bf0810d631e65a1fd0dbf46974.
- Completed work: metadata-only capacity proof, amendment, explicit cluster constraints, deterministic selection rule/config and authored policy templates. No selected IDs yet.
- Changed files: E2_FACT_TYPE_AMENDMENT.md; E2_SELECTION_RULE.md; experiments/e2_source_s1f/; scripts/select_e2_s1f.py; artifacts/aamas2027_e2_source_s1f/preselection_capacity.json; this file; logs.
- Validation commands: metadata-only Python aggregate counts; no runtime/evaluator/model execution.
- Known limitations: public tasks run in standardized MAS harness; synthetic sidecars; family/type coupling; clusters do not prove independence. R3/recognizer/source eligibility unchanged.
- Resume instructions: FIRST commit the rule/config/script and record SHA. ONLY THEN execute selector, replay in separate directory, validate witness, write preregistration and frozen SHA manifest. Commit/push without merging. Do not run pilot.
