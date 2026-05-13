# ASB Reproduction Checklist

## Upstream Reference

- [x] Official ASB repository cloned into `baselines/asb/upstream/`
- [x] Upstream commit recorded
- [x] First runnable workflow constrained to API-only execution

## Environment

- [x] Remote repo target fixed at `/home/huang/agent-privacy-defense/FlowFence-Lite`
- [x] Remote Python target fixed at `/home/wentian/anaconda3/bin/python`
- [x] Remote venv target fixed at `/home/huang/agent-privacy-defense/FlowFence-Lite/.envs/FlowFence_py313`
- [x] Python 3.13 dependency file added
- [ ] Remote bootstrap completed successfully

## First Runnable Path

- [x] Provider-loading utility added
- [x] Smoke config added
- [x] Remote sync/bootstrap/check scripts added
- [x] Smoke runner writes to `results/<run_name>/`
- [ ] Provider file validated on remote
- [ ] First smoke run completed

## Known Deviations From Upstream

- Upstream defaults to Python 3.11; this repo targets Python 3.13.5.
- Upstream quickstart emphasizes Ollama and local models; this repo's first runnable path is API-only.
- Upstream batch launcher backgrounds jobs with `nohup`; this repo uses a synchronous smoke runner for auditable artifacts.
- Upstream closed-model path assumes GPT-style names; this repo extends the API path to OpenAI-compatible provider models such as Qwen, GLM, Kimi, and MiniMax.
- Upstream package pins were adjusted where needed for Python 3.13 wheel availability, starting with `pandas` and `pydantic`.

## Open Issues

- Dependency compatibility on Python 3.13 still needs to be verified on the remote server.
- Some ASB judge/evaluation logic still assumes OpenAI-style defaults and may require additional adaptation if provider behavior differs.
- The first smoke task is intentionally small and is not full ASB reproduction.
