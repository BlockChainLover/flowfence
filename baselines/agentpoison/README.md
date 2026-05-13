# AgentPoison

## Upstream reference

- paper: [AgentPoison: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases](https://openreview.net/forum?id=Y841BRW9rY)
- official repo: [AI-secure/AgentPoison](https://github.com/AI-secure/AgentPoison)
- imported upstream commit: `f859b503318b450d158662f78d761e2918a05259`

## Selected minimum runnable slice

- upstream branch used for the first smoke path: `ReAct-StrategyQA`
- why this slice:
  it is the lightest path in the official repo that still exercises the core memory/knowledge-base poisoning idea without the heavier autonomous driving or EHR dependencies
- fixed pre-method target:
  the manifest `data/tasks/agentpoison_strategyqa_premethod_v2.json`, which locks a ten-question `StrategyQA` subset, two execution modes per question (`benign` and triggered `adv`), provider-backed `qwen36`, and a canonical FlowFence-Lite run artifact under `results/`
- fullreact target:
  the manifest `data/tasks/agentpoison_strategyqa_fullreact_v1.json`, which stages a labeled 25-question `StrategyQA` subset through the official `ReAct-StrategyQA` agent loop, upstream `local_wikienv.WikiEnv` DPR retrieval path, provider-backed `minimax27`, and official `ReAct/eval.py` outputs under `results/`

## What this repo is adapting

- source assets reused directly from upstream:
  `ReAct/database/strategyqa_train.json`
  `ReAct/database/strategyqa_test.json`
  `ReAct/database/strategyqa_train_paragraphs.json`
  `ReAct/prompts/prompts.json`
- FlowFence-Lite wrapper path:
  `src/runner/run_agentpoison_smoke.py`
- fullreact wrapper path:
  `src/runner/run_agentpoison_fullreact.py`

## Why this is only a smoke path

- it does not run trigger optimization
- it does not run the full upstream DPR or REALM retrieval stack
- it does not claim full baseline reproduction
- it is intentionally an adapted narrow baseline slice that is baseline-ready for the first proposed-defense comparison, not a paper claim of full official reproduction
- the method-start reference is a 3-rerun aggregate summary, not a single run

## Fullreact baseline scope

- reuses the official `ReAct-StrategyQA` loop shape, prompt template, and `local_wikienv.WikiEnv` retrieval semantics
- fixes the baseline to `dpr` retrieval, `ap` attack mode, and provider profile `minimax27`
- stages a labeled subset from the upstream `train` file into a dev-compatible wrapper path because the imported `test` file lacks labels
- preserves official eval metrics (`ACC`, `ASR-r`, `ASR-a`, `ASR-t`) and adds FlowFence-facing normalized rates in `metrics.json`
- still does not claim the full paper reproduction across all agent branches, trigger-optimization steps, or alternate retrievers

## Local/remote workflow

- sync:
  `./scripts/sync_remote.sh`
- remote bootstrap:
  `bash scripts/bootstrap_agentpoison_remote.sh`
- remote check:
  `bash scripts/check_agentpoison_remote.sh`
- fixed pre-method run:
  `bash scripts/run_agentpoison_smoke.sh`
- fullreact remote check:
  `bash scripts/check_agentpoison_fullreact_remote.sh`
- fullreact baseline run:
  `bash scripts/run_agentpoison_fullreact.sh`
