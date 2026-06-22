# WINE 2026 Paper Contract

## Paper Identity

- Paper: `papers/wine2026_flowfence/`
- Topic: runtime mediation for privacy propagation externalities in AI-mediated multi-agent platforms.
- Current phase: paper drafting / rebuttal evidence organization.

## Problem Definition

The paper studies whether platform mediation of information-moving events can reduce unauthorized raw leakage, external leakage, and contaminated propagation across shared multi-agent runtime state while preserving the vendor-facing workflow.

## Threat Model

In scope:

- Summary poisoning, workspace poisoning, and communication hijack in direct and indirect forms.
- Shared-state propagation through chain, star, and blackboard topologies.
- Unauthorized raw disclosure to external or final/vendor-facing channels.
- Label-free held-out paraphrase validation that removes evaluator-only attack annotations from guard input.

Out of scope:

- Non-MiniMax provider generalization for the final-writer evaluation.
- Real browser, desktop, network, OS, or human-workflow compromise.
- Production safety and formal security guarantees.
- Arbitrary paraphrase/adaptive robustness beyond the reserved validation matrices.

## Target Dataset And Split

- Main workflow: synthetic enterprise vendor-update multi-agent task.
- Topologies: `chain_4`, `star_4`, `blackboard_4`.
- Canonical MiniMax final-writer matrix: 3 topologies x 7 attack settings x 4 defenses x 3 seeds = 252 runs.
- Label-free deterministic matrix: 3 topologies x 10 attacks x 6 defenses x 3 seeds = 540 runs.
- Targeted MiniMax label-free matrix: 2 topologies x 3 paraphrase attacks x 4 defenses x 3 seeds = 72 runs.

## Metrics

- Task success: deterministic final-output rule/template check, not an LLM judge.
- Unauthorized raw leakage: exact raw-value matching over mediated runtime events, excluding quarantined or blocked events.
- External leakage: raw leakage reaching external recipient, final output, vendor-send tool, or external message.
- Cascade size: contaminated propagation extent in the runtime event graph.
- Cascade depth: longest contaminated causal path.
- Privilege reach: maximum privilege level touched by contaminated content outside quarantine/block.
- Evaluator-label use: recorded use of evaluator-only attack annotations by the guard.
- Improved/tied matched groups: per topology-attack-seed comparison against a baseline.

## Required Baselines

- No defense.
- Static ACL.
- Prompt filtering.
- FlowFence.
- Label-free FlowFence and no-semantic-pattern ablation for RQ4 validation.
- Adapted AgentPoison MiniMax retrieval-memory result for RQ1 continuity from EMNLP.

## Success Criterion

The paper can claim runtime mediation reduces privacy propagation externalities when FlowFence preserves task success and eliminates unauthorized raw/external leakage in the evaluated FlowFence MiniMax final-writer and label-free slices, while topology analysis shows systematic raw-leakage and cascade differences under no defense.

## Disallowed Shortcuts And Constraints

- MiniMax is the only real provider represented in WINE final-writer experiments.
- Do not claim non-MiniMax, production, browser/desktop, or arbitrary adaptive robustness.
- Do not treat deterministic synthetic-runtime results as real-provider behavior.
- Do not infer missing provider metadata; report missing fields explicitly.
- Do not claim topology changes privilege reach in the RQ2 no-defense aggregate because privilege reach saturates there.

## Canonical Evidence Map

Use `experiments/wine2026_flowfence/README.md` as the rebuttal lookup index for paper tables, metrics, raw/high-level results, safe traces, and caveats.
