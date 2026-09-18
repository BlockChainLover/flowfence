# Original evaluator and task-semantic preservation contract

Status: **P0 design proposal, not an implemented or certified runtime**. Date: 2026-09-18.
Native benchmark-runtime search is CLOSED. No dataset search/selection, development-task selection, benchmark integration, model generation, Gate B, R3 change or frozen-recognizer change is authorized here.

ORIGINAL_EVALUATOR_PRESERVATION: FEASIBLE (conditional acceptance contract).
TASK_SEMANTIC_PRESERVATION: FEASIBLE (conditional acceptance contract).

## Original evaluator invariants

Use the public source evaluator at a documented source revision/version or its documented stable scoring API. Preserve gold/reference, success conditions, thresholds, score weights, evaluator prompt, judge semantics and relevant model/configuration. Do not rewrite a purportedly equivalent scorer, drop rubric components, substitute a new judge, lower a threshold or grade tasks by hand after results. A source requiring an unavailable fixed judge or a non-authorized provider is not made eligible by swapping it to MiniMax. MiniMax-only experiment constraints must be compatible with the source's actual evaluator contract, or the source needs a separate human scope decision; P0 grants none.

The evaluator is a trusted offline/post-episode component. It receives source-private gold/reference through a separate port inaccessible to runtime principals, tools, role prompts and defense. Its own model calls, if part of original grading, are marked evaluator calls rather than experimental propagation. This separation does not exempt real runtime effects: evaluator-private replay is distinct from a live user/shared write.

## Allowed family-level adapters

The adapter is a deterministic representation map, defined once per source family before task selection. It may serialize a final structured answer into the documented answer field, rename/reorder schema fields without altering meaning, map actual executed tool-call records into the source trajectory schema, or serialize actual committed state into its documented evaluator input. It may translate stable principal/tool identifiers with a declared bijection where the source distinguishes them. It may join generated answer fragments only by a fixed source-compatible serialization rule, not solve the task or repair the answer.

For each output field specify its source/harness lineage, type, lossless transformation and whether the evaluator consumes it. Keep original public tool/result semantics. Do not hide multiple experimental actors under a source actor ID when source scoring meaning depends on who acted; that source would be incompatible unless the original contract treats the whole solver as one logical agent.

If a source's native evaluator expects execution results different from per-recipient views, retain that distinction only where its evaluator/input contract already supports it. Use actual executed arguments, actual committed state and actual published communication. A blocked proposal is not an executed call; a quarantined phrase is not a delivered answer. No special unmediated success trajectory may be invented to avoid failure. No extra gold copy enters runtime. Do not disable replay consistency or rewrite evaluator expectations to accept a redacted record. If the expected source-semantic trace cannot be reconstructed faithfully from the standardized runner, the family is ineligible.

## Task-semantic invariants

Preserve the original objective, instance input, allowed external knowledge/tools, output requirements, evaluator and success condition. Only the problem-solving orchestration changes. Equivalent capability requires the same source-permitted observations/actions and state transition meaning, not merely a tool with the same name. Required browsing, code execution or external actions cannot be replaced with a toy mock unless the source explicitly permits that environment. No hidden tests, reference actions, answer keys, private benchmark policies or evaluator-only assertions may be sent to the coordinator or workers.

For a single-agent source, workers collectively receive no information or environment capability unavailable to its original solver. All original task-required information remains available within that collective capability set. Experimental communication is an internal decomposition mechanism, not permission for extra external tools, privileged DB reads or leaked reference solutions. Source interaction limits apply to the aggregate team. Extra reasoning or different decomposition can change performance; report it as an orchestration shift, never as native-runtime reproduction.

Source-specific tool bindings and schema conversions are allowed at a predeclared family adapter boundary. They must not branch on task ID, answer/gold, defense, contamination condition or observed outcome. Source-semantic tools themselves can naturally implement domain rules; the adapter must not introduce task-specific remediation patches. A family that needs the original private orchestration to make its score meaningful is rejected.

## Future preservation evidence required before use

For each candidate family, retain public source/license/version, documented original input/output paths and the original evaluator entry point. On public deterministic fixtures, feed equivalent outputs/states to original evaluator through native and adapted serialization and compare every original score component, including failures. Include missing/wrong output, invalid calls, rejected writes, clean no-op and representative state/trajectory cases. Verify that private evaluator fields cannot reach any runtime context. These are tests of the adapter's preservation, not new scoring criteria.

Keep all attempted episodes and original evaluator outputs/errors. If the original evaluator has a failure-score convention, preserve it. If it cannot score an interrupted or invalid run, report unscorable/evaluator failure separately; do not invent a zero/one score or count absent privacy observations as safe. Later analysis must preregister denominators and missingness, not silently discard inconvenient failures. No evaluator test or public task integration is performed in P0.

Public-scoring APIs must have a stable contract, accessible research usage, version/reproducibility evidence and retention of full returned scores/errors. If an API is opaque or drifts and equivalence cannot be checked, mark the family unresolved/ineligible rather than claim original evaluator preservation. A source's evaluator maturity is assessed later; P0 asserts no available source passes.
