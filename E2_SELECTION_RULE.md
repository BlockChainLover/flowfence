# E2 S1-F deterministic selection rule

Version 1; 2026-09-18; committed before execution or selected-ID materialization. Executable rule: scripts/select_e2_s1f.py. Configuration and authored policy templates: experiments/e2_source_s1f/. No seed search, reranking or manual replacement is permitted. Fail rather than weaken constraints. The rule commit is recorded in selection provenance after this commit exists.

## Inputs and ordering

Use the accepted S1-R ELIGIBLE/NATURAL records and retained compatible types, S1 naturalness_and_clusters.csv.gz, pinned Hotpot parquet columns id/type only, and pinned source manifest. No questions, gold answers, SQL, source metrics, runtime defense results, model outputs, contamination outcomes, expected privacy effects or task-easiness judgments enter ordering. Only public source IDs/categories and frozen clusters are used. The accepted eligibility status is consumed as an admission list, not recomputed or ranked by certification results. Source file hashes and code pins identify inputs; no expensive evaluator recertification.

All lexical comparisons use Python Unicode string order, including numeric-looking BIRD IDs. Families are ordered bird_pg, tatqa, hotpot. Development is allocated first, then confirmatory; source IDs within a candidate group break ties lexicographically. Each family selects 3 development and 20 confirmatory records. Previously selected development IDs are permanently excluded from confirmatory eligibility; rerunning this rule reproduces the same split, never promotes development records.

## Constraints and algorithm (before IDs)

BIRD: group by database (portion before `|` in the retained database/difficulty key). Sort database names. Development uses the first available record from each of the first three distinct databases. Confirmatory cycles sorted databases, one next unused record per database per pass, until 20; maximum 2 per database, all 11 databases represented. Source difficulty remains reported, not scored. Development/confirmatory database overlap is explicitly allowed by S1 and reported.

TAT-QA: group by retained table/context UID, sort contexts, choose the lexicographically first eligible task per context. First 3 contexts are development, next 20 confirmatory. All 23 contexts are distinct; at most one question per context across both splits. Source table UID does not prove report/company independence.

HotpotQA: retain exact Unicode title identities and sorted title-set context signatures. Construct connected components over the FULL 7405-record supplied-title overlap graph, including all records before admission. Component key is its minimum source ID, not a hash. Development category slots are bridge/comparison/bridge. Confirmatory slots alternate bridge/comparison (10 each). For each slot choose the lexicographically first unused component supporting that category and its lexicographically first eligible task of that category. Never reuse a component across all 23 slots. This stronger diversity constraint implies S1's pairwise title disjointness and >=5 of each confirmatory category. All component sizes remain available, including large components; size does not rank tasks. Report full-pool shared-title/context-duplicate/component counts and selected component sizes. Distinct components do not imply semantic/statistical independence.

## Type assignment and policy

BIRD dev/confirm: all P4. TAT dev P1/P3/P1; confirm first 15 P1 then 5 P3. Hotpot dev P2/P3/P2; confirm first 15 P2 then 5 P3. Assignment positions refer to the above deterministic order, not file sorting. Verify every assignment against unchanged compatible types. Confirmatory totals exactly 15/15/10/20, family totals 20/20/20, development 3/3/3.

Freeze one policy skeleton per selected row using policy_templates.json; no raw fact is instantiated now. Deterministic future value generation uses the one-based ordinal of (family, task_id) sorted across the frozen 69 tasks, and the declared family/type template. It never uses a model or an outcome. Each selected row preserves authorized finance_agent, forbidden doc_writer_agent/final_output and internal_message contamination annotations. Closed-world authorization permits no other principal to read raw facts. Withheld-marker abstraction (`none`) is allowed; no inferred coarse semantic statement is licensed. Generic unique secret IDs use the unchanged defense's existing fallback marker.

## Feasibility and reproducibility

Before this rule is applied, a metadata-only capacity certificate checks unchanged type sets/counts, BIRD per-DB capacity, >=23 TAT contexts, and >=12 bridge plus >=11 comparison singleton Hotpot components. Singleton counts prove sufficient disjoint-category capacity even if other components are unavailable. The selector also validates the final constructive witness against the stronger constraints. Failure stops this stage for human review without substitutions.

After committing the rule/config/script, record its Git SHA, execute once, and independently replay into a separate directory from the same pins and metadata. Require byte-identical development.json, confirmatory.json, policy_skeletons.json, selection_provenance.json and allocation_certificate.json. A SHA256 manifest is explicitly requested by the human for exported frozen artifacts. It covers rule, configuration, templates, executable, input metadata/pins, selections, policies, feasibility and preregistration; it excludes itself to avoid a circular digest. Git remains the chronology record. No runtime architecture, recognizer, R3 or source annotations are changed. No model run or pilot is part of this stage.
