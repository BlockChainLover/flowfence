# E2-A formal report

**FORMAL CONFIRMATORY EVIDENCE — PARTIAL E2 TRANCHE**

Status: NOT_READY. Preregistration commit: `2a8e3910a133862a0df9f53a47131d798da047c1`.
Planned primary semantic units: **40 public benchmark tasks**, 20 TAT-QA and20 HotpotQA. The720episodes are repeated observations, not720independent samples. P1=15/P2=15/P3=10/P4=0. Fact type is coupled to family; no causal fact-type comparison.

BIRD was withdrawn before formal execution due to runtime-capability infeasibility under the frozen160000-byte guard; zero formal BIRD episodes. This is neither a negative privacy result nor a failed defense experiment. All historical IDs remain preserved. E2_B_STATUS: DEFERRED_NOT_SELECTED. Broader60-task E2 is incomplete.

## Implementation hard stop

A zero-call isolated fixture confirmed that the saved-evidence auditor crashes on the minimal setup-defect record the runner can emit (`KeyError: planner_stage_success`). This path did not occur in the actual53episodes. Existing observations remain valid; the user's implementation-defect rule nevertheless required stopping new cells upon discovery. No patch, resume or rerun occurred. See E2A_IMPLEMENTATION_DEFECT_REVIEW.md. Only27of40planned tasks were observed (13TAT-QA/14HotpotQA); the prefix is unbalanced and cannot represent the completed720-cell tranche. Cell053was in flight when STOP was written and completed; no054started.

## Execution

Expected720; attempted53; finished53; valid ordinary observations53; completed finals34; unattempted by hard stop667; pending/in-flight0.

| Termination | Count |
| --- | --- |
| POLICY_REJECTION | 17 |
| PROTOCOL_FAILURE | 2 |
| SUCCESSFUL_FINAL | 34 |

Provider and infrastructure failure counters overlap under the retained historical reporting convention. Transport timeout flags can overlap provider failures; do not add overlapping counters. A schema-valid final is not necessarily a correct answer.

| Family | Condition | Defense | Repetition | Attempted | Finals |
| --- | --- | --- | --- | --- | --- |
| hotpot | CLEAN | EXACT_IFC | 1 | 5 | 4 |
| hotpot | CLEAN | FLOWFENCE_R2 | 1 | 5 | 5 |
| hotpot | CONTAMINATION_A | EXACT_IFC | 1 | 4 | 4 |
| hotpot | CONTAMINATION_A | FLOWFENCE_R2 | 1 | 4 | 0 |
| hotpot | CONTAMINATION_B | EXACT_IFC | 1 | 5 | 5 |
| hotpot | CONTAMINATION_B | FLOWFENCE_R2 | 1 | 4 | 0 |
| tatqa | CLEAN | EXACT_IFC | 1 | 4 | 3 |
| tatqa | CLEAN | FLOWFENCE_R2 | 1 | 4 | 4 |
| tatqa | CONTAMINATION_A | EXACT_IFC | 1 | 5 | 5 |
| tatqa | CONTAMINATION_A | FLOWFENCE_R2 | 1 | 5 | 0 |
| tatqa | CONTAMINATION_B | EXACT_IFC | 1 | 4 | 4 |
| tatqa | CONTAMINATION_B | FLOWFENCE_R2 | 1 | 4 | 0 |

## Treatment

| Condition | Scheduled | Valid finance | Mediated | Quarantined | Released | Delivered | Pre-handoff failure |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CONTAMINATION_A | 240 | 18 | 18 | 9 | 9 | 9 | 0 |
| CONTAMINATION_B | 240 | 17 | 17 | 8 | 9 | 9 | 0 |

Conditional entry: {'entered': 35, 'valid_finance_handoff': 35, 'rate': 1.0}. Each contaminated episode has separate stage/treatment/writer/final accounting in derived/stage_treatment_reachability.json. Non-reachability is not privacy success. Terminal R2 quarantine permits no replacement semantic handoff or writer.

## Raw-value privacy

| Family | Condition | Defense | TRUE | FALSE | UNKNOWN |
| --- | --- | --- | --- | --- | --- |
| hotpot | CLEAN | EXACT_IFC | 0 | 4 | 1 |
| hotpot | CLEAN | FLOWFENCE_R2 | 0 | 5 | 0 |
| hotpot | CONTAMINATION_A | EXACT_IFC | 0 | 4 | 0 |
| hotpot | CONTAMINATION_A | FLOWFENCE_R2 | 0 | 0 | 4 |
| hotpot | CONTAMINATION_B | EXACT_IFC | 0 | 5 | 0 |
| hotpot | CONTAMINATION_B | FLOWFENCE_R2 | 0 | 0 | 4 |
| tatqa | CLEAN | EXACT_IFC | 0 | 3 | 1 |
| tatqa | CLEAN | FLOWFENCE_R2 | 0 | 4 | 0 |
| tatqa | CONTAMINATION_A | EXACT_IFC | 0 | 5 | 0 |
| tatqa | CONTAMINATION_A | FLOWFENCE_R2 | 0 | 0 | 5 |
| tatqa | CONTAMINATION_B | EXACT_IFC | 0 | 4 | 0 |
| tatqa | CONTAMINATION_B | FLOWFENCE_R2 | 0 | 0 | 4 |

TRUE requires an observed unauthorized raw release; FALSE requires completed observation under the frozen rule. UNKNOWN remains unknown. No semantic, paraphrase or reconstruction privacy judge.

## Original-evaluator utility

| Family | Metric | Success/attempted | Rate over attempted | Scored | Success/scored | Unknown |
| --- | --- | --- | --- | --- | --- | --- |
| hotpot | joint_em == 1.0 | 1/27 | 0.037037037037037035 | 18 | 1/18 | 0 |
| tatqa | EM == 1.0 | 8/26 | 0.3076923076923077 | 16 | 8/16 | 0 |

Original metric vectors are retained in derived/evaluator_summary.json; complete evaluator inputs/outputs are retained privately. No pooled cross-family utility score. Failed ordinary episodes remain in attempted denominators. Task-level counts by family/condition/defense are in derived/execution_summary.json. TAT source-context clustering and Hotpot entity/title/context dependence restrict independence claims.

## Integrity

Saved-evidence paired initial requests verified: 26; episode-level implementation defects: 0; separately confirmed run-level failure-accounting implementation defect: 1. Frozen requests, treatment entry, release observations, raw privacy and original evaluator vectors are audited from saved trajectories by summarize_e2a_formal.py.
Postrun frozen-file verification passed and is recorded in artifacts/aamas2027_e2a_formal/postrun_integrity.json. The run-level review decision is artifacts/aamas2027_e2a_formal/review_decision.json. V3, stage schemas, prompts, model settings, budgets, policies, fact generation, recognizer, IFC, R2 and R3 remain subject to the original pins and Git comparison.

## Artifacts and limits

- Amendment: E2A_PREREGISTRATION_AMENDMENT.md
- Frozen schedule: E2A_FORMAL_CELL_SCHEDULE.json
- Run/artifact index: artifacts/aamas2027_e2a_formal/derived/artifact_index.json
- Treatment audit: artifacts/aamas2027_e2a_formal/derived/stage_treatment_reachability.json
- Failure audit: artifacts/aamas2027_e2a_formal/derived/failure_audit.json
- Privacy summary: artifacts/aamas2027_e2a_formal/derived/privacy_summary.json
- Evaluator summary: artifacts/aamas2027_e2a_formal/derived/evaluator_summary.json
- Reproduction: E2A_FORMAL_REPRODUCTION.md

Only TAT-QA/HotpotQA under the frozen standardized V3 harness are in scope. No four-type, complete E2, other-provider or general confidentiality claim. No formal reruns, replacements or outcome-based design changes. Stop after720or any implementation defect for human scientific review; do not select E2-B.
