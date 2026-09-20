# E2 V2 D1: READY_FOR_D2_LIVE_REVIEW

D1 is design, implementation and deterministic certification only. No provider credential was read, no model request was sent, no source evaluator was run and no V1 observation was recomputed. D2 / confirmatory / formal model executions remain zero. Readiness is for human review, not permission to execute.

## V1 closure and scientific scope

Human review closes V1 as CLOSED_CONSTRUCT_VALIDITY_FAILURE. Its 28 attempted observations (32 planner-only model requests) remain permanently unchanged. The 26 unattempted cells are separately marked V1_UNATTEMPTED_BY_HUMAN_DESIGN_STOP, never failures or observed non-reachability. The nine V1 tasks are permanently development-only and excluded from D2 and confirmatory. The historical report, source runner and observation tree remain byte-identical to 3fb3e2d7ef36509e96adba6784faa32f703f7896.

The prospective V2 amendment is explicitly informed by V1 development observations and precedes all confirmatory execution. E2 now assesses public benchmark task/evaluator external validity under a standardized multi-agent execution harness. It does not validate dynamic delegation; that scientific role remains E3. No inference that V2 would have improved historical privacy or utility is made.

## Runtime, treatment and budgets

V2 requires an actual planner invocation and accepted delegation to finance, finance invocation after consuming it and accepted handoff to writer, then writer invocation after consuming the handoff. Only trusted accepted transitions/dispatch advance flags. The selected rule B rejects premature finalize as PROTOCOL_FAILURE; neither prompts nor model-supplied flags grant authority. Even direct Session finalization is blocked by the V2 trusted runtime until completion.

Before completion, FIFO activations belonging to other stages are deferred without losing relative order. After writer invocation, existing coalesced FIFO resumes with the already-dispatched writer action executing first. Tools remain synchronous. No scripted answer, subproblem or task-specific DAG is added; all handoff contents remain model-generated in the prospective design.

A/B still enter through the unchanged first model-proposed finance→writer send, immediately before that handoff. CLEAN never injects. Tests distinguish one treatment artifact entering mediation from successful delivery: R2 quarantines the original A/B artifact and the episode ends with existing POLICY_REJECTION, without forging a handoff or writer invocation. There is no leakage requirement. Both arms use identical protocol/prompt/tool/budget paths.

The successful minimal fixtures require three mock invocations, two CLEAN or three treated messages, thirteen or fifteen runtime actions, and zero tools. Limits remain 24 model / 512 actions / 24 messages / 12 tools, with all original timeouts and token reservations. MiniMax-M2.7, temperature 0, top_p 0.9, 8192 completion tokens, zero retries/repairs and original metrics are unchanged. Prompts are hashed in experiments/e2_v2_d1/PROMPT_HASHES.json.

## Transport repair

The new V2 provider adapter retains underlying exception class, available HTTP status, safe request ID, numeric provider error code and timeout classification. It discards arbitrary error text/bodies/headers and request/credential echoes from diagnostics. Deterministic V1-versus-V2 synthetic fixtures show the original omission and repaired record, preserving one-attempt PROVIDER_FAILURE. Worker serialization, supervisor error transfer and deadline termination/join are tested. Cell16 is not replayed or reconstructed. V1 transport code remains unchanged.

## D2 selection chronology

- Scientific amendment/specification commit: d8f62e0.
- V2 adapter/prompts and initial deterministic tests commit: 8d6b3a4.
- D2 selection rule commit: 2acf2059c6b572f85188461cd50e1ad06627334d.
- Later D2 IDs/policies/schedule commit: 0b5dae5.

The metadata-only rule excludes all 69 existing selected IDs and prior TAT contexts/Hotpot overlap components, then uses lexical ordering. It never reads individual V1 outcome data or source questions/golds. D2 has three tasks per family, three distinct BIRD databases, and no TAT-context or Hotpot-component overlap with prior splits. Exactly 78 distinct IDs span V1/D2/confirmatory; each of TAT and Hotpot has 26 distinct selected contexts/components. Existing confirmatory quotas/IDs/policies remain unchanged. D2 facts use the same mechanism with new ordinals 70–78; no raw facts enter public selection files. D2 bridge/comparison quotas are not introduced; original confirmatory quotas remain fixed.

The 54-cell schedule has distinct E2_DEVELOPMENT_V2_D2 cell IDs, three conditions, two defenses and one repetition, using precommitted balanced ordering. D2 remains permanently development-only.

## Certification and limits

- 18 synthetic family × defense × condition paths; mandatory participation, exactly-once A/B entry, no CLEAN/wrong-edge/premature injection, whole-artifact quarantine, duplicate handoff, early final and unchanged budget failure.
- 23/23 transition classes and 7/7 boundaries exercised through the actual staged runtime/Session APIs, with 32 paired scenarios. Private context, principal binding, immutable snapshots, forged authority, stale/foreign/replayed commits, tool-result mediation and final/evaluator boundary tests pass. Zero modeled bypasses in this tested API scope.
- 54 D2 initial public requests constructed without dispatch; all 27 matched defense pairs identical, within unchanged context limit, with no protected fact in planner context. No source evaluator inputs supplied to models.
- All 58 P1 file pins, 45 historical R3 blobs and 10 source/evaluator pins verified unchanged. Original V1 runner/results and 60 confirmatory task/policy artifacts preserved. All V2 prompt hashes verified.

Tool certification uses deterministic trusted drafts through actual B4/B5 runtime paths; it does not repeat SQL-engine/database correctness testing. No claim covers Python reflection, OS compromise, hidden channels, live model compliance, privacy effectiveness or benchmark accuracy. The D1 package intentionally provides no live-dispatch CLI: a future reviewed D2 execution step must bind the frozen D2-only schedule to EpisodeV2/LiveProviderV2 and enforce admission before any call; the V1 CLI must never be reused for D2.

## Reproduction (no model calls)

```bash
PYTHONPATH=.:/private/tmp/e2_s0_deps python3 scripts/check_e2_v2_runtime.py --output artifacts/aamas2027_e2_v2_d1/runtime_tests.json
PYTHONPATH=.:/private/tmp/e2_s0_deps python3 scripts/certify_e2_v2.py --source-root /private/tmp/e2_s0_sources --schema /private/tmp/e2_s1r_schema.json --output artifacts/aamas2027_e2_v2_d1/recertification.json
python3 -m py_compile src/e2_live/v2.py src/e2_live/transport_v2.py scripts/check_e2_v2_runtime.py scripts/certify_e2_v2.py scripts/select_e2_d2.py
git diff --check
```

Both certification scripts deny network sockets. Dependencies/source/schema are the previously restored pinned local environment. Selection is reproducible into a fresh directory with `python3 scripts/select_e2_d2.py --rule-commit 2acf2059c6b572f85188461cd50e1ad06627334d --output /private/tmp/e2_d2_reselection`; it refuses to overwrite an existing output directory. Selection and materialization occurred in separate commits as required.

Next human decision: review the staged execution amendment, deterministic certificate and fresh D2 matrix; separately authorize any D2 live phase. Do not resume V1, rerun its cells or execute confirmatory tasks.
