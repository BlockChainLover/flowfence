#!/usr/bin/env bash
set -euo pipefail

REMOTE_HOST="${REMOTE_HOST:-wentian-server}"
REMOTE_REPO="${REMOTE_REPO:-/home/huang/agent-privacy-defense/FlowFence-Lite}"
REMOTE_VENV="${REMOTE_VENV:-${REMOTE_REPO}/.envs/FlowFence_py313}"

ssh "${REMOTE_HOST}" "bash -lc '
  set -euo pipefail
  test -d \"${REMOTE_REPO}\" && echo remote_repo_ok
  test -d \"${REMOTE_REPO}/baselines/asb/upstream\" && echo asb_checkout_ok
  test -x \"${REMOTE_VENV}/bin/python\" && echo venv_ok
  test -f \"${REMOTE_REPO}/.secrets/providers.env\" && echo providers_ready
  test -w \"${REMOTE_REPO}/results\" && echo results_writable
  \"${REMOTE_VENV}/bin/python\" -V
'"
