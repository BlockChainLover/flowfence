#!/usr/bin/env bash
set -euo pipefail

REMOTE_HOST="${REMOTE_HOST:-wentian-server}"
REMOTE_REPO="${REMOTE_REPO:-/home/huang/agent-privacy-defense/FlowFence-Lite}"
REMOTE_VENV="${REMOTE_VENV:-${REMOTE_REPO}/.envs/FlowFence_py313}"
CONFIG_PATH="${1:-configs/experiment/agentpoison_fullreact.yaml}"
RUN_NAME="${2:-diagnostic_agentpoison_fullreact_dpr_retrieval_v1}"

ssh "${REMOTE_HOST}" "bash -lc \"cd '${REMOTE_REPO}' && PYTHONPATH='${REMOTE_REPO}' '${REMOTE_VENV}/bin/python' src/runner/diagnose_agentpoison_retrieval.py --config '${CONFIG_PATH}' --run-name '${RUN_NAME}'\""
rsync -avz "${REMOTE_HOST}:${REMOTE_REPO}/results/" "./results/"

echo "agentpoison_retrieval_diagnostic_complete"
