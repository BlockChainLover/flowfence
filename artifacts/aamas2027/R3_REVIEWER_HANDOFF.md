# AAMAS R3 reviewer handoff

START_HEAD: 89fbb3e68655d82877b73c7cd5837b3019b64215
R3_PREREG_SHA: b46e60ad2282d086ade1a8ce85b4823733d23c1a
FINAL_HEAD: enclosing evidence commit; resolve with git log -1 --format=%H -- artifacts/aamas2027/R3_REVIEWER_HANDOFF.md.

Preregistration was normally pushed and GitHub HEAD verified before any R3 API. Source/method/config/analysis remained frozen throughout. No live pilot, no failed episode replacements, no new regex/detector, no E5, second model, novel rerun, extra wording/replicate, paper-body edit or merge. PR stays OPEN/Draft.

## Formal outcomes

Planned108 /terminal108 /completed106 /model failures2 /infrastructure failures0 /blocked0.
Logical generations320 /transport attempts320 /transport retries0; reported tokens136026/272083; missing-token attempts0.
Complete pairs: {'clean': 18, 'heldout_registered_A': 17, 'heldout_registered_B': 17}.

| Condition | Defense | Completed /18 | Task /18 | Disclosure episodes observed /18 | Privacy unknown | Privacy-safe /18 | Propagation events |
|---|---|---:|---:|---:|---:|---:|---:|
| clean | ifc_safeview | 18 | 18 | 0 | 0 | 18 | 0 |
| clean | flowfence_lite_nonoracle_r2 | 18 | 18 | 0 | 0 | 18 | 0 |
| heldout_registered_A | ifc_safeview | 17 | 16 | 6 | 1 | 11 | 18 |
| heldout_registered_A | flowfence_lite_nonoracle_r2 | 18 | 16 | 0 | 0 | 16 | 0 |
| heldout_registered_B | ifc_safeview | 17 | 16 | 7 | 1 | 9 | 21 |
| heldout_registered_B | flowfence_lite_nonoracle_r2 | 18 | 18 | 0 | 0 | 18 | 0 |

Primary disclosure counts each completed episode at most once; multiple delivery events can be repeated propagation of one disclosure. Failed/blocked privacy remains unknown. Full-response/parsed-action attempts are diagnostics, not primary recipient observation. Raw counts/18 expose coverage, while completed-only rates and matched comparisons have their own denominators. All hold/approve and external-send results remain in derived tables.

## Utility qualification for Independent Review

The primary A task tie16/18 vs16/18 includes the IFC model failure as unsuccessful execution. Among17 both-completed A pairs, R2 is15/17 versus IFC16/17. The primary Case A flags remain as preregistered, but completed-pair utility preservation is unsupported; a descriptive matched-A privacy–utility tradeoff is visible. See derived/INTERPRETATION.md and matched_condition_summary.csv. Two R2 completed A wrong answers and both IFC planner failures are retained.

## Task clusters and decisions

The complete6-task x3-condition cluster table is in derived/paired_task_cluster.csv; all3 replicate outcomes in per_task_replicates.csv and all54 matched cells in paired_episode.csv. Primary privacy compares both-completed repetitions within each task, then equal task weights; utility uses registered successes/3 per task. Failed pairs are unavailable for scientific paired differences. No population/domain significance or controlled provider RNG seed.

Configured semantic-request-triggered quarantine showed an incremental containment benefit over exact-value IFC on two held-out registered-request phrasings in the evaluated workflow.

R3_CONFIRMATORY_EVIDENCE_COMPLETE: YES
BOTH_HELDOUT_PRIVACY_BETTER: YES
HELDOUT_UTILITY_PRESERVED: YES
CLEAN_UTILITY_PRESERVED: YES
STABLE_REGISTERED_PATTERN_BENEFIT: YES
PRIVACY_UTILITY_TRADEOFF: NO
PAPC_R2_CONFIRMATORY_ADVANTAGE: YES
GENERAL_SEMANTIC_CONFIDENTIALITY: NO
NOVEL_PARAPHRASE_ROBUSTNESS: NO

Supported observations:
- Configured semantic-request-triggered quarantine showed an incremental containment benefit over exact-value IFC on two held-out registered-request phrasings in the evaluated workflow.

Unsupported claims:
- General semantic confidentiality or arbitrary/novel paraphrase robustness.
- General multi-agent or population-wide/statistical superiority; six instances are one enterprise family.
- Arbitrary mixed-content quarantine preserving all useful content; task-critical structured state remains separate.
- Topology contribution, cross-model generalization, or results from any additional benchmark or experiment.
- Replacing or erasing R1/R1.1/R2/E3/E4 limitations or negative evidence.

Six parameterized instances of one enterprise task family. Task-critical structured state is maintained separately from the quarantined untrusted note. Held out from previous experimental wording, not pre-existing detector vocabulary. No population significance or arbitrary mixed-content utility claim.

## Validation and retained evidence

Frozen method/IFC/task/prompt SHA256 values and exact A/B text/hash are in R3_FROZEN_INPUTS.json and R3_EXPERIMENT_PREREGISTRATION.md. Full paired schedule is R3_SCHEDULE.json; runtime schedule.jsonl audits wait-for-both barriers and alternating submission order. Source freeze, existing detector matches, absence from prior wording, no raw secret, no oracle, retry rules and safe artifact checks are retained in R3_validation/.
Pre-API tests:26 R3 tests,208 AAMAS targeted,44 relevant runtime passed; full276 passed/1 pre-existing exporter failure on missing papers/claims_checklist.md,0 skipped/xfail. Final offline replay/source preservation/safe audit is in final_audit.json. No unrelated exporter repair.
Original dirty desktop checkout untouched; all work in /private/tmp/flowfence-aamas-r11-w4EWq4Ac. Live execution retained at /tmp/flowfence-aamas-r3-20260914-w4EW on wentian-server. Private full traces stay outside repo at /tmp/flowfence-aamas-r3-20260914-w4EW-private/formal, dirs0700/files0600; credential env referenced externally only. Historical R1/R1.1/R2/E3/E4 negative/incomplete evidence unchanged.

Rebuild without API: `PYTHONPATH=. python scripts/summarize_aamas_binding_r3.py --input artifacts/aamas2027/R3_CONFIRMATORY/formal --output /private/tmp/r3-independent-rebuild`.

READY_FOR_INDEPENDENT_REVIEW: YES. Review concerns the actual coverage and conditional scope above; it is not submission acceptance.

NO MORE EXPERIMENTS. Stop for Independent Review and later paper rewrite. No additional model call, wording, replicate, detector change, E5 or merge.
