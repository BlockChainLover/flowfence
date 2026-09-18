# Coding internal-write bypass

Classification: ADAPTER_HOOK_FEASIBLE for the reproduced `create_solution` write. This is a narrow closed surface, not full Coding mediation certification.

1. Producer: `marble/environments/coding_utils/coder.py:create_solution_handler`, model response at line 74, extraction at 84–91, `open(full_path, "w")` at 93 and `file.write(code_content)` at 94.
2. Principal: tool sub-agent invoked by the original calling MARBLE agent through `environment.apply_action(agent_id, "create_solution", ...)`. The boundary attributes the write to that caller in both arms; nested model has no independent upstream identity.
3. Destination: shared `env.workspace_dir/solution.py`, real temporary filesystem in these tests.
4. Visibility: reviewer reads it at reviewer.py:47–48; debugger reads at debugger.py:53–54; engine/evaluator later read solution.py. The original code return also contains the generated text.
5. Propagation: file → reviewer model context → revision/advice files; file → execution/test subprocess → output/error; file → official evaluator. Thus later agents/tools/results can consume it before the previous outer return wrapper can erase it.
6. Missed hook: old apply_action wraps arguments before execution and result after execution. A write during the handler occurs between them. The original 200 real-handler fixtures reproduced raw file presence in both defense arms.
7. Boundary vs semantics: generating a solution file is benchmark semantics; mediation immediately before publishing its bytes is an integration/release boundary. Removing the coding tool or changing what constitutes correct code would be a semantic intervention and was not done.
8. Hook: `RecoveredMarbleAdapter` adds a synchronous scoped `coder.open` adapter. Text writes under the original workspace are accumulated as an artifact and released through the same unchanged `inspect_r2_event` before flush/close publishes bytes. Read operations and original tool schema/capabilities are retained. No gold, evaluator labels or semantic detectors are used. No upstream handler source is rewritten.

Evidence: 200/200 original create_solution protected fixtures now have raw absent in solution.py. 200/200 normal-code fixtures compare direct original-handler and wrapped-handler output: identical file bytes and return values. Unit tests additionally cover split writes, explicit flush, both arms, original clean write length/read behavior and restoration after errors. The same original handler/state path is intercepted; this is not merely a direct call to release().

Limits: scoped hook covers coder.create_solution only, not reviewer/debugger/analyst alternate writes to the same workspace, append-only debug logs, arbitrary generated-code filesystem effects or concurrent unwrapped callers. Those are NOT claimed closed. This source-local wrapper is suitable for the synchronous audited path, not a general filesystem sandbox. The same store remains reachable through other unmediated paths; full Coding coverage and eligibility remain NOT_VERIFIED/UNRESOLVED. Hard stop applies; no capability removal or semantic rewrite was used to force certification.
