# Public task/evaluator acceptance specification after the pivot

Status: **P0 design proposal, not an implemented or certified runtime**. Date: 2026-09-18.
Native benchmark-runtime search is CLOSED. No dataset search/selection, development-task selection, benchmark integration, model generation, Gate B, R3 change or frozen-recognizer change is authorized here.

PUBLIC_TASK_ACCEPTANCE_SPEC: DEFINED

This checklist is for later source screening after human acceptance of P0. It does not nominate any dataset, reopen the native-runtime search, select examples or authorize a run. Record PASS/FAIL/UNRESOLVED with source evidence per item; unknowns cannot silently become pass. Apply architecture and semantic requirements before spending effort on final task eligibility.

| Criterion | Required evidence / rejection condition |
|---|---|
| Public origin | Inspectable task release with a clear source identity and revision/version. Public paraphrases of inaccessible tasks are insufficient. |
| Reproducible data | Stable task IDs and obtainable original inputs, documented split, preprocessing and any externally fetched resources. No generated substitutions called independent public tasks. |
| License | Task, evaluator, tool/environment and derived-artifact usage compatible with intended research; separate code/data restrictions recorded. |
| Original evaluator | Inspectable original code or stable public scoring API; original success/gold/prompt/weights/thresholds/judge semantics preserved. |
| Infrastructure | Evaluator/tools runnable with available permitted infrastructure; provider requirements compatible with approved constraints. No unavailable hidden backend replaced ad hoc. |
| Representable output/state | Documented answer/state/trajectory schema reconstructable faithfully from actual standardized execution. No fabricated unmediated success trace. |
| Independent of private orchestration | Original task success/evaluator meaning does not depend on hidden native agent roles, internal reasoning traces or private scheduler behaviors the harness cannot preserve. |
| Capability equivalence | Collective tools, knowledge, source permissions and aggregate interaction limits retained without exposing additional private information. |
| Mediation-compatible effects | All modeled shared/external effects are proposed before publication through generic boundaries; no live mutable aliases or ungoverned callbacks. |
| Family-wide adapter | One fixed schema/tool mapping for the family; no task-ID/gold/condition/defense/outcome-dependent adapter behavior. |
| Frozen defense compatibility | Existing identity/channel/abstraction projection faithfully represents the required policy; unchanged recognizer and exact comparator. Unsupported surface semantics are not invented. |
| Scale | At least 23 potentially eligible semantic tasks per intended 20-task family, allowing 3 development + 20 confirmatory with deterministic disjoint selection later. |
| Orthogonal PrivacyInstance | Synthetic fact can be private to at least one existing principal and forbidden to another surface without changing clean success requirements; A/B omit raw value and use existing recognizer coverage. |
| Semantic diversity | Explain what differentiates families; relabelings, seeds and parameter permutations are not automatically distinct semantic tasks or workflows. |
| Failure fidelity | Original evaluator and source tool failures can be represented without new success criteria or silent exclusions. |

Only after a family passes source-level checks should later work enumerate task-level eligibility without inspecting defense outcomes. Determine licenses/access and deterministic selection rules before selecting disjoint development and confirmatory IDs. Then verify 60-task total and P1/P2/P3/P4=15 each jointly, not by allocating artificial fact types to semantically unsuitable tasks. Keep the preferred three-family 20+20+20 target; if no valid combination supports it, return to the human rather than reduce scale or rewrite tasks.

Prefer fewer family adapters and one runtime when scientific validity is equal. A large task count cannot compensate for a changed evaluator, missing original capability or hidden state publication. Sources rejected as native runtimes are neither automatically accepted nor permanently rejected as task/evaluator sources; no such source is evaluated or chosen in P0.
