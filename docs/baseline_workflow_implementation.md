# Baseline Workflow Implementation

This repo's first runnable baseline path uses ASB as the scaffold and stops at a small smoke run. It does not implement the proposed method.

## Canonical Paths

- local repo: `/Users/crazy/Desktop/agent-privacy-defense/FlowFence-Lite`
- remote repo: `/home/huang/agent-privacy-defense/FlowFence-Lite`
- remote bootstrap interpreter: `/home/wentian/anaconda3/bin/python`
- remote venv: `/home/huang/agent-privacy-defense/FlowFence-Lite/.envs/FlowFence_py313`
- provider file: `/home/huang/agent-privacy-defense/FlowFence-Lite/.secrets/providers.env`

## Workflow Files

- `scripts/sync_remote.sh`
- `scripts/bootstrap_remote.sh`
- `scripts/check_remote_env.sh`
- `scripts/run_asb_smoke.sh`
- `src/common/provider_loader.py`
- `src/runner/run_asb_smoke.py`
- `configs/experiment/asb_smoke.yaml`
- `configs/logger/default.yaml`
- `configs/model/api_default.env.example`

## Smoke Run Contract

Each smoke run must create `results/<run_name>/` with:

- `manifest.json`
- `resolved_config.yaml`
- `stdout.log`
- `stderr.log`
- `status.txt`
- `metrics.json`
- `asb_results.csv`

If execution fails, `status.txt` must still exist and explain the failure.

## Provider Model Profiles

The smoke runner supports these provider profiles:

- `qwen36`
- `qwen35`
- `glm5`
- `kimi25`
- `minimax25`
- `minimax27`

All profiles are resolved from `.secrets/providers.env`. No local model serving is used.
