# R1 independent reviewer handoff — partial formal evidence

PR: https://github.com/BlockChainLover/flowfence/pull/1
Source/preregistration commit: a34dc1bd7e135c2f6b0f903b59604b19bbff6b46. No amendment or outcome-based input change. Final evidence commit is the branch tip after this handoff is committed.

## Operational outcome

108/108 terminal cells; 25 completed, 51 failed, 32 blocked. Formal requests 135, input/output reported tokens 54344/113938; pilot separately 5 requests, 2089/4559 tokens. Total requests 140, no retry, MiniMax-M2.7 requested/returned. Consecutive HTTP 529 infrastructure failures triggered the predeclared stop. Failed formal cells: 44 length-truncated JSON responses, six HTTP 529, one interrupted-in-progress call prevented locally by the stop rule. Generic BLOCKED_BY_API on 32 unstarted rows is a runtime placeholder for this infrastructure stop, not 401/403. All model parser failures have finish_reason=length. No provider execution continued after stop.

## Scientific interpretation

SUPPORTED: corrected metric separation, immutable historical replay, a constructed decision-binding six-instance family, and real model-assisted approve coordination in a subset of four approve instances. The registry cap changes every public optimum by construction; relaxing it in a deterministic counterfactual restores the public optimum.

MUST NARROW: there are no completed hold episodes and no complete PAPC/IFC pair in either attack condition. Only seven complete privacy pairs exist, all clean. Both delivered exposure counters are observed zero, which cannot establish confidentiality on failed, blocked or unattempted conditions. The pre-mediation counters cover full returned responses before reasoning-tag stripping/parsing, so they are broader than outgoing-action disclosure attempts. They do not establish unsafe-action prevention.

NOT SUPPORTED: PAPC-specific confidentiality or overall utility advantage, general semantic confidentiality, novel-paraphrase protection, topology-specific algorithmic contribution, robust hold coordination, or an AAMAS headline superiority claim. PAPC and IFC both achieve 7/36 task and privacy-safe successes, with task wins/ties/losses 2/32/2; None achieves 9/36. Completed privacy pairs tie 7/7 with 29 unavailable, not 36 ties. PAPC full-response exact/reconstruction counters are 14/5 versus IFC 8/0 and None 11/2; these are diagnostic counts, not final breaches. PAPC intervenes/re-writes eight times; IFC/None zero. No defense has a delivered exact/reconstruction disclosure observed in the retained partial traces.

The predeclared descriptive topology interaction rule fires on small task-success differences, so E5 is TRIGGERED_PENDING_HUMAN_APPROVAL; no ablation was run and no causal topology claim follows. Old E3 remains 90/90 reconstruction failures and old E4 remains 20 HTTP 403 failures.

## Review steps

Read R1_PREREGISTRATION.md, R1_METRIC_DEFINITIONS.md, R1_MANIFEST.json and E6_binding_semantic/derived/REPORT.md. Inspect frozen defense/policy equality and the common source/prompt/role hooks. Recompute using `PYTHONPATH=. python scripts/integrate_aamas_r1.py`, which validates safe event/attempt counters against episode records and writes new derived summaries only. Review generated_attempts.jsonl separately from events.jsonl; do not infer privacy from incomplete zero counters. Inspect per-task, per-topology and condition CSVs and all failure records.

Review whether the full-response attempt proxy is adequate for the scientific question; it must not be sold as action-only attempted exfiltration. Check that the model-completion bottleneck and absent live hold coverage block a strong discrimination claim. Any further live experiment requires a new approved work package; no implicit resumption or parameter change is authorized by this handoff.

Validation: 96 targeted passed; 123 relevant passed; full suite 164 passed / one pre-existing missing papers/claims_checklist.md failure; no skips/xfail. Safe scan, byte-identical historical comparison and bundle replay are recorded in R1_validation. Complete final git/source verification follows in the publication log.

READY_FOR_INDEPENDENT_REVIEW: YES
FORMAL_EVIDENCE_COMPLETE: NO
PAPC_SPECIFIC_ADVANTAGE_OBSERVED: NO
SEMANTIC_GENERALIZATION_SUPPORTED: NO
TOPOLOGY_CONTRIBUTION_SUPPORTED: NO
