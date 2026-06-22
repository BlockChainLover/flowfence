# EMNLP 2026 Paper Contract

## Paper Identity

- Paper: `papers/emnlp2026_flowfence/`
- Topic: retrieval-memory poisoning containment for LLM agents.
- Current phase: paper drafting / rebuttal evidence organization.

## Problem Definition

The paper studies whether a runtime boundary between retrieval and model-visible context can prevent poisoned memory records from becoming exposed prompt context or downstream unsafe actions while preserving useful ReAct task execution.

## Threat Model

In scope:

- Poisoned retrieved memory or knowledge-base records in an AgentPoison-derived StrategyQA full-ReAct setting.
- Poisoned instructions that may be retrieved internally and serialized into model-visible observations.
- Same-axis paraphrase, held-out poisoned-instruction, and adaptive-pilot stress variants.

Out of scope:

- Official AgentPoison reproduction claims.
- Multi-agent topology propagation claims.
- OS, network, browser, desktop, credential, or raw provider-log compromise.
- Production safety or formal security guarantees.

## Target Dataset And Split

- Dataset axis: adapted `AgentPoison` `ReAct-StrategyQA` full-ReAct task subset.
- Main paper groups use 25-question runs where recorded in `artifacts/emnlp2026_p0/results/emnlp_p0_cross_provider_runs.csv`.
- Older 10-question pre-method `qwen36` artifacts are historical and are not canonical EMNLP evidence.

## Metrics

- Raw poisoned retrieval: poison present before the retrieval-to-exposure boundary.
- Exposed poisoned retrieval: poison remains in model-visible context after boundary processing.
- Attack manifestation: downstream attack behavior in trajectory or final answer.
- Clean utility and attacked utility: exact-match utility rates.
- Interventions per case: defense intervention events divided by evaluated cases.
- False quarantine / false intervention: clean-event or clean-record intervention rate.
- Replay overhead: local microseconds per saved event or serialized-context token proxy unless explicitly provider-measured.

## Required Baselines

- No defense.
- Static keyword filtering for known-trigger same-axis comparison.
- Rewrite-only and quarantine-only mechanism variants.
- Prompt quoting and paraphrase-aware keyword comparators for same-axis boundary comparison.

## Success Criterion

The paper can claim retrieval-memory containment when raw poisoned retrieval remains non-zero while exposed poisoned retrieval and attack manifestation are reduced to zero or near-zero in the saved FlowFence runs, with caveats for utility and comparator scope.

## Disallowed Shortcuts And Constraints

- Do not describe the adapted comparator as an official AgentPoison reproduction.
- Do not describe smoke tests or dry runs as reproduced baselines.
- Do not silently change split, metric definitions, or preprocessing after comparison.
- Do not introduce new non-MiniMax experiments in the current phase unless the human explicitly changes the provider constraint.
- Do not claim detector-independent performance from detector-swap replay.

## Canonical Evidence Map

Use `experiments/emnlp2026_flowfence/README.md` as the rebuttal lookup index for paper tables, metrics, raw results, and caveats.
