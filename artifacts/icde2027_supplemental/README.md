# ICDE 2027 Supplemental Experiment Artifacts

This directory is reserved for paper-facing supplemental outputs generated from the fixed adapted AgentPoison StrategyQA full-ReAct MiniMax axis.

## Reduced Reproduction Command

Run the configured supplemental matrix:

```bash
bash scripts/run_icde_supplemental_agentpoison.sh
```

The script regenerates JSON-compatible YAML configs under `configs/experiment/icde_supplemental/`, runs each config for `v1`, `repeat1`, and `repeat2`, then writes summaries under `artifacts/icde2027_supplemental/results/`.

## Experiment Groups

- `paraphrase_family`: six poisoned-instruction surface forms across no defense, non-oracle static keyword filtering, and FlowFence-Lite.
- `false_positive_clean_memory`: benign instruction-like retrieved records across no defense and FlowFence-Lite.
- `pressure_topk_candidate_pool`: top-k candidate-pool sensitivity for `knn=1,3,5` across no defense, static keyword filtering, and FlowFence-Lite.
- `audit_cases`: compact case exports showing whether unsafe retrieved content crossed the retrieval-exposure boundary.

## Safety Notes

- Provider profile is fixed to `minimax27`.
- These runs are adapted AgentPoison comparator runs, not full official AgentPoison reproduction.
- No API keys or personal absolute paths should be written into this artifact directory.
