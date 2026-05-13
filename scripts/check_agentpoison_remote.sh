#!/usr/bin/env bash
set -euo pipefail

REMOTE_HOST="${REMOTE_HOST:-wentian-server}"
REMOTE_REPO="${REMOTE_REPO:-/home/huang/agent-privacy-defense/FlowFence-Lite}"
REMOTE_VENV="${REMOTE_VENV:-${REMOTE_REPO}/.envs/FlowFence_py313}"

ssh "${REMOTE_HOST}" "bash -lc '
  set -euo pipefail
  test -d \"${REMOTE_REPO}/baselines/agentpoison/upstream\" && echo agentpoison_checkout_ok
  test -f \"${REMOTE_REPO}/baselines/agentpoison/upstream/ReAct/database/strategyqa_test.json\" && echo react_strategyqa_data_ok
  test -x \"${REMOTE_VENV}/bin/python\" && echo venv_ok
  test -f \"${REMOTE_REPO}/.secrets/providers.env\" && echo providers_ready
  \"${REMOTE_VENV}/bin/python\" -c \"import openai, yaml; print(openai.__version__)\" 
'"
