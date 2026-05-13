#!/usr/bin/env bash
set -euo pipefail

REMOTE_HOST="${REMOTE_HOST:-wentian-server}"
REMOTE_REPO="${REMOTE_REPO:-/home/huang/agent-privacy-defense/FlowFence-Lite}"

ssh "${REMOTE_HOST}" "mkdir -p '${REMOTE_REPO}'"

rsync -avz \
  --exclude '.git/' \
  --exclude '.envs/' \
  --exclude '.secrets/' \
  --exclude '.DS_Store' \
  --exclude '__pycache__/' \
  --exclude '.pytest_cache/' \
  --exclude 'baselines/asb/upstream/.git/' \
  --exclude 'baselines/agentdojo/upstream/runs/' \
  ./ "${REMOTE_HOST}:${REMOTE_REPO}/"

echo "synced:${REMOTE_REPO}"
