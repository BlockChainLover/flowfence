# Baselines

This folder tracks which published baselines should be reproduced first, based on the contract in [02_literature_survey.md](/Users/crazy/Desktop/agent-privacy-defense/FlowFence-Lite/research/contract/02_literature_survey.md) and [04_baseline_and_experiment_plan.md](/Users/crazy/Desktop/agent-privacy-defense/FlowFence-Lite/research/contract/04_baseline_and_experiment_plan.md).

Nothing in `src/` should be treated as our proposed method until at least one baseline here is runnable end to end with a saved artifact.

## Baseline Selection Rule

Prioritize baselines that are:

1. strong enough to matter in the paper,
2. directly relevant to the contract’s attack, defense, privacy, or topology questions,
3. backed by official open code,
4. feasible to adapt into a simulated, instrumented multi-agent runtime.

## Strongest Baselines To Reproduce First

| baseline | why it matters | expected setup difficulty | expected dependencies | reproduction priority | current status |
| --- | --- | --- | --- | --- | --- |
| `ASB` | Broadest direct attack/defense benchmark source in the literature set. It covers tool use, memory poisoning, and mixed attacks, so it is the strongest single starting point for attack families and prompt-defense style comparisons. | medium-high | official ASB codebase, one working model backend, task adapters, attack prompt templates, evaluation wrapper, local replayable tools | P1 | `failed exploratory`: smoke scaffold reaches live provider-backed execution, but the saved artifact at `results/smoke_asb_qwen36_dpi/` still fails after entering agent execution and is frozen out of the critical path |
| `AgentDojo` | Strong dynamic benchmark precedent for tool-calling agents under prompt injection. It is the cleanest source for runtime-style evaluation patterns and should help define the first executable benchmark harness. | medium | official AgentDojo codebase, tool sandbox or local substitutes, prompt-injection task adapters, one model backend | P1 | `minimal smoke coverage`: one-task smoke workflow saved at `results/smoke_agentdojo_qwen36_workspace_direct/`; runnable but not reproduced beyond the smoke path |
| `AgentPoison` | Strongest direct memory-poisoning baseline in the contract. It matters because memory is a first-class attack surface in FlowFence-Lite and this is the clearest published attack comparator. | medium | official AgentPoison codebase, retrievable memory layer, poisoning data injection path, metric hooks for memory-linked leakage | P1 | `baseline reproduction in progress`: historical `premethod_v2` slice is saved, and the new critical path is the `fullreact` ReAct-StrategyQA + DPR + `minimax27` baseline under `configs/experiment/agentpoison_fullreact.yaml` |
| `G-Safeguard` | Closest published defense competitor because it is topology-aware and multi-agent focused. It is critical for showing that topology-only protection is not enough. | high | official G-Safeguard codebase, multi-agent graph logging, topology features, anomaly or gating implementation, one stable runtime substrate | P2 | not started |
| `AgentDAM` | Strongest privacy-focused comparator. It matters because the paper needs a credible privacy-vs-utility baseline, not only security baselines. | medium-high | official AgentDAM codebase, privacy policy/task mapping, utility metrics, prompt-level minimization baseline, one compatible agent runtime | P2 | not started |
| `A-MEM` | Strong memory-system baseline for the runtime/memory comparison group. It matters because stronger memory can improve utility and potentially increase privacy risk. | high | official A-MEM codebase, memory backend integration, retrieval interface compatibility, task adapters, logging around memory reads/writes | P3 | not started |

## Status Labels

- `failed exploratory`: useful scaffolding exists, but the path is not stable enough to judge the proposed method.
- `minimal baseline-ready`: fixed task slice, fixed metrics, runnable instructions, saved artifact path, and explicit mismatch notes exist; acceptable for the first method-facing comparison.
- `not started`: no runnable slice yet.

## Recommended Reproduction Order

### Phase 1: benchmark and attack bring-up

1. `AgentPoison`
   Reason: strongest direct memory attack comparator and now the active fullreact baseline-reproduction target.
2. `AgentDojo`
   Reason: useful dynamic benchmark precedent, but no longer on the critical pre-method path.
3. `ASB`
   Reason: valuable long-run comparator, but currently frozen as failed exploratory scaffolding.

### Phase 2: strongest narrow defense comparators

4. `G-Safeguard`
   Reason: closest topology-aware defense baseline.
5. `AgentDAM`
   Reason: strongest privacy minimization comparator.

### Phase 3: memory/runtime comparator

6. `A-MEM`
   Reason: useful and credible, but integration cost is high enough that it should follow the core baseline stack.

## Practical Interpretation For This Repo

- `AgentPoison` remains the primary baseline, but the preferred next artifact is now the `fullreact` ReAct-StrategyQA baseline rather than another method run on the simplified `premethod_v2` slice.
- `results/premethod_summary_agentpoison_strategyqa_premethod_v2.json` remains useful as a historical minimal reference and mismatch anchor.
- `ASB` is preserved as `failed exploratory` scaffolding and should not block fullreact baseline work.
- `AgentDojo` remains a documented smoke artifact, not a required comparator before the first fullreact verdict.
- The first broader defense comparator after the first accepted fullreact defense result should be `G-Safeguard` or `AgentDAM`, with `G-Safeguard` preferred if topology instrumentation is already working.

## Deferred Or Non-Primary References

- `MEXTRA`: important paper evidence for extraction attacks, but no official code located in the contract survey, so it should not be first-line reproduction work.
- `Agent Smith`: strong conceptual motivation for propagation, but multimodal and post-MVP for this text-first repo.
- `Firewalled-Agentic-Networks` and `AiTM`: useful engineering references, not primary headline baselines.

## Required Per-Baseline Contents

For each reproduced baseline, create a subfolder such as `baselines/asb/` or `baselines/g_safeguard/` with:

- `README.md`: source paper/repo, version or commit, run instructions, and what part of the original work is being adapted.
- `reproduction_checklist.md`: setup steps, expected outputs, and mismatch notes.
- `notes.md`: observations separated from interpretations.

## Minimum Reproduction Standard

A baseline counts as reproduced only when all of the following exist:

- source paper or repository reference,
- runnable local instructions,
- fixed task split and metric definitions,
- saved artifact path under `results/`,
- explicit note on mismatch from the original setup.

## Current Gaps Before Method Implementation

- TODO: finish the first remote fullreact `AgentPoison` run and save `official_eval.json` under `results/baseline_agentpoison_fullreact_.../`.
- TODO: manually verify at least 3 adversarial cases for upstream DPR retrieval behavior and poisoned content exposure.
- TODO: keep `ASB` and `AgentDojo` status accurate as non-critical artifacts while fullreact baseline work is in flight.
- TODO: keep the historical simplified retrieval mismatch explicit; it is no longer the preferred next defense target.
