# AgentPoison Reproduction Checklist

## Upstream Reference

- [x] Official AgentPoison repository cloned into `baselines/agentpoison/upstream/`
- [x] Upstream commit recorded
- [x] First runnable workflow constrained to the `ReAct-StrategyQA` branch

## Environment

- [x] Remote repo target fixed at `/home/huang/agent-privacy-defense/FlowFence-Lite`
- [x] Remote Python target fixed at `/home/wentian/anaconda3/bin/python`
- [x] Remote venv target fixed at `/home/huang/agent-privacy-defense/FlowFence-Lite/.envs/FlowFence_py313`
- [x] API-only LLM path fixed through `.secrets/providers.env`
- [x] AgentPoison remote bootstrap completed successfully

## First Runnable Path

- [x] Fixed pre-method config added at `configs/experiment/agentpoison_premethod.yaml`
- [x] Fixed task manifest added at `data/tasks/agentpoison_strategyqa_premethod_v2.json`
- [x] Runner writes canonical run artifacts to `results/<run_name>/`
- [x] Remote bootstrap/check/run scripts added
- [x] Provider file validated on remote
- [x] First smoke run completed

## Fullreact Path

- [x] Fullreact task manifest added at `data/tasks/agentpoison_strategyqa_fullreact_v1.json`
- [x] Fullreact config added at `configs/experiment/agentpoison_fullreact.yaml`
- [x] Fullreact runner added at `src/runner/run_agentpoison_fullreact.py`
- [x] Fullreact remote check/run scripts added
- [x] Fullreact path fixed to `ReAct-StrategyQA` + `dpr` + `ap` + provider profile `minimax27`
- [ ] Remote bootstrap updated and validated for fullreact dependencies
- [ ] First fullreact benign/adv run completed
- [ ] Official eval artifact saved under `results/baseline_agentpoison_fullreact_.../official_eval.json`

## Known Deviations From Upstream

- Upstream targets Python 3.9 with a much larger environment; this repo reuses the shared Python 3.13 remote venv.
- Upstream StrategyQA scripts assume legacy OpenAI SDK calls and a standalone project layout; this repo wraps the minimum smoke path in a FlowFence-Lite runner.
- Upstream ReAct path expects a `dev` split name, but the imported data files expose `train` and `test`; this repo uses the labeled `train` split for the first smoke artifact because the imported `test` file does not include answers.
- The pre-method slice reuses the official StrategyQA data and poisoning format but simplifies retrieval for workflow validation and first defense comparison instead of claiming the full DPR-based attack pipeline.

## Open Issues

- Full reproduction still needs the official retrieval stack and its dependency burden audited on the remote server.
- The enlarged fixed subset now has 3 successful reruns and a rerun aggregate summary artifact, but the repo still needs to decide whether that aggregate is sufficient to start method work.
- The comparator is minimal baseline-ready, not full reproduction, so every paper-facing note must preserve the mismatch statement.
- The fullreact baseline now targets official `WikiEnv` retrieval semantics, but remote dependency and cache setup still need one successful end-to-end run before it can replace the simplified slice as the preferred defense target.
