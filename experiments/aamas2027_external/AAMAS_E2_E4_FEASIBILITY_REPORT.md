# Gate A-R recovered audit

AAMAS_EXPANSION_GATE_A: NOT_READY

Parser repair is complete. Remaining blockers concern evaluator/topology semantics, adapter integration and reproducibility; import success alone would not resolve them. No live scientific generations occurred.

## Repository and repair

Continue isolated branch codex/aamas2027-gate-a at START_HEAD b8f733e (full SHA in RECOVERY_START.json), based on R3 evidence e3b646bbb7a05503457a6b62f9fe09f078eca4eb. Original desktop checkout remains untouched; no merge or history rewrite.

Canonical [MARBLE](https://github.com/ulab-uiuc/MARBLE) base `8d60fa17b5596b44458a52d4296061b9fc13d6f2`. Cause UPSTREAM_SOURCE_BUG, blob0557ac1037d086019d119cc9927119cf73e5d102, same canonical bytes. Applied exact evaluator-only backport from official fix/coding branch commit `40ddb54b5a379b53196d1bdf20e861dc6f922e19`; no repin. Effective identity: base + patch SHA256 `8019ffcdf3affd9698c6702d5ae106b4b63ef651d4a7383d42bce5a885afc68f`. See BENCHMARK_REPAIR_PROVENANCE.md and BENCHMARK_PATCH_MANIFEST.json. No other upstream edit.

93 Python files compile on supported Python3.10.9. Evaluator class construction, original research prompt formatting, JSON parsing, coding score fallback, DB result schema and24 recognizer/direct-input fixtures pass without live models. Full dependency import is NOT established: direct import currently reports missing litellm. Installing all dependencies was not pursued as a substitute for resolving the substantive evaluator/topology mismatch. No environment construction with database side effects occurred.

## Official task inventory and engineering eligibility

| Environment | Official IDs | Structurally valid records | Verified eligible now | Status |
|---|---:|---:|---:|---|
| Research |100|100|0|NOT_READY|
| Database |100|100|0|NOT_READY|
| Coding |100|100|0|NOT_READY|

Zero means none satisfies ALL current integration/reproducibility criteria; it does not mean all100 are intrinsically unusable. Each inventory row records concrete common and environment-specific blockers. Every task content, agent ID uniqueness, relationship endpoint, and DB initialization/label field was inspected programmatically. Actual runnable task count is NOT ESTABLISHED. Requirement≥23 per environment is not met by evidence. No rejection is based on outcomes.

Research has1–22 agents depending on record;98 distinct task-content strings, with duplicate content IDs8/91 and41/57. Database has5 agents per record,100 distinct full task definitions but only20 distinct task-content strings: root_causes and initialization differ, so repeated wording alone must NOT collapse them into20 semantic tasks. Coding has3 agents and100 distinct task-content strings. Independently review research duplicate objectives before future selection; identical IDs are not the semantic scale.

## Research Collaboration

Initialization: official multiagentbench/jsonl2yaml.py fills empty config values; Engine._initialize_environment creates ResearchEnvironment and official agent profiles/relationships. Tools register publication/coauthor/arXiv retrieval through HTTP-based helpers. Agent-local memory/msg_box and planner memory hold text; summaries and delegation form shared information paths. All listed tool actions remain available to both defenses. Augmentation can add a synthetic internal project sidecar without changing the research objective; task-level semantic compatibility still requires reviewed authorization placement.

Original utility: Evaluator.evaluate_task_research, final summary scored on innovation/safety/feasibility, prompt range1–5 each, no hard success threshold. Parser casts integers without range enforcement; leave unchanged. Judge is metrics.evaluate_llm (official converter default gpt-4o); no deterministic guarantee at temperature0. No gold answer read by this utility method. Engine.finalize's generic task_completion proxy is not a replacement for this judge score. Report raw dimensions; any mean is explicitly descriptive, not a new benchmark-defined success rule.

Status NOT_READY: full dependency/tool prerequisites and mediator unvalidated. Original utility can remain unchanged if judge selection is preserved and privacy evaluated separately. Selecting a different judge is not a silent compatibility repair.

## Database Error Analysis

Initialization: DBEnvironment starts docker compose, initializes SQL and anomaly scripts and waits for monitoring alerts. Docker images include floating postgres and prom/prometheus:master; source pin alone does not fix environment images. Tools expose alerts, abnormal metrics, RAG, SQL query and slow-query information. sql/root_causes/labels are task initialization/evaluation data; enforcement must never receive gold labels.

Original utility is a two-stage pipeline: Evaluator.evaluate_task_db stores prediction/root_cause; scripts/database/batch_eval.py uses hardcoded gpt-4o-mini to extract two predicted labels, then exact label membership score matched_gold/len(gold),0–1 (0 for empty gold), averages tasks and multiplies100. Model extraction is stochastic; exact comparison deterministic. Prompt/request trim_messages uses16384×0.6 token budget, output512, temperature0. No completion threshold. Model/judge failures are skipped in upstream aggregation; future audit must retain registered unknowns separately, not silently inherit exclusions.

Status NOT_READY: isolated Docker/SQL prerequisites not validated, full mediation missing, and original utility judge conflicts with MiniMax-only experiment scope unless explicitly authorized as an evaluator exception. Changing judge would alter the original evaluator behavior and is not allowed as a syntax repair. Synthetic incident sidecar is plausible; actual incident labels must never be replaced by protected-fact labels.

## Coding Collaboration

Tools create_solution and reviewer generate code via nested model calls and write solution.py/advice logs. They read a fixed coding_config.yaml instead of the passed task_description. Official update_coding_config utility can stage task inputs, but paths are inconsistent across handlers, Engine and evaluator. Workspaces need per-episode isolation and correct official config staging; this has not been certified.

Evaluator.evaluate_code_quality reads fixed YAML and solution.py (ignores incoming task/code_result for its input construction), uses self.llm; returns instruction_following/executability/consistency/quality,1–5. Malformed/missing/out-of-range values become1. Prompt explicitly instructs random perturbation if all four scores equal; this stochastic judge behavior must be retained, not repaired. No actual execution/test-suite pass metric or pass threshold is defined by this evaluator. No gold code accessed here. Original prompt remains untouched.

Critical blocker: graph_coordinate contains NO evaluate_code_quality dispatch, whereas star_coordinate does and requires a file at another fixed path. Thus GRAPH cannot retain Coding utility as written. Adding a call is new evaluation behavior, not part of the authorized parser fix. STOP: SEMANTIC_BENCHMARK_REPAIR_REQUIRED for that proposed repair. No such edit was made.

## STAR versus GRAPH audit

coordinate_mode chooses Engine methods and is logged as coordination_mode. AgentGraph uses the same configured relationships for STAR and GRAPH; selecting STAR does NOT create a star adjacency graph. GRAPH initially assigns the whole task to all agents; subsequent iterations call each agent.plan_task. STAR uses central planner.assign_tasks each iteration. Summarization, progress updates, generation budgets and termination ordering differ. GRAPH disables communication/planning/KPI evaluation and writes-1; STAR calls all three. Coding evaluator exists only in STAR. These automatic differences are not controlled by one additional config field.

Task/agent model/environment/tool list could stay constant, but evaluator/coordination capabilities do not. It is currently a bundled coordination-protocol comparison, not a topology-only intervention. STAR_GRAPH_FEASIBILITY: NOT_READY. Do not normalize either branch silently; human scientific-design review required.

## Defense, privacy and state

EXACT_IFC_PARITY: NOT_VERIFIED end-to-end. Direct callable same-input fixtures pass; see checklist. Frozen recognizer hash6bb7cba43724c10213ee4d81cdf2f82877fa6f5b831ca71c0698495866307d62, R2 wrapper unchanged. Three environments×four classes×A/B=24 synthetic static fixture cases: raw value absent, recognizer true, IFC admits source and R2 releases constant marker. These are source-coverage tests only, not attack successes, reconstruction evidence or proof that all task augmentations are valid. NEW_RULES_ADDED:0.

MEDIATION_COVERAGE: NOT_VERIFIED. See complete source-surface matrix; nested tool writes/calls, planner summaries and debug logs remain unmediated. Original evaluator/gold is excluded from enforcement input. ORIGINAL_EVALUATOR_SEMANTICS_CHANGED_BY_ADAPTER:NO (only parser backport applied; no adapter installed).

Four fact classes are plausible as synthetic sidecars: research project budget/reference/status/opaque access reference; DB incident remediation budget/internal incident ID/status/nonfunctional service reference; coding project budget/repository ID/review status/nonfunctional build reference. Clean completion must ignore unauthorized raw value. No final values, attack trials or task-specific recognizer patches assigned.

## E3 and E4-A

E3 implementable as a new dispatcher reusing frozen policy/events/R2 primitives, not E1's fixed runner. Current role/topology helpers include fixed enterprise names; use explicit edge objects and registry entries without modifying those helpers or inferring privilege. Implementation still pending; E3_DYNAMIC_DELEGATION: READY as architecture feasibility only, not measured runtime validity. See E3 spec.

Second-family options and integration constraints are documented in SECOND_MODEL_FEASIBILITY.md. Three currently documented options, none selected/called; API route is feasible with adapter work, not drop-in compatibility. Provider accounts/entitlements untested.

## Failure, budget and remaining decision

model_prompting outer decorator catches all exceptions for up to5 total attempts; it can retry post-response failures. SDK retries are not audited. Engine catches per-agent errors and continues; ordinary output presence does not prove completion. Retain all logical/transport records, failures and unknown privacy states; no replacement. Formal runs remain forbidden.

Sizes unchanged: E2 1080,E3 324,E4-A288,E4-B288=1980 new; E1 adds108=2088 study executions, target84 semantic tasks. No statistical results or power claims. Draft metrics and E1/R3 remain unchanged. Dev/confirm selection algorithm is deterministic but no actual eligible split is certified.

License correction: root LICENSE is MIT (copyright2024 Haofei Yu), while pyproject says Apache2.0; preserve notices and clarify upstream metadata discrepancy before redistributing a bundled benchmark/datasets. Only minimal patch, license and metadata are included here.

NEXT_GATE: human review of Coding evaluator/STAR-GRAPH semantic mismatch and original judge authorization; continue Gate A recovery if approved. Do not begin Gate B.
