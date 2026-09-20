# E2 development pilot — 2026-09-20

**AAMAS_E2_DEVELOPMENT_PILOT: NOT_READY**

**DEVELOPMENT_ONLY — NOT CONFIRMATORY EVIDENCE**

## Outcome and hard stop

The authorized frozen schedule was executed through cell28; cells29–54 remain unattempted. There were28valid development observations,18released finals scored by original evaluators and32provider requests. All ordinary failures remain observations: none were invalidated or replaced. “Valid” here does not assert a complete diagnostic record: cell16has a known incomplete transport-failure audit.

During read-only live audit, cell16's PROVIDER_FAILURE record was found to retain only a generic failure/timeout flag, with no exception class or available HTTP error response metadata. `_worker` returns only the exception type; `supervised` raises it, and `provider_action` discards it. The exact failure cause cannot be reconstructed. There is no basis to invent an HTTP status or claim that a provider error response was definitely available. This is an implementation logging defect, not a scientific outcome or low-model-performance stop.

At discovery27cells had finished and28was in flight. To stop NEW cells without killing the in-flight request or editing code, the append-only admission file attempts.jsonl was made read-only. Cell28finished and retained its normal final/evaluator result. The next append failed before cell29Runtime or provider construction. An empty private cell29directory is not a trajectory or attempt. The intentional PermissionError is not an extra provider/infrastructure episode failure. The stop request/completion records document this control action. No live code was patched; no automatic resume, retry or rerun occurred.

**Unresolved implementation defect:** transport error diagnostics are incomplete. All28existing observations and private artifacts must remain. Human review is required before a generic implementation repair or any further execution; no repair/re-execution authority is inferred.

## Preregistration and chronology

- PRE_RUN_PREREG_COMMIT:9290f71b9a3f8dd02334f88f7f331eb61751bd03
- HOT_POT_METRIC_FREEZE_COMMIT:1d67d65cc1974d18430b797c82658833a14937f7
- FIRST_LIVE_RUNNER_COMMIT:f4dcc6e34720fa0763c74ed5fe28c8a92d5febe4
- LIVE_CONFIG_FREEZE_TIMING:AFTER_DETERMINISTIC_TASK_SELECTION_BEFORE_ANY_MODEL_OUTCOME
- HOT_POT_METRIC_FREEZE_TIMING:AFTER_TASK_SELECTION_AND_P1_BEFORE_ANY_MODEL_OUTCOME

The human Hotpot clarification was committed/pushed before live runner implementation. The runner was committed before dispatch. P1/R3 preservation, pinned source/evaluator files and original restored PostgreSQL14.24UTF8/C/Asia-Shanghai schema were verified. All58P1manifest entries and45R3blobs remain unchanged after execution; all10source/evaluatorfiles remain pinned. Frozen recognizer remains6bb7cba43724c10213ee4d81cdf2f82877fa6f5b831ca71c0698495866307d62. No selection, policy, fact, prompt, scheduler, budget, contamination template, evaluator, R2 or IFC change occurred. No history rewrite.

## Engineering validation and limitations

Before dispatch,54complete mock cells plus strict parsing, FIFO, quarantine rejection,24call cap and confirmatory admission denial passed. Three original source-reference fixtures passed; actual read-only broker SELECT/write-denial and process deadline cancellation passed. These tests are distinct from model evidence.

The post-run audit recomputed all28trajectory hashes, exact raw-value disclosure observations, frozen request objects, and FIFO acting sequences. All32live model calls were to planner_agent; finance_agent and doc_writer_agent were NOT live-invoked. Their trusted mappings were statically/mock validated only. Both defenses shared the same task/model/prompt/tool/budget/scheduler path; no capability difference was found. Recorded live boundaries include B1/B3/B4/B5/B6/B7; B2 inter-agent delivery/quarantine was only exercised by deterministic fixtures, not these live trajectories. Do not claim all live multi-agent paths were exercised or live contamination containment was demonstrated.

Original evaluators scored18actual released finals with no evaluator integration failure. Model aliasMiniMax-M2.7 was returned on31responses; one failed call has no returned model metadata. This alias does not pin immutable weights. Requested provider/model/endpoint/sampling remained frozen. Usage over31reported responses:200368prompt tokens,11661completion tokens,212029total; one failed request has unknown usage. No monetary cost is reported. No significance tests, confidence intervals, ranking or effectiveness claims.

## Failure taxonomy

| Termination | Episodes |
|---|---:|
| SUCCESSFUL_FINAL |18|
| PROTOCOL_FAILURE |5|
| TOOL_FAILURE |2|
| CONTEXT_LIMIT |2|
| PROVIDER_FAILURE |1|
| All other episode terminations |0|

One implementation audit defect was discovered separately; it does not relabel the ordinary provider failure. Provider failure also counts as infrastructure failure, so those two counts overlap. Timeouts0; budget exhaustion0; policy rejections0; evaluator failures0. No invalidated runs, reruns or task replacements. Exact breakdown by family/condition/defense is in derived/failure_audit.json.

## Development-only privacy and utility

| Family | Attempted | Scored finals | Original task successes | Episode failures | Privacy TRUE / FALSE / UNKNOWN |
|---|---:|---:|---:|---:|---|
| BIRD PostgreSQL |12|5|0|12|0 /5 /7|
| TAT-QA |6|5|2|4|0 /5 /1|
| HotpotQA |10|8|0|10|0 /8 /2|

BIRD task_success is original EX; F1/VES diagnostic-only and not rerun. TAT-QA uses existing original EM==1.0, retaining F1/scale/operation fields. Hotpot uses original joint_em==1.0 and all12original answer/support/joint metrics are retained. No evaluator or normalization was modified. Of18scored finals,2meet their disclosed family criteria; ordinary pre-final terminations account for the remaining episode failures. These are simple descriptive counts, not a pooled utility metric.

Privacy TRUE0/FALSE18/UNKNOWN10. FALSE means a completed negative observation under the frozen raw-value criterion, not semantic confidentiality. No finance worker was invoked; no protected-value use or contaminated handoff occurred. Therefore these negative observations cannot support a containment effectiveness claim. Failed incomplete episodes remain UNKNOWN, never safe by default. Attempted, candidate and committed release views remain distinct.

## Contamination reachability

| Condition | Scheduled | Attempted | Reached | Not reached | Unattempted |
|---|---:|---:|---:|---:|---:|
| A |18|10|0|10|8|
| B |18|10|0|10|8|

CONTAMINATION_CONSTRUCT_VALIDITY_CONCERN:YES. Among attempted contaminated trajectories, BIRD0/8, TAT-QA0/4andHotpot0/8reached the registered finance→writer edge. This is partial observed systematic non-reachability, with remaining cells unobserved. A/B were not injected because the frozen trigger never occurred. No forced handoff, prompt tuning, replacement or rerun was performed. Breakdown by each family/condition/defense/task is in derived/contamination_reachability.json.

## Artifact index and reproduction

Safe artifacts: artifacts/aamas2027_e2_development_live/. Start with artifact_index.json, implementation_defect.json, postrun_integrity.json, run/registration.json and derived/summary.json. The run directory preserves all attempts/episode metadata, stop request and stop completion. derived/episode_summary.json retains complete safe episode records; runtime_audit.json contains verified metric vectors; release_audit.jsonl records every boundary's safe decision/hash metadata. Raw trajectory hashes are in episode summaries.

Raw local audit: /Users/crazy/Desktop/agent-privacy-defense/FlowFence-Lite/data/secrets/e2_development_20260920/raw (Git-ignored; private files600). Includes requests, successful provider response metadata/reasoning, actual SQL/evaluator inputs/outputs, attempted/candidate/published views and full typed traces. The explicit diagnostic gap for cell16cannot be recovered or filled by guessing. The copied credential is outside the raw artifact index and is never committed. User explicitly approved the limited credential transfer after the automatic reviewer initially rejected it.

Run commands and implementation boundary are in E2_LIVE_RUNNER_REPRODUCTION.md. Recompute reports only:

```bash
PYTHONPATH=.:/private/tmp/e2_s0_deps python3 scripts/summarize_e2_development_pilot.py --run artifacts/aamas2027_e2_development_live/run --private /Users/crazy/Desktop/agent-privacy-defense/FlowFence-Lite/data/secrets/e2_development_20260920/raw --output artifacts/aamas2027_e2_development_live/derived
```

This reads saved artifacts only, invokes no models/evaluators, and scans safe outputs for instantiated raw values. No execution command should be relaunched without human review. The live-runner bytes are verified unchanged from FIRST_LIVE_RUNNER_COMMIT; reporting code was added afterward without changing runtime/scientific semantics.

FORMAL_MODEL_RUNS_EXECUTED:0. CONFIRMATORY_TASKS_EXECUTED:0. OUTCOME_BASED_DESIGN_CHANGES:NO. IMPLEMENTATION_FIXES_AFTER_FIRST_OUTCOME:NONE. RERUNS_PERFORMED:0.

Next human decision: review the logging defect and incomplete coverage, approve any generic diagnostic repair and explicit continuation policy separately, and assess observed contamination non-reachability without silently modifying the frozen design. Do not start confirmatory execution.
