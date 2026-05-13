# ASB Baseline

Upstream repository: `https://github.com/agiresearch/ASB`  
Pinned commit: `1f561dccf92d55302368fa67679b4ba9d9c8fdc4`

## Purpose

ASB is the first runnable scaffold for this repo because it already includes:

- multi-agent attack workflows,
- tool-using agent execution,
- prompt-injection and memory-attack settings,
- an API-based LLM path via the OpenAI SDK.

## Local Layout

- `baselines/asb/upstream/`: upstream ASB checkout
- `baselines/asb/requirements-py313.txt`: Python 3.13 dependency file for the first runnable path
- `baselines/asb/reproduction_checklist.md`: reproduction notes and deviations
- `baselines/asb/notes.md`: working observations

## Minimal Adaptation Scope

This repo does **not** implement the proposed method here. The ASB adaptation is limited to:

- API-only model routing for the first smoke run,
- Python 3.13 dependency installation,
- remote bootstrap and result logging,
- one small smoke execution path that writes artifacts under `results/`.

## Python 3.13 Adjustments

The upstream README targets Python 3.11 and includes local-model backends such as Ollama and Hugging Face. For this repo's first runnable path:

- the remote interpreter is `/home/wentian/anaconda3/bin/python` (`Python 3.13.5`),
- the remote venv is `/home/huang/agent-privacy-defense/FlowFence-Lite/.envs/FlowFence_py313`,
- the smoke workflow uses API providers only,
- local inference packages are intentionally excluded from the minimal dependency path.

## API Model Adaptation

The first runnable path resolves models from `/home/huang/agent-privacy-defense/FlowFence-Lite/.secrets/providers.env` and maps them into an OpenAI-compatible client path. The first smoke run is designed to work with:

- DashScope-backed aliases: `qwen36`, `qwen35`, `glm5`, `kimi25`
- MiniMax-backed aliases: `minimax25`, `minimax27`

The smoke runner writes all artifacts under `results/<run_name>/` and does not claim full baseline reproduction.
