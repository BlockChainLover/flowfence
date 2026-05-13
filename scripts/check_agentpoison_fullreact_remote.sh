#!/usr/bin/env bash
set -euo pipefail

REMOTE_HOST="${REMOTE_HOST:-wentian-server}"
REMOTE_REPO="${REMOTE_REPO:-/home/huang/agent-privacy-defense/FlowFence-Lite}"
REMOTE_VENV="${REMOTE_VENV:-${REMOTE_REPO}/.envs/FlowFence_py313}"

ssh "${REMOTE_HOST}" "bash -lc '
  set -euo pipefail
  test -d \"${REMOTE_REPO}/baselines/agentpoison/upstream/ReAct\" && echo react_checkout_ok
  test -f \"${REMOTE_REPO}/baselines/agentpoison/upstream/ReAct/database/strategyqa_train.json\" && echo strategyqa_train_ok
  test -f \"${REMOTE_REPO}/data/tasks/agentpoison_strategyqa_fullreact_v1.json\" && echo fullreact_manifest_ok
  test -f \"${REMOTE_REPO}/.modelscope-cache/facebook/dpr-ctx_encoder-single-nq-base/pytorch_model.bin\" && echo dpr_cache_ok
  test -x \"${REMOTE_VENV}/bin/python\" && echo venv_ok
  test -f \"${REMOTE_REPO}/.secrets/providers.env\" && echo providers_ready
  AGENTPOISON_DPR_CTX_ENCODER_PATH=\"${REMOTE_REPO}/.modelscope-cache/facebook/dpr-ctx_encoder-single-nq-base\" \
  \"${REMOTE_VENV}/bin/python\" -c \"import openai, yaml, torch, transformers, gym, pandas, bs4, jsonlines, requests, modelscope; from transformers import AutoTokenizer, DPRContextEncoder; model_dir=\\\"${REMOTE_REPO}/.modelscope-cache/facebook/dpr-ctx_encoder-single-nq-base\\\"; tok=AutoTokenizer.from_pretrained(model_dir); model=DPRContextEncoder.from_pretrained(model_dir); print(openai.__version__, tok.__class__.__name__, model.__class__.__name__)\" 
'"
