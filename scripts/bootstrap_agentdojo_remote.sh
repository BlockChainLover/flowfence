#!/usr/bin/env bash
set -euo pipefail

REMOTE_HOST="${REMOTE_HOST:-wentian-server}"
REMOTE_REPO="${REMOTE_REPO:-/home/huang/agent-privacy-defense/FlowFence-Lite}"
REMOTE_VENV="${REMOTE_VENV:-${REMOTE_REPO}/.envs/FlowFence_py313}"

ssh "${REMOTE_HOST}" "bash -lc '
  set -euo pipefail
  test -x \"${REMOTE_VENV}/bin/python\"
  cd \"${REMOTE_REPO}\"
  \"${REMOTE_VENV}/bin/pip\" install -e ./baselines/agentdojo/upstream
'"

echo "agentdojo_bootstrapped:${REMOTE_VENV}"
