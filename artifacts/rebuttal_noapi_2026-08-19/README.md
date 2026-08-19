# WINE 2026 Rebuttal No-API Experiments

- Local repo root: `/Users/crazy/Desktop/agent-privacy-defense/FlowFence-Lite`
- Remote repo mapping inspected: `/home/huang/agent-privacy-defense/FlowFence-Lite`
- Remote isolated workspace: `/tmp/flowfence_rebuttal_noapi_2026-08-19_workspace`
- Remote experiment output root: `/tmp/flowfence_rebuttal_noapi_2026-08-19_remote`
- Local result root: `/Users/crazy/Desktop/agent-privacy-defense/FlowFence-Lite/artifacts/rebuttal_noapi_2026-08-19`
- Source Git HEAD: `37bbdff617bbe2cb9ba4de5860052ab934c8b337`

## Exact experiment commands

```bash
ssh wentian-server 'cd /tmp/flowfence_rebuttal_noapi_2026-08-19_workspace && env -u MINIMAX_API_KEY -u MINIMAX_BASE_URL -u MINIMAX_GROUP_ID -u MODEL_MINIMAX27 -u MINIMAX_MODEL PYTHONPATH=. /home/huang/agent-privacy-defense/FlowFence-Lite/.envs/FlowFence_py313/bin/python src/runner/sweep_mas.py --config configs/experiment/mas_rebuttal_noapi_component_ablation_pilot.yaml --output-root /tmp/flowfence_rebuttal_noapi_2026-08-19_pilot_a --status-path /tmp/flowfence_rebuttal_noapi_2026-08-19_remote/01_component_ablation/logs/pilot_status.json'
ssh wentian-server 'cd /tmp/flowfence_rebuttal_noapi_2026-08-19_workspace && env -u MINIMAX_API_KEY -u MINIMAX_BASE_URL -u MINIMAX_GROUP_ID -u MODEL_MINIMAX27 -u MINIMAX_MODEL PYTHONPATH=. /home/huang/agent-privacy-defense/FlowFence-Lite/.envs/FlowFence_py313/bin/python src/runner/sweep_mas.py --config configs/experiment/mas_rebuttal_noapi_composite_pilot.yaml --output-root /tmp/flowfence_rebuttal_noapi_2026-08-19_pilot_b --status-path /tmp/flowfence_rebuttal_noapi_2026-08-19_remote/02_composite_baseline/logs/pilot_status.json'
ssh wentian-server 'cd /tmp/flowfence_rebuttal_noapi_2026-08-19_workspace && env -u MINIMAX_API_KEY -u MINIMAX_BASE_URL -u MINIMAX_GROUP_ID -u MODEL_MINIMAX27 -u MINIMAX_MODEL PYTHONPATH=. /home/huang/agent-privacy-defense/FlowFence-Lite/.envs/FlowFence_py313/bin/python src/runner/sweep_mas.py --config configs/experiment/mas_rebuttal_noapi_component_ablation.yaml --output-root /tmp/flowfence_rebuttal_noapi_2026-08-19_component_raw --status-path /tmp/flowfence_rebuttal_noapi_2026-08-19_remote/01_component_ablation/logs/full_status.json'
ssh wentian-server 'cd /tmp/flowfence_rebuttal_noapi_2026-08-19_workspace && env -u MINIMAX_API_KEY -u MINIMAX_BASE_URL -u MINIMAX_GROUP_ID -u MODEL_MINIMAX27 -u MINIMAX_MODEL PYTHONPATH=. /home/huang/agent-privacy-defense/FlowFence-Lite/.envs/FlowFence_py313/bin/python src/runner/sweep_mas.py --config configs/experiment/mas_rebuttal_noapi_composite_baseline.yaml --output-root /tmp/flowfence_rebuttal_noapi_2026-08-19_composite_raw --status-path /tmp/flowfence_rebuttal_noapi_2026-08-19_remote/02_composite_baseline/logs/full_status.json'
ssh wentian-server 'cd /tmp/flowfence_rebuttal_noapi_2026-08-19_workspace && env -u MINIMAX_API_KEY -u MINIMAX_BASE_URL -u MINIMAX_GROUP_ID -u MODEL_MINIMAX27 -u MINIMAX_MODEL PYTHONPATH=. /home/huang/agent-privacy-defense/FlowFence-Lite/.envs/FlowFence_py313/bin/python src/runner/sweep_mas.py --config configs/experiment/mas_rebuttal_noapi_composite_reference_refresh.yaml --output-root /tmp/flowfence_rebuttal_noapi_2026-08-19_reference_raw --status-path /tmp/flowfence_rebuttal_noapi_2026-08-19_remote/02_composite_baseline/logs/reference_status.json'
ssh wentian-server 'cd /tmp/flowfence_rebuttal_noapi_2026-08-19_workspace && PYTHONPATH=. /home/huang/agent-privacy-defense/FlowFence-Lite/.envs/FlowFence_py313/bin/python scripts/summarize_wine_rebuttal_noapi.py --component-runs-root /tmp/flowfence_rebuttal_noapi_2026-08-19_component_raw --composite-runs-root /tmp/flowfence_rebuttal_noapi_2026-08-19_composite_raw --reference-runs-root /tmp/flowfence_rebuttal_noapi_2026-08-19_reference_raw --output-root /tmp/flowfence_rebuttal_noapi_2026-08-19_remote --local-repo-root /Users/crazy/Desktop/agent-privacy-defense/FlowFence-Lite --local-result-root /Users/crazy/Desktop/agent-privacy-defense/FlowFence-Lite/artifacts/rebuttal_noapi_2026-08-19 --remote-repo-root /home/huang/agent-privacy-defense/FlowFence-Lite --remote-workspace /tmp/flowfence_rebuttal_noapi_2026-08-19_workspace --remote-output-root /tmp/flowfence_rebuttal_noapi_2026-08-19_remote --git-head 37bbdff617bbe2cb9ba4de5860052ab934c8b337'
rsync -avz wentian-server:/tmp/flowfence_rebuttal_noapi_2026-08-19_remote/ /Users/crazy/Desktop/agent-privacy-defense/FlowFence-Lite/artifacts/rebuttal_noapi_2026-08-19/
```

## Counts

- Experiment A new: expected 270, completed 270, failed 0, retried 0.
- Experiment A schema refresh: 180 FULL/NO_SEMANTIC rows.
- Experiment B new: expected 90, completed 90, failed 0, retried 0.
- Experiment B schema refresh: 180 Static ACL/Prompt Filter rows; 90 matched FULL rows are reused from Experiment A refresh.

The reference refresh was necessary because the committed canonical package contains high-level summaries but not per-run cascade depth, action counts, or raw traces, and the historical remote raw locator is absent. No canonical artifact or paper file was modified.
