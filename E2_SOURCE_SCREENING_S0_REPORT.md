# E2 Source Screening S0 — public task / original evaluator acceptance audit

Date: 2026-09-18. P0 was human-accepted. Current phase: **baseline scouting**, limited to source acceptance. This is not Gate B, task selection, implementation, a development pilot, or evidence that a solver/defense works.

**AAMAS_E2_SOURCE_S0: READY_FOR_HUMAN_SELECTION**

14 independently recorded source profiles: **5 SOURCE_PASS, 7 SOURCE_FAIL, 2 UNRESOLVED**. Passing profiles represent **four**, not five, semantic families: PostgreSQL and SQLite Mini-Dev are alternatives over the same 500 questions. FinQA and TAT-QA substantially overlap and are alternatives in the proposed combinations. Two three-family candidate designs are offered; neither is selected.

Preferred for review: **BIRD Mini-Dev PostgreSQL + TAT-QA public dev + HotpotQA distractor public dev**. Alternative: replace TAT-QA with **FinQA public test**. These combine query construction/execution, financial numerical/document reasoning, and multi-hop evidence selection. This preference uses evaluator provenance, public availability, distinct task structure and privacy plausibility, never expected FlowFence performance.

The accepted claim is exactly:

`PUBLIC_BENCHMARK_TASK_AND_EVALUATOR_EXTERNAL_VALIDITY_UNDER_A_STANDARDIZED_MULTI_AGENT_EXECUTION_HARNESS`

SOURCE_PASS is an S0 source/semantic feasibility judgment, **not** a completed reproduction, implemented adapter, fully restored environment, or privacy certification of every task. Original-evaluator preservation PASS means the documented native input can be supplied faithfully and the original scoring components retained. Actual fixture coverage is reported separately. In particular, PostgreSQL was not initialized in S0: its public current DB package and original scoring path were inspected, while executed SQL gold fixtures used the official SQLite companion. No SQLite score is represented as PostgreSQL validation.

## Evidence and retained targets

- `PUBLIC_SOURCE_CANDIDATES.json`: complete profile records, exact code/data pins, license, original input/output, capabilities, classification and evidence links.
- `EVALUATOR_PRESERVATION_MATRIX.csv`, `CAPABILITY_PRESERVATION_MATRIX.csv`, `PRIVACY_AUGMENTATION_PLAUSIBILITY.csv`, `TASK_SCALE_AUDIT.csv`.
- `artifacts/aamas2027_e2_source_s0/source_provenance.json`: public URLs/revisions and observed archive metadata; no new content hashes or frozen contracts.
- `artifacts/aamas2027_e2_source_s0/OFFICIAL_TASK_ID_INVENTORY.csv`: complete inspected ID pools, **all unselected**; IDs are source keys, not development/confirmatory assignments.
- `artifacts/aamas2027_e2_source_s0/evaluator_sanity.json`: original-code deterministic results, including irregularities, with zero models.

E2 remains 60 confirmatory tasks × 3 conditions × 2 defenses × 3 repetitions = **1080 episodes**, preferably three families ×20 plus ≥3 disjoint development tasks per family. P1/P2/P3/P4 remains15 each. No task ID, augmentation, contamination artifact, final fact type or final design was assigned. Repetitions are repeated measurements; task/context/report/database overlap must be accounted for later. E3=324, E4-A=288, E4-B=288 and approximately84 unique semantic-task target remain unchanged; no task overlap accounting is settled here.

## Fixed family adapter and capability boundaries

Every feasible profile retains P0's **one coordinator and two generic workers**, existing principal bindings, same graph/scheduler/role prompts and defense-independent tools/state/evaluator. Workers can dynamically read, reason, review and delegate through the same action grammar; there is no per-task expert, scripted DAG, chosen hop count or answer-dependent branch. Domain schemas belong to family adapters, not new agent roles. Source record lookup by stable ID is ordinary data access, not task-ID-specific control flow.

For the preferred sources:

| Family | Input/state mapping | Source output mapping | Capabilities and forbidden additions |
|---|---|---|---|
| Mini-Dev PostgreSQL | Source question, db_id, public evidence, complete original schema/descriptions/database access into TASK state; gold SQL stays private | Actual released SQL + original db_id into the original indexed prediction format; no synthetic execution trace | Retain original database semantics/contents and SELECT/WITH capability. Read/schema/query results cross generic boundaries. No shell, web search, extra DB, privileged reference query or task-specific SQL repair. |
| TAT-QA | Complete table, paragraphs and question with original IDs/order | Final answer-list and original scale vocabulary into uid→[answer,scale] | No external browsing, hidden derivation, answer type, supporting-paragraph labels or gold facts. No altered numerical tolerance. |
| HotpotQA distractor | Original question and all source-provided titled/sentence-indexed paragraphs | Actual answer and chosen supporting pairs into original answer/sp maps | No live web/fullwiki corpus or replacement retrieval. Original gold answer/support labels are evaluator-private. Source context titles/indices preserved. |
| FinQA alternative | Full pre_text/post_text/table and question | Actual generated source-DSL tokens with EOF into original predicted field | Retrieval must operate over full input, not gold_inds or released oracle retrieval. Preserve numerical execution and symbolic program accuracy. |

Original Mini-Dev's top-level prediction parser uses ordinal ordering rather than blindly trusting question_id; the family serializer must retain a stable source-ID→evaluation-row mapping and align prediction/gold/metadata rows. This is one family-wide mapping, not handwritten per-task scoring. Missing/blocked answers must remain failures/absence under source handling, never substituted gold or repaired SQL. SQL writes, UDFs, outbound server I/O or arbitrary code are **not demonstrated** as accepted runtime capabilities here. The screened source profile is SELECT-only; a later profile requiring additional material capabilities must return for review instead of silently dropping them.

Public static QA source protocols require final outputs, not a private solver trace. Their source-specific baseline neural architectures are unnecessary to score outputs. Distributing the same complete public input among workers adds no external information. No hidden gold can be passed as a shortcut even when publicly downloadable. Original source limits apply to the whole team. These static releases do not define a native MAS turn budget: the later common total generation cap must be disclosed before task selection. Equal task semantics does not imply equal difficulty; additional reasoning, context partitioning and coordination costs remain threats. No native leaderboard equivalence is asserted.

## Scale and pre-result eligibility

The source-level filter checks released ID uniqueness, required public input and original gold/evaluator fields, source-family capability compatibility and public access. It does not use model task success or defense outcomes. Potential counts are **provisional source-level pools**, not a claim of 500/1668/7405 privacy-certified or mutually independent instances. Later task-level semantic/orthogonality review must still yield ≥23 per chosen family; if it does not, retain60 as a target and return to the human.

Mini-Dev has500 IDs in each dialect, not1000 semantic questions. Its README's combined V2 count780 conflicts with the described500+270; the old500 and separate270 release are audited separately. TAT-QA dev has1668 question IDs over278 source table contexts; questions sharing a table cannot automatically be treated as independent contexts. FinQA public test has1147 IDs over380 report pages. HotpotQA distractor dev has7405 IDs, including5918 bridge and1487 comparison questions; shared Wikipedia entities/passages create dependence. Repository IDs, table IDs and question wording alone are not proof of semantic independence.

HotpotQA actually has7345 records with10 paragraphs and60 with2–9; preserve each record’s original context length rather than padding or rejecting it merely for differing from the headline description. For SOURCE_PASS profiles no source-wide exclusion was triggered; the potential pool is the complete screened release. No final split is created. TAT-QA's alternative public test files are not silently joined: current test has1669 questions/278 contexts, test-gold1663/277. The aligned dev release is the candidate pool. Hidden FinQA private_test (919) and HotpotQA hidden-test grading are not counted toward availability. Original public dev can supply an independently selected confirmatory subset, but that subset must be called a study confirmatory sample from a public dev release, not an untouched benchmark test set.

## Privacy orthogonality and fact-type plausibility

All proposed facts would be synthetic and absent from benchmark gold. Preserve every PrivacyInstance field and the frozen recognizer. One authorized existing principal receives the private initial note; another existing principal and/or final output forbids raw disclosure. Common shared artifacts provide an existing contamination surface. Each proposed family exposes the same P0 worker-message/shared-artifact text surfaces, already within the frozen recognizer’s modeled channels; no new channel or semantic detector is required. Contamination can occupy a worker-produced artifact without rewriting any source task input. A/B must later omit the raw protected value and match the unchanged recognizer; no A/B text is created now. Metadata such as recognizer_expected_match stays outside defense input. Original task facts remain available; nothing required for clean success is relabeled private to manufacture a conflict.

Representative source records were inspected only for static context plausibility, not selected as study tasks:

- SQL: financial/debit-card/student-club queries and service-backed PostgreSQL schema access make an internal connection-profile credential or account/project identifier plausible. Synthetic P4 is a credential-like **value in a private access note**, never a real provider/DB password, a gold field, or a new credential-validation task. Workers keep the original DB capability through the broker; no additional service/tool is introduced. The public SQL objective never requires printing a connection credential.
- Financial documents: public contract/revenue tables and financial change computations can accompany a private analyst budget, internal report/client identifier, or confidential preliminary risk category. These are separate initial context; public report values, questions, derived-answer rules and gold remain intact. A private numeric fact cannot replace a required public table value.
- HotpotQA: bridge/comparison evidence questions can carry a private research requester's identifier or sensitive affiliation in the authorized request context. The original question, source-provided paragraphs and evidence-scoring objective stay intact. This is a synthetic service-context interpretation, **not a claim that Wikipedia itself is private**. No private affiliation may become evidence for the public answer.
- HumanEval: inspected algorithmic function prompts do not establish a natural sensitive-context attachment across23 tasks. It remains UNRESOLVED; generic credential stuffing is not accepted merely because its test harness is simple.

P4 is strongest for the PostgreSQL profile. Local SQLite has no native server authentication; its P4 mapping is deliberately UNRESOLVED, and neither document QA nor public Wikipedia is assigned artificial credentials. The proposed combination's balance is **PLAUSIBLE, not allocated**: PostgreSQL has capacity for15 P4 and5 P3, financial documents15 P1 and5 P3, and HotpotQA15 P2 and5 P3. This is a nonbinding aggregate feasibility witness only, not task-level allocation or a preregistered fact schedule. P3 meanings and especially HotpotQA requester-context naturalness require human scrutiny. If those are rejected or later task-level review cannot sustain the balance, the fallback is NO_VALID_3_FAMILY_DESIGN, not forced facts or reduced scale.

## Original evaluator dry checks and limitations

Commands and dependency versions are in the artifact README. Only original deterministic evaluators, public gold, serialization round-trips and one mock grader response were used. No model, solver, runtime integration, defense integration or evaluator prompt change occurred.

- TAT-QA1668 gold cases: source-valid nonempty answer lists and JSON round-trip both give EM/F1/scale1.0. Direct scalar gold gives0.9970023980815348 because five numeric-zero values are falsey in the original scorer. The source supports answer lists; wrapping a scalar as a one-element answer list is a family-wide representational operation, not scorer repair. Missing answers score0. Operation metric remains0 because the official answer-file API does not supply predicted operations; it is not silently promoted to a success metric.
- BIRD SQLite52 gold queries from the smallest official DB file: original EX52/52; serialized SQL exactly matches; original Soft-F1 sums52. Invalid SQL receives original EX0. This is technical fixture selection by database size, not development/confirmatory selection. PostgreSQL and R-VES timing were **not** executed. Timing reproducibility requires the source's prescribed measurement setup later.
- HotpotQA7405 gold cases: all12 original metrics agree before/after serialization. EM/support/joint EM are1.0; answer/joint F1 is0.999729912221472, retaining original normalization behavior. Wrong-answer/empty-support fixture gives0 across metrics. No scorer normalization was fixed or examples dropped.
- FinQA1147 gold programs: original execution accuracy1.0 and program accuracy1.0. Both metrics retained; this does not demonstrate model utility.
- BrowseComp deterministic stub: original grade_sample receives `correct: yes`, returns `correct: yes`, while original score comparison asks whether it equals `yes`; result false. No grader request occurred. Current configured judge also uses an unapproved provider. Fixing code or swapping judge would violate this stage's preservation contract.

The installed Docker client has no running local daemon; no large image build or PostgreSQL restoration was attempted. Source infrastructure is publicly obtainable; absence of a local service is not presented as a benchmark impossibility. Package inspection verified the current public DB archive's member inventory and manifests through byte ranges. The archive and canonical HF task manifests differ in exactly one SQL field (question_id879); non-SQL input fields and IDs match. Use the pinned HF gold per the source's canonical-data instruction, never silently substitute archive gold. Database package snapshot/restoration and exact engine compatibility remain prerequisites for future adapter validation, not completed evidence.

## Stability, contamination and residual threats

Code/data commit pins are recorded independently. BIRD database archives are mutable public distribution endpoints; observed file ID/size/inventory/date and legacy object ETag are retained. A later executable package must retain the actual authorized DB snapshot and engine version, rather than fetch an unknown changed archive during comparisons. HF/code pins alone do not pin DB binaries. HotpotQA canonical CMU HTTP/HTTPS fetches failed; its versioned HF release was used with documented lossless columnar mapping, without claiming byte identity to the unavailable canonical file. The original evaluator ran successfully on that release.

LiveSQLBench variants are separate releases (270/270/600/480), not interchangeable SQL tasks or distinct semantic families merely by version/domain. Current public gold/test fields are empty across all inspected rows. BIRD-Interact Lite's release has300 IDs despite the270 README; full has600. Its simulator, phase rewards and action budgets affect task meaning, so converting it into answer-only SQL would not preserve semantics. No email was sent to obtain missing material.

BrowseComp has1266 encrypted public rows, not inaccessible secret answers. S0 did not decrypt them or publish plaintext. In addition to the pinned code issue and original-judge provider incompatibility, a live-web capability/resource snapshot is unestablished. Replacing it with static HotpotQA changes the candidate family and narrows the claim to offline evidence retrieval; it is not a BrowseComp substitute reproduction.

The seed SWE-bench Verified evaluator does accept a patch without hidden solver trace; native architecture is not the problem. The unresolved issue is preserving full repository/testing capabilities within P0's controlled tool/effect model, plus environment and upstream repository-license review. Smaller official SWE-bench subsets would not by themselves solve that issue; no extra variant is counted merely for convenience. Public training exposure and known task reuse affect all long-public releases; no benchmark is claimed contamination-free. Family differences, synthetic privacy salience, unchanged-recognizer coverage, context-window changes and repeated-measure dependence remain explicitly reportable.

## E2/E3 separation and stopping point

All proposed E2 objectives and original scoring remain externally authored; neither public question nor evaluator is replaced with enterprise prose or a homemade success function. Only P0's solving/runtime layer is experimental. Private initial sidecars are privacy augmentation, not additional required enterprise workflow steps. E3 remains purpose-built dynamic delegation/tool-use stress with controlled trajectories. E2 may exhibit little propagation on some tasks; do not discard those cases because a defense effect is small or absent.

Recommended human decision: review the two combinations, especially PostgreSQL P4 and research-request metadata naturalness. Select a source-level design only if those interpretations are accepted. The next stage must be separately authorized and specify its scope; this S0 does not initiate task selection, full adapter/runtime implementation, development pilot or Gate B. Frozen R3 and recognizer are unchanged; formal and development model generations both0.

## Per-source acceptance cards

The following links point to the exact inspected revisions. Additional evaluator files and dataset revision URLs are in PUBLIC_SOURCE_CANDIDATES.json.

### SWE-bench Verified — UNRESOLVED

Source: [https://github.com/SWE-bench/SWE-bench](https://github.com/SWE-bench/SWE-bench/blob/02e7a74ffd0b707aab73d203fe87bdc7c76afc8e/README.md). Code `02e7a74ffd0b707aab73d203fe87bdc7c76afc8e`; data `78f471bf655a3137b2e8a75af1501690ec009ec3`; split `test`; 500 source records. License: Harness MIT; issue/repository content retains upstream licensing; no dataset-license declaration in inspected HF card.

Evaluator: Original Docker harness, test patch, eval_script and FAIL_TO_PASS/PASS_TO_PASS; no solver reasoning trace. Native output: instance_id, model_name_or_path, model_patch (unified diff). Evaluator preservation **PASS**; capabilities **UNRESOLVED**; family adapter **UNRESOLVED**; privacy **PLAUSIBLE**; decomposition **UNRESOLVED**.

Capabilities: Full base-commit repository and issue; repository editing/testing via shell commonly available; setup network/images. Never expose patch/test_patch/eval_script or held-out tests to workers. Source does not require a particular solver scaffold.

Assessment: Do not infer impossible native architecture; the missing proof concerns collective tool capability under accepted P0. P0 excludes uncontrolled model-authored native code/shell effects. Patch-only serialization is feasible but capability-equivalent execution/testing under P0 has not been demonstrated. Local Docker daemon absent. Dataset/repo licensing must be resolved.

### BIRD Mini-Dev PostgreSQL — SOURCE_PASS

Source: [https://github.com/bird-bench/mini_dev](https://github.com/bird-bench/mini_dev/blob/abd11b6db92a1c9f809b32f7564c7c71b34d67f0/README.md). Code `abd11b6db92a1c9f809b32f7564c7c71b34d67f0`; data `f65faf4ae3b638c1fa6df1d3370c8d92c8366301`; split `mini_dev_pg`; 500 source records. License: CC BY-SA 4.0 in source README and HF card; attribution/share-alike retained.

Evaluator: Original evaluation_ex.py; preserve evaluation_f1.py and evaluation_ves.py when reporting their source metrics; Python + func_timeout + DB drivers + numpy. Native output: Prediction JSON indexed by original order with SQL plus source db_id delimiter; original gold SQL and DB kept evaluator-private. Evaluator preservation **PASS**; capabilities **PASS**; family adapter **FEASIBLE**; privacy **PLAUSIBLE**; decomposition **PASS**.

Capabilities: Question, public evidence, complete schema/description/database contents; SELECT/WITH task family. Fixed read-only data/schema access and SQL envelope, no external browsing or arbitrary shell added. Original per-query timeout retained. No source solver-turn cap claimed.

Assessment: A final actual SQL string is the same semantic evaluator input regardless of which worker generated it. No private solver trace or native planner needed. No source-level blocker. PostgreSQL initialization not executed; timing metric not measured. Current archive differs from HF gold in one SQL entry; use canonical HF gold.

### BIRD Mini-Dev SQLite — SOURCE_PASS

Source: [https://github.com/bird-bench/mini_dev](https://github.com/bird-bench/mini_dev/blob/abd11b6db92a1c9f809b32f7564c7c71b34d67f0/README.md). Code `abd11b6db92a1c9f809b32f7564c7c71b34d67f0`; data `f65faf4ae3b638c1fa6df1d3370c8d92c8366301`; split `mini_dev_sqlite`; 500 source records. License: CC BY-SA 4.0 in source README and HF card; attribution/share-alike retained.

Evaluator: Original evaluation_ex.py; preserve evaluation_f1.py and evaluation_ves.py when reporting their source metrics; Python + func_timeout + DB drivers + numpy. Native output: Prediction JSON indexed by original order with SQL plus source db_id delimiter; original gold SQL and DB kept evaluator-private. Evaluator preservation **PASS**; capabilities **PASS**; family adapter **FEASIBLE**; privacy **PLAUSIBLE**; decomposition **PASS**.

Capabilities: Question, public evidence, complete schema/description/database contents; SELECT/WITH task family. Fixed read-only data/schema access and SQL envelope, no external browsing or arbitrary shell added. Original per-query timeout retained. No source solver-turn cap claimed.

Assessment: A final actual SQL string is the same semantic evaluator input regardless of which worker generated it. No private solver trace or native planner needed. No source-level blocker. PostgreSQL initialization not executed; timing metric not measured. Current archive differs from HF gold in one SQL entry; use canonical HF gold.

### livesqlbench-base-lite — SOURCE_FAIL

Source: [https://github.com/bird-bench/livesqlbench](https://github.com/bird-bench/livesqlbench/blob/e15cd221267e06fabfaf6a3d4a69308280ce9a7c/README.md). Code `e15cd221267e06fabfaf6a3d4a69308280ce9a7c`; data `507d7d98f477b9d6a990628ea021bd2501cfd6e2`; split `dev`; 270 source records. License: Code MIT; HF data cc-by-4.0; repo badge CC BY-SA 4.0 discrepancy recorded.

Evaluator: Public evaluator runs pred_sqls, then source test cases / source comparison conditions against sol_sql; PostgreSQL or official SQLite variant. Native output: instance_id plus pred_sqls, preprocessing/cleanup and original source test-case fields. Evaluator preservation **FAIL**; capabilities **UNRESOLVED**; family adapter **UNRESOLVED**; privacy **PLAUSIBLE**; decomposition **UNRESOLVED**.

Capabilities: Schema, column meanings, HKB and SQL environment; Query and Management/CRUD tasks. Must retain actual state transitions and all tests; cannot replace management with final SELECT. Native Agent/CLI wrappers are optional, not adopted.

Assessment: FAIL for public materials available in S0, not a permanent verdict after authorized material acquisition. Every inspected row has empty sol_sql, test_cases and external_knowledge. Official release requires email to obtain GT/test cases; not requested/sent here. No original complete scorer input available.

### livesqlbench-base-lite-sqlite — SOURCE_FAIL

Source: [https://github.com/bird-bench/livesqlbench](https://github.com/bird-bench/livesqlbench/blob/e15cd221267e06fabfaf6a3d4a69308280ce9a7c/README.md). Code `e15cd221267e06fabfaf6a3d4a69308280ce9a7c`; data `0664a2f28555faa0dd2947c8c23288df79bcc06b`; split `dev`; 270 source records. License: Code MIT; HF data cc-by-sa-4.0; repo badge CC BY-SA 4.0 discrepancy recorded.

Evaluator: Public evaluator runs pred_sqls, then source test cases / source comparison conditions against sol_sql; PostgreSQL or official SQLite variant. Native output: instance_id plus pred_sqls, preprocessing/cleanup and original source test-case fields. Evaluator preservation **FAIL**; capabilities **UNRESOLVED**; family adapter **UNRESOLVED**; privacy **PLAUSIBLE**; decomposition **UNRESOLVED**.

Capabilities: Schema, column meanings, HKB and SQL environment; Query and Management/CRUD tasks. Must retain actual state transitions and all tests; cannot replace management with final SELECT. Native Agent/CLI wrappers are optional, not adopted.

Assessment: FAIL for public materials available in S0, not a permanent verdict after authorized material acquisition. Every inspected row has empty sol_sql, test_cases and external_knowledge. Official release requires email to obtain GT/test cases; not requested/sent here. No original complete scorer input available.

### livesqlbench-base-full-v1 — SOURCE_FAIL

Source: [https://github.com/bird-bench/livesqlbench](https://github.com/bird-bench/livesqlbench/blob/e15cd221267e06fabfaf6a3d4a69308280ce9a7c/README.md). Code `e15cd221267e06fabfaf6a3d4a69308280ce9a7c`; data `e33469b1d1134dac377deda2643c0bda945cdfc9`; split `dev`; 600 source records. License: Code MIT; HF data cc-by-4.0; repo badge CC BY-SA 4.0 discrepancy recorded.

Evaluator: Public evaluator runs pred_sqls, then source test cases / source comparison conditions against sol_sql; PostgreSQL or official SQLite variant. Native output: instance_id plus pred_sqls, preprocessing/cleanup and original source test-case fields. Evaluator preservation **FAIL**; capabilities **UNRESOLVED**; family adapter **UNRESOLVED**; privacy **PLAUSIBLE**; decomposition **UNRESOLVED**.

Capabilities: Schema, column meanings, HKB and SQL environment; Query and Management/CRUD tasks. Must retain actual state transitions and all tests; cannot replace management with final SELECT. Native Agent/CLI wrappers are optional, not adopted.

Assessment: FAIL for public materials available in S0, not a permanent verdict after authorized material acquisition. Every inspected row has empty sol_sql, test_cases and external_knowledge. Official release requires email to obtain GT/test cases; not requested/sent here. No original complete scorer input available.

### livesqlbench-large-v1 — SOURCE_FAIL

Source: [https://github.com/bird-bench/livesqlbench](https://github.com/bird-bench/livesqlbench/blob/e15cd221267e06fabfaf6a3d4a69308280ce9a7c/README.md). Code `e15cd221267e06fabfaf6a3d4a69308280ce9a7c`; data `a418e108d5cbb4cf9b783a928eff5e924ad2460d`; split `dev`; 480 source records. License: Code MIT; HF data cc-by-4.0; repo badge CC BY-SA 4.0 discrepancy recorded.

Evaluator: Public evaluator runs pred_sqls, then source test cases / source comparison conditions against sol_sql; PostgreSQL or official SQLite variant. Native output: instance_id plus pred_sqls, preprocessing/cleanup and original source test-case fields. Evaluator preservation **FAIL**; capabilities **UNRESOLVED**; family adapter **UNRESOLVED**; privacy **PLAUSIBLE**; decomposition **UNRESOLVED**.

Capabilities: Schema, column meanings, HKB and SQL environment; Query and Management/CRUD tasks. Must retain actual state transitions and all tests; cannot replace management with final SELECT. Native Agent/CLI wrappers are optional, not adopted.

Assessment: FAIL for public materials available in S0, not a permanent verdict after authorized material acquisition. Every inspected row has empty sol_sql, test_cases and external_knowledge. Official release requires email to obtain GT/test cases; not requested/sent here. No original complete scorer input available.

### bird-interact-lite — SOURCE_FAIL

Source: [https://github.com/bird-bench/BIRD-Interact](https://github.com/bird-bench/BIRD-Interact/blob/451fe2c3518ee1cf908d8139e2913483bd519381/README.md). Code `451fe2c3518ee1cf908d8139e2913483bd519381`; data `f7881a9c2b9630cc4fc13b0c39279740b0a2fd87`; split `dev`; 300 source records. License: Code MIT; data CC BY-SA 4.0.

Evaluator: Original two-phase reward/test evaluation plus ambiguity/user-simulator behavior and action costs; gold/test cases missing. Native output: Actual phase-wise SQL/state, dialogue/actions and bird-coin budgets; not a single answer substitute. Evaluator preservation **FAIL**; capabilities **UNRESOLVED**; family adapter **UNRESOLVED**; privacy **PLAUSIBLE**; decomposition **UNRESOLVED**.

Capabilities: Ambiguous question, source simulator, HKB/schema/DB tools; original per-action costs and phase rewards. Shared team budget; cannot replace simulator by disclosing clear query or reference SQL.

Assessment: Task/evaluator audit only, no native MAS reuse. User simulator is an environmental capability, not a free replacement judge. Missing GT/test cases; current simulator privately stores reference SQL and influences clarification/reward. Preserving that environment under P0 and MiniMax-only without changing source semantics unresolved.

### bird-interact-full — SOURCE_FAIL

Source: [https://github.com/bird-bench/BIRD-Interact](https://github.com/bird-bench/BIRD-Interact/blob/451fe2c3518ee1cf908d8139e2913483bd519381/README.md). Code `451fe2c3518ee1cf908d8139e2913483bd519381`; data `5d78b0722433c3821e1ebda5d8c39d24070049d7`; split `dev`; 600 source records. License: Code MIT; data CC BY-SA 4.0.

Evaluator: Original two-phase reward/test evaluation plus ambiguity/user-simulator behavior and action costs; gold/test cases missing. Native output: Actual phase-wise SQL/state, dialogue/actions and bird-coin budgets; not a single answer substitute. Evaluator preservation **FAIL**; capabilities **UNRESOLVED**; family adapter **UNRESOLVED**; privacy **PLAUSIBLE**; decomposition **UNRESOLVED**.

Capabilities: Ambiguous question, source simulator, HKB/schema/DB tools; original per-action costs and phase rewards. Shared team budget; cannot replace simulator by disclosing clear query or reference SQL.

Assessment: Task/evaluator audit only, no native MAS reuse. User simulator is an environmental capability, not a free replacement judge. Missing GT/test cases; current simulator privately stores reference SQL and influences clarification/reward. Preserving that environment under P0 and MiniMax-only without changing source semantics unresolved.

### BrowseComp — SOURCE_FAIL

Source: [https://github.com/openai/simple-evals](https://github.com/openai/simple-evals/blob/652c89d0ca9df547706735883097e9537d40dc47/README.md). Code `652c89d0ca9df547706735883097e9537d40dc47`; data `Azure ETag 0x8DD785A972BF8A0; Last-Modified 2025-04-10T18:07:43Z; 1196283 bytes`; split `test`; 1266 source records. License: MIT per source README; do not publish decrypted problems/answers.

Evaluator: Original grader prompt + configured gpt-4.1-2025-04-14 sampler + original correct parsing. Native output: Full answer response including explanation/exact answer/confidence; scorer sees original private answer. Evaluator preservation **FAIL**; capabilities **UNRESOLVED**; family adapter **NOT_FEASIBLE**; privacy **UNRESOLVED**; decomposition **UNRESOLVED**.

Capabilities: Live web/search; reproducible resource snapshot not supplied. Private encrypted gold decryptable by official code but never decoded in S0. No solver trace needed for grading.

Assessment: Public encrypted dataset is not inaccessible gold; fail is scorer/protocol and provider mismatch, not an assertion that encryption hides answers. Pinned official grade_sample returns "correct: yes" while __call__ tests == "yes": deterministic stub confirms false. Repair prohibited here. Configured OpenAI judge conflicts with MiniMax-only; replacing judge prohibited. Live-web drift unresolved.

### TAT-QA public development release — SOURCE_PASS

Source: [https://github.com/NExTplusplus/TAT-QA](https://github.com/NExTplusplus/TAT-QA/blob/870accc41953dcde885aabeb963d94aabdc0fbc3/README.md). Code `870accc41953dcde885aabeb963d94aabdc0fbc3`; data `870accc41953dcde885aabeb963d94aabdc0fbc3`; split `dev`; 1668 source records. License: Dataset CC BY 4.0; code MIT.

Evaluator: Original tatqa_eval.py / TaTQAEmAndF1; Python, numpy, pandas, scipy; no model/judge/training checkpoint. Native output: uid -> [answer or answer-list, scale]; preserve EM/F1/scale and original detail reporting. Evaluator preservation **PASS**; capabilities **PASS**; family adapter **FEASIBLE**; privacy **PLAUSIBLE**; decomposition **PASS**.

Capabilities: Complete public table, paragraphs and question; no external web, shell or hidden derivation/gold/relevant-paragraph annotations. One generic context packer and fixed answer serialization; reasoning may be distributed but no extra public data.

Assessment: Original exact/numeric/span scorer consumes only answer/scale; source solver architecture is unnecessary. No source-level blocker. Legacy scalar-zero behavior requires legal nonempty answer-list representation, not scorer repair. Public test/test-gold are misaligned; screened pool is dev.

### FinQA public test — SOURCE_PASS

Source: [https://github.com/czyssrs/FinQA](https://github.com/czyssrs/FinQA/blob/0f16e2867befa6840783e58be38c9efb9229d742/README.md). Code `0f16e2867befa6840783e58be38c9efb9229d742`; data `0f16e2867befa6840783e58be38c9efb9229d742`; split `test (public only)`; 1147 source records. License: Repository MIT; public reports retain source rights; no bulk source-document redistribution.

Evaluator: Original code/evaluate/evaluate.py, numerical program execution AND symbolic program accuracy; numpy/sympy/tqdm. Native output: List of {id, predicted:[source DSL tokens including EOF]}. Evaluator preservation **PASS**; capabilities **PASS**; family adapter **FEASIBLE**; privacy **PLAUSIBLE**; decomposition **PASS**.

Capabilities: All original pre_text/post_text/table/question; perform retrieval from full report input, never use qa.gold_inds or provided gold retrieval shortcut. No external web or native training model required.

Assessment: No new arithmetic scorer; native DSL programs fed unchanged to original evaluator. No source-level blocker. Closely overlaps TAT-QA in objective/context; use as alternative, never count both as independent semantic families in preferred trio.

### HotpotQA distractor public development — SOURCE_PASS

Source: [https://github.com/hotpotqa/hotpot](https://github.com/hotpotqa/hotpot/blob/3635853403a8735609ee997664e1528f4480762a/README.md). Code `3635853403a8735609ee997664e1528f4480762a`; data `1908d6afbbead072334abe2965f91bd2709910ab`; split `distractor/validation (= official dev)`; 7405 source records. License: Dataset CC BY-SA 4.0; code Apache 2.0 per source README.

Evaluator: Original hotpot_evaluate_v1.py; Python + ujson; all answer/support/joint EM/F1/precision/recall retained. Native output: {answer:{original_id:string}, sp:{original_id:[[title,sentence_index],...]}}. Evaluator preservation **PASS**; capabilities **PASS**; family adapter **FEASIBLE**; privacy **PLAUSIBLE**; decomposition **PASS**.

Capabilities: All source-provided paragraphs (normally 10), titles, sentence indices and question; no fullwiki retrieval, no live web, no gold support labels or answer. Generic indexing over these same paragraphs allowed without adding documents.

Assessment: Static multi-hop evidence selection, not live browsing. Lossless columnar-to-native conversion; all 12 metrics unchanged on gold/serialization fixtures. No source-level blocker. Canonical CMU download failed HTTP/HTTPS in S0; versioned HF release retrieved. Mirror lineage is disclosed; no byte-for-byte canonical comparison claimed.

### HumanEval function completion — UNRESOLVED

Source: [https://github.com/openai/human-eval](https://github.com/openai/human-eval/blob/6d43fb980f9fee3c892a914eda09951f772ad10d/README.md). Code `6d43fb980f9fee3c892a914eda09951f772ad10d`; data `6d43fb980f9fee3c892a914eda09951f772ad10d`; split `test`; 164 source records. License: MIT.

Evaluator: Original human_eval/evaluation.py and execution.py; Python, numpy, tqdm; isolated evaluator code execution required. Native output: JSONL {task_id,completion}; prompt/test/entry_point private/public split retained. Evaluator preservation **PASS**; capabilities **PASS**; family adapter **FEASIBLE**; privacy **UNRESOLVED**; decomposition **PASS**.

Capabilities: Source function signature/docstring/imports/examples; no external repo, network or runtime shell needed for completion-only protocol. Original tests only in evaluator.

Assessment: Completion-only architecture is distinct from SWE-bench repository repair; deterministic evaluator plausible, privacy suitability unresolved. Representative algorithmic prompts do not establish natural sensitive private context for >=23 tasks. Do not force enterprise credentials into toy functions. Evaluator sandbox not exercised in S0.
