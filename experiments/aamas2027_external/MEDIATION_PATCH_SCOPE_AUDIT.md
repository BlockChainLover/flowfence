# Gate A runtime patch scope

| Hook/change | Classification | Formal E2 disposition |
|---|---|---|
| ReleaseAdapter.release/value | generic integration adapter | Same frozen semantics dispatcher in both arms; no gold or task-ID rules |
| MarbleBoundaryAdapter agent act/send/receive wrappers | generic integration adapter | Partial coverage; retained for transition comparison, not full certification |
| BaseMemory update/get_memory_str, planner assign/summary/progress, engine memory wrappers | generic integration adapter | Helper-method interception is insufficient for direct backing storage/attribute paths |
| BaseEnvironment.apply_action input/return wrapper | generic integration adapter | Applies to all registered actions; returned-result coverage cannot retroactively cover nested effects |
| Engine._write_to_jsonl wrapper | generic integration adapter | Final publication only |
| RecoveredMarbleAdapter Coding name branch | environment-specific integration adapter | Historical feasibility prototype, not used by A-E formal-candidate tests |
| coder.open scoped create_solution hook | handler-specific patch/prototype | Retained as historical evidence; replaced in A-E file probes by namespace-wide builtins.open boundary |
| ArtifactWriter | generic integration primitive | Can serve whole text artifacts; not a general transparent filesystem sandbox |
| CommunicationEdges send/receive restriction | generic integration adapter/prototype | Direct-edge permission only; does not fix upstream reply schema |
| ContextBoundaryProbe | generic integration adapter/prototype | Correct with supplied trustworthy recipient; fails session attribution under outer scope |
| workspace_publication_probe | generic integration adapter/prototype | One runtime file API and workspace predicate, no list of coder/reviewer/debugger names |
| Official parser backport and approved braces patch | nonsemantic benchmark runtime repairs, not mediation hooks | Unchanged; no new benchmark semantic modification |
| SQL/HTTP/process/model/time doubles | audit-only dependencies, not defense hooks | Never claimed as mediation mechanisms |

Benchmark semantic modifications added in A-E: NONE. New handler-specific hooks: ZERO. No modifications to coder/reviewer/debugger/analyst, DB operations or individual Research tools. Existing caller wrappers and new probes live outside MARBLE.

A-E also corrects an A-D evidence overstatement: its normal-code direct/wrapped create_solution comparisons ran after a file already existed. They proved equal refusal/file preservation, not successful clean creation. A-E unlinks the fixture before creation and verifies actual successful normal publication; historical A-D artifacts remain unchanged. The protected A-D fixture did unlink before its test and is not invalidated by this correction.

Formal E2 cannot proceed by stacking more local patches. Shared-state ownership and model-recipient metadata require a common runtime redesign; no remaining handler collection is disguised as one adapter. All three environments are NOT_FEASIBLE_GENERIC_MEDIATION for the current bounded architecture. The file publication finding alone does not make Coding certifiable.
