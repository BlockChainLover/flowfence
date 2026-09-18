# Gate A feasibility report

AAMAS_EXPANSION_GATE_A: NOT_READY

Audit date: 2026-09-18. This is a hard-stop report, not a completed feasibility audit.

## Repository state and provenance

Original checkout: `/Users/crazy/Desktop/agent-privacy-defense/FlowFence-Lite`, branch `codex/aamas2027-experiment-extension`, HEAD `2a179d37e4b93132e42a1338074d4c3e4f72faa7`. It already had modified progress.md and untracked WINE artifacts/archives/task states; none were changed by this task.

[Open PR 1](https://github.com/BlockChainLover/flowfence/pull/1) points to `e3b646bbb7a05503457a6b62f9fe09f078eca4eb`. Fetched it read-only and located the R2/R3 evidence missing from the older desktop checkout. Created isolated `/tmp/flowfence_gate_a_worktree_20260918`, branch `codex/aamas2027-gate-a`, at that exact evidence commit. No merge, historical rerun, detector edit, or publication occurred.

Canonical benchmark: [ulab-uiuc/MARBLE](https://github.com/ulab-uiuc/MARBLE), linked by the [official ACL paper](https://aclanthology.org/2025.acl-long.421/). Downloaded source pin: `8d60fa17b5596b44458a52d4296061b9fc13d6f2`. This is an audited failing candidate, NOT a validated reproducible pin. Source checkout: `/tmp/flowfence_gate_a_marble_20260918`. Existing R3 hashes remain in `artifacts/aamas2027/R3_FROZEN_INPUTS.json`; the separate preservation check verifies them, without redefining them. Manifest content hashes in STATIC_AUDIT.json are the source-identity record explicitly requested by Gate A, not a new runtime gate.

## Blocking observation

Python `ast.parse` on [evaluator.py](https://github.com/ulab-uiuc/MARBLE/blob/8d60fa17b5596b44458a52d4296061b9fc13d6f2/marble/evaluator/evaluator.py#L324) fails with `SyntaxError: invalid syntax` at line 324, column 13: an `except json.JSONDecodeError` is nested under an `if` instead of aligned with its `try`. [Engine](https://github.com/ulab-uiuc/MARBLE/blob/8d60fa17b5596b44458a52d4296061b9fc13d6f2/marble/engine/engine.py#L21) imports this module directly. All three target environments share that import. Installing dependencies cannot cure a Python grammar error.

The source can be pinned and downloaded, but reproduction at this pin fails before model execution. Under prompt §26(1), stopped without patching the official evaluator, selecting a replacement commit, or trying model calls. This does NOT prove that every historical MARBLE revision is unusable. A different revision or reviewed syntax-only upstream correction requires a resumed audit, not an invented reproduction claim.

## Environment verdicts

| Environment | Official records / unique IDs | Confirmed usable | Verdict |
|---|---:|---:|---|
| Research Collaboration | 100 / 100 | Not established | NOT_READY |
| Database Error Analysis | 100 / 100 | Not established | NOT_READY |
| Coding Collaboration | 100 / 100 | Not established | NOT_READY |

Each JSONL has IDs 1–100. Research and Database first-record relationship graphs have five agents; Coding has three. This is sampled metadata, not an all-task role audit. All manifests contain blank runtime configuration fields and need the official configuration conversion path evaluated. Database first record supplies initialization SQL and anomaly settings; Coding specifies a workspace directory. No row is called usable merely because it parses as JSON. Inventory `eligible=false` means blocked by common runtime, not rejected for unfavorable outcomes. Requirement of ≥23 usable tasks per environment remains unverified.

## Runtime and license findings

[pyproject.toml](https://github.com/ulab-uiuc/MARBLE/blob/8d60fa17b5596b44458a52d4296061b9fc13d6f2/pyproject.toml) declares Python >=3.9,<3.12, LiteLLM ^1.52.1, Pydantic ^2.9.2, psycopg2-binary, PyMySQL, research retrieval libraries and Poetry. README suggests Python 3.10. No dependencies were installed, database started or benchmark imported. Metadata declares Apache 2.0; actual license file, dataset provenance and redistribution terms remain unaudited. No benchmark task text is redistributed in this report.

[model_prompting.py](https://github.com/ulab-uiuc/MARBLE/blob/8d60fa17b5596b44458a52d4296061b9fc13d6f2/marble/llms/model_prompting.py) uses LiteLLM completion with tools/tool_choice, temperature/top_p/max_tokens; it exposes no seed parameter. A special backend substring selects an alternate base URL. This is not evidence that MiniMax routing is already compatible.

## Evaluator and retry findings

Research `evaluate_task_research` invokes a model judge at temperature 0 and parses integer ratings. Range, aggregation and success threshold remain unverified. Database `evaluate_task_db` only stores `root_cause` and `predicted`; its comment says evaluation occurs separately. The separate original scorer must be located before utility can be reported. Coding engine branches reference `evaluate_code_quality`; its full scoring path remains unaudited. No utility metric was replaced. Planning, communication and KPI evaluation calls exist in the engine; parse_score falls back to 3 on malformed judge output, which must be surfaced separately as evaluator failure while retaining the original output.

[error_handler.py](https://github.com/ulab-uiuc/MARBLE/blob/8d60fa17b5596b44458a52d4296061b9fc13d6f2/marble/llms/error_handler.py) catches all Exceptions and makes up to five total attempts with exponential sleep before returning None. It therefore may retry post-response errors as well as transport errors. `mode=TEST` lowers that outer attempt count to one but is not proof SDK retries are disabled. A future adapter needs structured logical-generation/transport-attempt records and must audit LiteLLM/SDK nested retries. No retry-policy change was made.

## Remaining required audits

- Complete mediation coverage, private/shared state, tools, delegation and all release sites: unverified.
- EXACT_IFC parity: required, not yet demonstrated against MARBLE.
- Frozen recognizer: located `src/defenses/mas_flowfence_r2.py`; unchanged wrapper delegates legacy non-oracle handling, retains block decisions, and uses existing contains_poison_instruction on listed propagation surfaces to release `[artifact quarantined]`. No external A/B construction or compatibility test performed after stop.
- Four fact classes: conditional schema only; semantic fit for all three environments unverified.
- STAR/GRAPH: engine has separate `star_coordinate` and `graph_coordinate` branches selected by coordinate_mode. Availability of two branches does not establish topology-only comparability; prompts, planning, termination, budgets and evaluator paths still require comparison.
- E3: architecture proposal only; reuse audit and dynamic-trajectory validation incomplete.
- E4-A: no model selected; current model identifiers, prices, capability and entitlement checks deferred after hard stop. No unverified candidates presented as currently available.
- Selection: deterministic conditional procedure saved, but no eligible pool or actual split is established.

## Size and integrity

E2 1,080 + E3 324 + E4-A 288 + E4-B 288 = 1,980 NEW formal episodes. Adding E1 108 gives 2,088 study executions. Unique semantic tasks target: 6+60+18=84; robustness subsets add none. No outcome or power calculation was made. The original 39 propagation events must never become 39 independent leaks.

No adapter scaffold, new detector, task-specific enforcement, gold access or scientific model generation was introduced. All uncompleted requested deliverables are explicitly marked partial. NEXT_GATE: Human review of the upstream evaluator failure and approval of a recovery route; resume Gate A before considering Gate B.
