# E2-A formal report

**FORMAL CONFIRMATORY EVIDENCE — PARTIAL E2 TRANCHE**

Status: COMPLETED. Preregistration commit: `2a8e3910a133862a0df9f53a47131d798da047c1`.
Primary semantic units: **40 public benchmark tasks**, 20 TAT-QA and20 HotpotQA. The720episodes are repeated observations, not720independent samples. P1=15/P2=15/P3=10/P4=0. Fact type is coupled to family; no causal fact-type comparison.

BIRD was withdrawn before formal execution due to runtime-capability infeasibility under the frozen160000-byte guard; zero formal BIRD episodes. This is neither a negative privacy result nor a failed defense experiment. All historical IDs remain preserved. E2_B_STATUS: DEFERRED_NOT_SELECTED. Broader60-task E2 is incomplete.

## Execution

Expected720; attempted720; finished720; valid ordinary observations720; completed finals421; unattempted by hard stop0; pending/in-flight0.

| Termination | Count |
| --- | --- |
| EVALUATOR_FAILURE | 2 |
| MODEL_LENGTH | 1 |
| POLICY_REJECTION | 215 |
| PROTOCOL_FAILURE | 30 |
| PROVIDER_FAILURE | 53 |
| SUCCESSFUL_FINAL | 419 |

Provider and infrastructure failure counters overlap under the retained historical reporting convention. Transport timeout flags can overlap provider failures; do not add overlapping counters. A schema-valid final is not necessarily a correct answer.

| Family | Condition | Defense | Repetition | Attempted | Finals |
| --- | --- | --- | --- | --- | --- |
| hotpot | CLEAN | EXACT_IFC | 1 | 20 | 18 |
| hotpot | CLEAN | EXACT_IFC | 2 | 20 | 17 |
| hotpot | CLEAN | EXACT_IFC | 3 | 20 | 20 |
| hotpot | CLEAN | FLOWFENCE_R2 | 1 | 20 | 18 |
| hotpot | CLEAN | FLOWFENCE_R2 | 2 | 20 | 17 |
| hotpot | CLEAN | FLOWFENCE_R2 | 3 | 20 | 19 |
| hotpot | CONTAMINATION_A | EXACT_IFC | 1 | 20 | 19 |
| hotpot | CONTAMINATION_A | EXACT_IFC | 2 | 20 | 17 |
| hotpot | CONTAMINATION_A | EXACT_IFC | 3 | 20 | 18 |
| hotpot | CONTAMINATION_A | FLOWFENCE_R2 | 1 | 20 | 0 |
| hotpot | CONTAMINATION_A | FLOWFENCE_R2 | 2 | 20 | 0 |
| hotpot | CONTAMINATION_A | FLOWFENCE_R2 | 3 | 20 | 0 |
| hotpot | CONTAMINATION_B | EXACT_IFC | 1 | 20 | 18 |
| hotpot | CONTAMINATION_B | EXACT_IFC | 2 | 20 | 16 |
| hotpot | CONTAMINATION_B | EXACT_IFC | 3 | 20 | 15 |
| hotpot | CONTAMINATION_B | FLOWFENCE_R2 | 1 | 20 | 0 |
| hotpot | CONTAMINATION_B | FLOWFENCE_R2 | 2 | 20 | 0 |
| hotpot | CONTAMINATION_B | FLOWFENCE_R2 | 3 | 20 | 0 |
| tatqa | CLEAN | EXACT_IFC | 1 | 20 | 18 |
| tatqa | CLEAN | EXACT_IFC | 2 | 20 | 17 |
| tatqa | CLEAN | EXACT_IFC | 3 | 20 | 19 |
| tatqa | CLEAN | FLOWFENCE_R2 | 1 | 20 | 19 |
| tatqa | CLEAN | FLOWFENCE_R2 | 2 | 20 | 17 |
| tatqa | CLEAN | FLOWFENCE_R2 | 3 | 20 | 17 |
| tatqa | CONTAMINATION_A | EXACT_IFC | 1 | 20 | 18 |
| tatqa | CONTAMINATION_A | EXACT_IFC | 2 | 20 | 18 |
| tatqa | CONTAMINATION_A | EXACT_IFC | 3 | 20 | 16 |
| tatqa | CONTAMINATION_A | FLOWFENCE_R2 | 1 | 20 | 0 |
| tatqa | CONTAMINATION_A | FLOWFENCE_R2 | 2 | 20 | 0 |
| tatqa | CONTAMINATION_A | FLOWFENCE_R2 | 3 | 20 | 0 |
| tatqa | CONTAMINATION_B | EXACT_IFC | 1 | 20 | 18 |
| tatqa | CONTAMINATION_B | EXACT_IFC | 2 | 20 | 16 |
| tatqa | CONTAMINATION_B | EXACT_IFC | 3 | 20 | 16 |
| tatqa | CONTAMINATION_B | FLOWFENCE_R2 | 1 | 20 | 0 |
| tatqa | CONTAMINATION_B | FLOWFENCE_R2 | 2 | 20 | 0 |
| tatqa | CONTAMINATION_B | FLOWFENCE_R2 | 3 | 20 | 0 |

## Treatment

| Condition | Scheduled | Valid finance | Mediated | Quarantined | Released | Delivered | Pre-handoff failure |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CONTAMINATION_A | 240 | 218 | 218 | 109 | 109 | 109 | 22 |
| CONTAMINATION_B | 240 | 212 | 212 | 106 | 106 | 106 | 28 |

Conditional entry: {'entered': 430, 'valid_finance_handoff': 430, 'rate': 1.0}. Each contaminated episode has separate stage/treatment/writer/final accounting in derived/stage_treatment_reachability.json. Non-reachability is not privacy success. Terminal R2 quarantine permits no replacement semantic handoff or writer.

## Raw-value privacy

| Family | Condition | Defense | TRUE | FALSE | UNKNOWN |
| --- | --- | --- | --- | --- | --- |
| hotpot | CLEAN | EXACT_IFC | 0 | 55 | 5 |
| hotpot | CLEAN | FLOWFENCE_R2 | 0 | 54 | 6 |
| hotpot | CONTAMINATION_A | EXACT_IFC | 0 | 54 | 6 |
| hotpot | CONTAMINATION_A | FLOWFENCE_R2 | 0 | 0 | 60 |
| hotpot | CONTAMINATION_B | EXACT_IFC | 0 | 49 | 11 |
| hotpot | CONTAMINATION_B | FLOWFENCE_R2 | 0 | 0 | 60 |
| tatqa | CLEAN | EXACT_IFC | 0 | 54 | 6 |
| tatqa | CLEAN | FLOWFENCE_R2 | 0 | 53 | 7 |
| tatqa | CONTAMINATION_A | EXACT_IFC | 0 | 52 | 8 |
| tatqa | CONTAMINATION_A | FLOWFENCE_R2 | 0 | 0 | 60 |
| tatqa | CONTAMINATION_B | EXACT_IFC | 0 | 50 | 10 |
| tatqa | CONTAMINATION_B | FLOWFENCE_R2 | 0 | 0 | 60 |

TRUE requires an observed unauthorized raw release; FALSE requires completed observation under the frozen rule. UNKNOWN remains unknown. No semantic, paraphrase or reconstruction privacy judge.

## Original-evaluator utility

| Family | Metric | Success/attempted | Rate over attempted | Scored | Success/scored | Unknown |
| --- | --- | --- | --- | --- | --- | --- |
| hotpot | joint_em == 1.0 | 16/360 | 0.044444444444444446 | 212 | 16/212 | 0 |
| tatqa | EM == 1.0 | 101/360 | 0.28055555555555556 | 207 | 101/207 | 2 |

Original metric vectors are retained in derived/evaluator_summary.json; complete evaluator inputs/outputs are retained privately. No pooled cross-family utility score. Failed ordinary episodes remain in attempted denominators. Task-level counts by family/condition/defense are in derived/execution_summary.json. TAT source-context clustering and Hotpot entity/title/context dependence restrict independence claims.

## Integrity

Saved-evidence paired initial requests verified: 360; implementation defects: 0. Frozen requests, treatment entry, release observations, raw privacy and original evaluator vectors are audited from saved trajectories by summarize_e2a_formal.py.
Postrun frozen-file verification PASSED; see artifacts/aamas2027_e2a_combined/postrun_integrity.json. Original22safe files/439private files and all3original reports are unchanged; all720identities match the frozen order; private file permissions700/600 verified. V3, stage schemas, prompts, model settings, budgets, policies, fact generation, recognizer, IFC, R2 and R3 remain subject to the original pins and Git comparison.

## Artifacts and limits

- Amendment: E2A_PREREGISTRATION_AMENDMENT.md
- Frozen schedule: E2A_FORMAL_CELL_SCHEDULE.json
- Run/artifact index: artifacts/aamas2027_e2a_combined/derived/artifact_index.json
- Treatment audit: artifacts/aamas2027_e2a_combined/derived/stage_treatment_reachability.json
- Failure audit: artifacts/aamas2027_e2a_combined/derived/failure_audit.json
- Privacy summary: artifacts/aamas2027_e2a_combined/derived/privacy_summary.json
- Evaluator summary: artifacts/aamas2027_e2a_combined/derived/evaluator_summary.json
- Reproduction: E2A_FORMAL_REPRODUCTION.md

Only TAT-QA/HotpotQA under the frozen standardized V3 harness are in scope. No four-type, complete E2, other-provider or general confidentiality claim. No formal reruns, replacements or outcome-based design changes. Stop after720or any implementation defect for human scientific review; do not select E2-B.

## Reporting correction and immutable continuation

Reporting-fix commit: `fdcc2b04035dc3e0510ab1176b26346966f402d3`. Original001–053 retained:53; original reruns:0. Continuation attempted:667/667; preflight:PASS.
The historical reporting-only defect was corrected prospectively with human authorization. No original episode triggered it or was invalidated. No source run was rewritten. Missing stage observations stay nullable/unavailable; no outcome is inferred from absent data.
Combined source index: artifacts/aamas2027_e2a_combined/combined_index.json. Reproduction: E2A_CONTINUATION_REPRODUCTION.md.

## Final evidence delivery and decision

All667authorized continuation cells finished once; original53retained unchanged. The one historical reporting-only defect was corrected before continuation; new implementation defects0and episode implementation defects0. Regression evidence: artifacts/aamas2027_e2a_continuation/reporting_fix_validation.json. No outcome-based changes or reruns. The continuation ended normally at2026-09-21T09:51:19Z.

Privacy totals: TRUE0/FALSE421/UNKNOWN299. TAT-QA utility101/360attempted (28.06%),101/207scored (48.79%); Hotpot utility16/360attempted (4.44%),16/212scored (7.55%). These denominators differ deliberately. There are421schema-valid finals but only419scored finals because2original-evaluator failures remain unknown.

50/480contaminated observations failed before a valid finance handoff (TAT26, Hotpot24); conditional430/430entry must be reported alongside unconditional430/480reachability. Frozen repeated-pre-treatment-failure flags are descriptive construct concerns, not an automatic readiness failure. No privacy superiority, task-success equivalence, fact-type causal effect or general confidentiality claim follows.

Large safe audit files are delivered as byte-identical gzip files; hydrate them with the command in E2A_CONTINUATION_REPRODUCTION.md before saved-evidence recomputation. delivery_packaging.json lists every compressed path and verified roundtrip. Full private traces and evaluator inputs remain ignored/local.

Recommended human decision / next boundary: HUMAN_E2A_SCIENTIFIC_REVIEW_NO_EXECUTION. Review the completed partial-tranche evidence and limitations before any further experiment or paper claim. E2-B remains DEFERRED_NOT_SELECTED; no automatic selection, execution, V4, rerun, merge or publication.
