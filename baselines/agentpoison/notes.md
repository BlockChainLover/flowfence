# AgentPoison Notes

## Initial observations

- The official repo contains three agent branches, and `ReAct-StrategyQA` is the smallest one that still exercises memory or knowledge-base poisoning.
- The imported upstream `ReAct` assets already include the StrategyQA train/test data, the paragraph database, and the prompt file, which makes a narrow smoke slice feasible without extra dataset downloads.
- The upstream StrategyQA scripts mix legacy OpenAI SDK usage, hard-coded save paths, and a `dev` split assumption that does not match the imported files exactly.
- The imported `strategyqa_test.json` omits labels, so the first auditable smoke slice has to use the labeled `train` split if it is going to report even a minimal utility metric.

## Current blockers

- The saved smoke artifact uses a simplified retrieval wrapper instead of the full upstream DPR or REALM path, so it is still only a workflow-validation slice.
- The next meaningful AgentPoison step is to decide whether to bring up the official retriever path first or expand to a second smoke question while keeping the mismatch accounting explicit.

## Fullreact implementation notes

- The fullreact baseline should keep the official `ReAct-StrategyQA` loop and upstream `local_wikienv.WikiEnv` instead of extending the simplified smoke runner.
- The imported upstream wrapper expects `ReAct/data/strategyqa/strategyqa_dev.json`, so the repository stages a labeled subset from the upstream `train` file into a dev-compatible path for evaluation and records that mismatch explicitly.
- Official eval is preserved by running `ReAct/eval.py` on the produced benign and adversarial jsonl outputs, then mapping only the compatible parts into FlowFence-facing metrics.
