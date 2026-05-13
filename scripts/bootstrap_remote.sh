#!/usr/bin/env bash
set -euo pipefail

REMOTE_HOST="${REMOTE_HOST:-wentian-server}"
REMOTE_REPO="${REMOTE_REPO:-/home/huang/agent-privacy-defense/FlowFence-Lite}"
REMOTE_PYTHON="${REMOTE_PYTHON:-/home/wentian/anaconda3/bin/python}"
REMOTE_VENV="${REMOTE_VENV:-${REMOTE_REPO}/.envs/FlowFence_py313}"

ssh "${REMOTE_HOST}" "bash -lc '
  set -euo pipefail
  mkdir -p \"${REMOTE_REPO}\" \"${REMOTE_REPO}/.envs\" \"${REMOTE_REPO}/.secrets\" \"${REMOTE_REPO}/results\"
  if [ ! -x \"${REMOTE_VENV}/bin/python\" ]; then
    \"${REMOTE_PYTHON}\" -m venv \"${REMOTE_VENV}\"
  fi
  \"${REMOTE_VENV}/bin/python\" -m pip install --upgrade pip setuptools wheel
  cd \"${REMOTE_REPO}\"
  \"${REMOTE_VENV}/bin/pip\" install -r requirements-workflow.txt
  \"${REMOTE_VENV}/bin/pip\" install --retries 1 --timeout 30 openai pandas numpy tqdm pydantic protobuf python-dotenv PyYAML click Pympler
'"

echo "bootstrapped:${REMOTE_VENV}"
