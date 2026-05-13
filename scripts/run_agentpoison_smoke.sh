#!/usr/bin/env bash
set -euo pipefail

REMOTE_HOST="${REMOTE_HOST:-wentian-server}"
REMOTE_REPO="${REMOTE_REPO:-/home/huang/agent-privacy-defense/FlowFence-Lite}"
REMOTE_VENV="${REMOTE_VENV:-${REMOTE_REPO}/.envs/FlowFence_py313}"
CONFIG_PATH="${1:-configs/experiment/agentpoison_premethod.yaml}"
RUN_NAME="${2:-}"

RUN_ARG=""
if [ -n "${RUN_NAME}" ]; then
  RUN_ARG=" --run-name '${RUN_NAME}'"
fi

ssh "${REMOTE_HOST}" "bash -lc \"cd '${REMOTE_REPO}' && PYTHONPATH='${REMOTE_REPO}' '${REMOTE_VENV}/bin/python' src/runner/run_agentpoison_smoke.py --config '${CONFIG_PATH}'${RUN_ARG}\""
rsync -avz "${REMOTE_HOST}:${REMOTE_REPO}/results/" "./results/"

echo "agentpoison_premethod_complete"
