# S0 candidate combinations — no final selection

AAMAS_E2_SOURCE_S0: READY_FOR_HUMAN_SELECTION

| Candidate | Three semantic families | Potential source pools | Evaluator validity/maturity | Integration and infrastructure | Privacy/reproducibility limits |
|---|---|---|---|---|---|
| A — preferred for review | BIRD Mini-Dev PostgreSQL; TAT-QA dev; HotpotQA distractor dev | 500;1668 (278 table contexts);7405 | Original SQL EX/optional source efficiency/F1; original numeric/span EM/F1/scale; original answer/support/joint metrics | One generic envelope with SQL+two answer serializers. PostgreSQL server/dump largest dependency; QA scorers CPU/local. No live web or paid judge. | PG private connection metadata supports P4 plausibly. TAT analyst notes and Hotpot private requester context are synthetic interpretations requiring human acceptance. DB restoration not run; HF Hotpot mirror used. |
| B — alternative for review | BIRD Mini-Dev PostgreSQL; FinQA public test; HotpotQA distractor dev | 500;1147 (380 report pages);7405 | Original SQL metrics; original DSL execution AND symbolic equivalence; original answer/support/joint metrics | Same SQL/retrieval serializers; financial DSL token serialization adds complexity over A; sympy/numpy instead of TAT scorer | More explicit financial reasoning output, same public-report/privacy limitations; no oracle retrieval shortcuts. |

Both preserve20 confirmatory +≥3 disjoint development tasks per family as targets, with source pools comfortably exceeding23. Counts are provisional source-level availability, not a final eligibility certification. No original-ID selection, fact allocation, contamination artifact or outcome filtering occurred.

Diversity is based on reasoning/action and scoring structure: executing relational queries against a database; deriving numerical/document answers or DSL programs from financial reports; locating/cross-checking sentences and returning evidence in an externally supplied paragraph collection. PostgreSQL versus SQLite, different DB domains and different repository IDs do not make new families. TAT-QA and FinQA are alternatives rather than two seats in a trio. Hotpot distractor is static evidence retrieval, not live-web research.

A is preferred for fewer output mechanisms and mature deterministic scorer interfaces, not predicted defense advantage. B is useful if the human values explicit financial programs. No third recommendation is padded with a failed or unresolved source. SWE-bench and HumanEval remain unresolved; LiveSQLBench/BIRD-Interact public complete evaluator inputs unavailable; BrowseComp current source/judge incompatible. SQLite is a feasible SQL source profile but not currently preferred for P4: a local SQLite task does not naturally require server credentials.

Nonbinding aggregate balance witness (no task IDs or actual facts): SQL may support15P4+5P3; financial documents15P1+5P3; research requests15P2+5P3. Totals15 of each. This is a plausibility assessment, not permission to force a type into unsuitable tasks. Human rejection or later failure to obtain≥23 naturally augmentable tasks/family returns NO_VALID_3_FAMILY_DESIGN; never lower60 or change evaluator/goal.

E2 remains externally sourced tasks/scoring under our common harness. E3 remains purpose-built enterprise delegation/tool-use stress. No new required enterprise steps are added to E2 to make it resemble E3. Repeated conditions/defenses/repetitions are not new semantic tasks. No design is frozen or selected by this artifact.
