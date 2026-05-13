# AgentDojo Reproduction Checklist

## Upstream Reference

- [x] Official AgentDojo source imported into `baselines/agentdojo/upstream/`
- [x] Imported package version recorded (`0.1.35`)
- [x] First runnable workflow constrained to API-only execution

## Environment

- [x] Remote repo target fixed at `/home/huang/agent-privacy-defense/FlowFence-Lite`
- [x] Remote Python target fixed at `/home/wentian/anaconda3/bin/python`
- [x] Remote venv target fixed at `/home/huang/agent-privacy-defense/FlowFence-Lite/.envs/FlowFence_py313`
- [x] AgentDojo editable install completed successfully in the remote venv

## First Runnable Path

- [x] Smoke config added
- [x] Smoke runner writes to `results/<run_name>/`
- [x] Remote bootstrap/check/run scripts added
- [x] Provider file validated on remote
- [x] First smoke run completed

## Known Deviations From Upstream

- The imported source is a local snapshot of the official repo, not a git submodule or fresh clone.
- Upstream examples assume direct model names such as OpenAI-hosted GPT variants; this repo resolves the actual API-backed model name from `.secrets/providers.env`.
- Upstream OpenAI message conversion used the `developer` role; this repo patches the smoke path to emit `system` so OpenAI-compatible providers such as DashScope accept the request.
- The first runnable path uses one small task pair and writes FlowFence-Lite-style run artifacts under `results/` instead of using AgentDojo's default `runs/` directory as the top-level artifact.
- The first smoke path uses the existing FlowFence-Lite remote venv and remote repo conventions rather than AgentDojo's standalone project environment.

## Open Issues

- Python 3.13 compatibility for the full AgentDojo dependency set still needs to be validated on the remote server.
- The smoke artifact verifies only one `workspace` task/injection pair with the `direct` attack and no defense.
- This smoke path is intentionally narrow and is not full AgentDojo reproduction.
