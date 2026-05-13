# EMNLP Next P0 Execution Plan

Date: 2026-05-12

Phase: paper drafting

## Scope Confirmed By User

- LLM judge API calls are allowed for P0.
- LLM judge dry-run is capped at 50 retrieval events per provider.
- Judge providers: `kimi25` and `minimax27`.
- Near-official AgentPoison sanity check is acceptable; full official reproduction is not required for this batch.
- Adaptive poison templates do not require manual review before running.
- Keep the current fixed 25-question subset.
- Adaptive pilot uses only `kimi25`.
- Do not add a CI appendix or automatic LaTeX table generator in this batch.

## P0 Execution Order

### P0.1 Logging and Script Preparation

Objective: create minimal reusable scripts and artifacts without changing paper text or core runner behavior.

Actions:

- Add fixed-trace inspector-swap replay.
- Add benign false-quarantine offline replay.
- Keep outputs as CSV/JSON artifacts.
- Avoid automatic LaTeX table generation.

Artifacts:

- `src/runner/replay_inspector_swap.py`
- `src/runner/replay_benign_false_quarantine.py`
- `artifacts/emnlp2026_p1/inspector_swap/`
- `artifacts/emnlp2026_p1/benign_false_quarantine/`

### P0.2 Detector-Swap Fixed-Trace Replay

Objective: test whether the same FlowFence retrieval-to-exposure boundary can be driven by different inspectors on saved retrieval events.

Inputs:

- `artifacts/emnlp2026_p0/overhead_replay/fixed_trace_events.jsonl`
- 466 saved retrieval events, including 22 poisoned events.

Inspectors:

- Rule inspector: current FlowFence rule policy.
- Paraphrase-aware heuristic inspector: broader non-oracle patterns.
- LLM judge inspector: `kimi25` and `minimax27`, capped at 50 events each.

Metrics:

- flagged rate
- quarantine rate
- false quarantine rate on non-poisoned events
- poisoned-event recall
- poisoned exposed rate
- local microseconds per event
- LLM token usage, when provider usage is returned

Status:

- Local rule/heuristic replay completed.
- LLM judge dry-run is pending remote/API availability.

### P0.3 Benign False-Quarantine Expansion

Objective: test whether inspectors over-block benign retrieval records.

Benign families:

- benign instructional memory
- useful factual memory
- irrelevant harmless memory

Scale:

- 30 records per family for the first offline pass.
- 90 records total.

Metrics:

- false quarantine rate
- false rewrite rate
- intervention rate
- local microseconds per record
- representative false positives from the event CSV

Status:

- Local offline replay completed for rule and heuristic inspectors.

### P0.4 Adaptive Poisoning Pilot

Objective: evaluate harder poisoned memory that avoids obvious trigger words and produces a credible failure analysis.

Provider:

- `kimi25` only.

Question subset:

- current fixed 25-question subset.

Families for first pilot:

- factual-looking misinformation
- soft preference manipulation
- multilingual or mixed-language poison

Conditions:

- No defense
- Static keyword filter
- FlowFence rule inspector

Metrics:

- raw poisoned retrieval
- exposed poisoned retrieval
- attack manifestation
- clean utility
- attacked utility
- detector miss cases
- examples of bypassed and quarantined records

Launch condition:

- Start only after P0.2 LLM judge dry-run has either completed or been explicitly deferred.

### P0.5 Near-Official AgentPoison Sanity Check

Objective: calibrate the current adapted trigger-query setting against a less-adapted AgentPoison setting.

Settings:

- current adapted trigger-query setting
- near-official / less-adapted full-context setting

Conditions:

- No defense
- FlowFence quarantine + action canonicalization

Metrics:

- raw poisoned retrieval
- exposed poisoned retrieval
- attack manifestation
- clean utility
- attacked utility
- intervention rate
- raw-poison-positive subset behavior if raw retrieval pressure is low

Launch condition:

- Run after adaptive pilot setup, because known risk is low raw poison pressure under near-official context.

## Current Execution Notes

- Local Python 3.8 cannot import `src.common.provider_loader` because that file uses newer type syntax; use Python 3.10 for local P0 scripts.
- Local LLM judge failed because the `openai` package and provider secrets are not available locally.
- Remote host `wentian-server` was reachable for a short env check, but subsequent `rsync`, `scp`, and `ssh` attempts timed out. Remote LLM judge dry-run should be retried after SSH stabilizes.

