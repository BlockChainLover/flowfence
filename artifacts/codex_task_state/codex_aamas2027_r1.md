# AAMAS R1 durable task state

- Goal: repair metric semantics and preregister/run 108-cell binding semantic MiniMax comparison; push PR #1, do not merge.
- Branch: codex/aamas2027-experiment-extension, clean isolated checkout /private/tmp/flowfence-aamas-r1-20260912; starting SHA 2a179d37e4b93132e42a1338074d4c3e4f72faa7. Original checkout remains untouched and dirty.
- Completed: corrected offline replay; six binding tasks, two hold paths; shared prompt/attacks; evaluator-only attempted/delivered counters; tests and 108-cell zero-API wiring run; preregistration documentation.
- Changed files: new aamas_metrics/aamas_binding_semantic modules; additive E1 hooks/E0 counters; run/recompute/summarize scripts, e6 configs, tests, R1 docs and corrected records.
- Validation: pytest tests/test_aamas_*.py (93 passed); full dry-run 108 completed, zero provider requests; full/relevant logs under R1_validation.
- Known limitations: one decision family; fixed representation grammar; original E3 negative and E4 blocked evidence remain. No paid calls yet.
- Resume: push preregistration, record SHA, stage only committed source on existing server, fixed pilot <=9 calls then formal <=324; rebuild reports from safe records; final commit/push and independent review.
