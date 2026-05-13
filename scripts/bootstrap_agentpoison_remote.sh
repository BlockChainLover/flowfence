#!/usr/bin/env bash
set -euo pipefail

REMOTE_HOST="${REMOTE_HOST:-wentian-server}"
REMOTE_REPO="${REMOTE_REPO:-/home/huang/agent-privacy-defense/FlowFence-Lite}"
REMOTE_VENV="${REMOTE_VENV:-${REMOTE_REPO}/.envs/FlowFence_py313}"

ssh "${REMOTE_HOST}" "bash -lc '
  set -euo pipefail
  test -x \"${REMOTE_VENV}/bin/python\"
  cd \"${REMOTE_REPO}\"
  \"${REMOTE_VENV}/bin/pip\" install -r requirements-workflow.txt
  \"${REMOTE_VENV}/bin/pip\" install -r requirements-agentpoison-fullreact.txt
  \"${REMOTE_VENV}/bin/pip\" install --force-reinstall --index-url https://download.pytorch.org/whl/cu128 torch==2.10.0
  \"${REMOTE_VENV}/bin/python\" - <<\"PY\"
from pathlib import Path

from modelscope.hub.file_download import model_file_download

cache_root = \"/home/huang/agent-privacy-defense/FlowFence-Lite/.modelscope-cache\"
local_dir = Path(cache_root) / \"facebook\" / \"dpr-ctx_encoder-single-nq-base\"
local_dir.mkdir(parents=True, exist_ok=True)
for filename in [
    \"config.json\",
    \"configuration.json\",
    \"pytorch_model.bin\",
    \"tokenizer.json\",
    \"tokenizer_config.json\",
    \"vocab.txt\",
]:
    model_file_download(
        \"facebook/dpr-ctx_encoder-single-nq-base\",
        file_path=filename,
        cache_dir=cache_root,
        local_dir=str(local_dir),
    )
PY
'"

echo "agentpoison_bootstrapped:${REMOTE_VENV}"
