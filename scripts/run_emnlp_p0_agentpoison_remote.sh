#!/usr/bin/env bash
set -euo pipefail

REMOTE_HOST="${REMOTE_HOST:-wentian-server}"
REMOTE_REPO="${REMOTE_REPO:-/home/huang/agent-privacy-defense/FlowFence-Lite}"
REMOTE_VENV="${REMOTE_VENV:-${REMOTE_REPO}/.envs/FlowFence_py313}"
MODE="${1:-dryrun}"

if [[ "${MODE}" != "dryrun" && "${MODE}" != "formal" && "${MODE}" != "same_axis" ]]; then
  echo "usage: $0 [dryrun|formal|same_axis]" >&2
  exit 2
fi

mkdir -p artifacts
PYTHONPATH="${PWD}" python3 scripts/generate_emnlp_p0_configs.py >/dev/null
rsync -avz scripts src configs data "${REMOTE_HOST}:${REMOTE_REPO}/" >/dev/null
ssh "${REMOTE_HOST}" "bash -lc \"cd '${REMOTE_REPO}' && PYTHONPATH='${REMOTE_REPO}' '${REMOTE_VENV}/bin/python' scripts/generate_emnlp_p0_configs.py >/dev/null\""

if [[ "${MODE}" == "dryrun" ]]; then
  CONFIG_QUERY=(find configs/experiment/emnlp_p0 -maxdepth 1 -name 'dryrun_agentpoison_*.yaml')
elif [[ "${MODE}" == "formal" ]]; then
  CONFIG_QUERY=(find configs/experiment/emnlp_p0 -maxdepth 1 -name 'agentpoison_*.yaml' ! -name '*minimax27_paraphrase_aware*' ! -name '*minimax27_prompt_quoting*')
else
  CONFIG_QUERY=(find configs/experiment/emnlp_p0 -maxdepth 1 \( -name 'agentpoison_minimax27_paraphrase_aware_keyword_filter_*.yaml' -o -name 'agentpoison_minimax27_prompt_quoting_isolation_*.yaml' \))
fi

CONFIGS=()
while IFS= read -r config; do
  CONFIGS+=("${config}")
done < <("${CONFIG_QUERY[@]}" | sort)

printf '%s\n' "${CONFIGS[@]}" > "artifacts/emnlp2026_p0_${MODE}_configs.txt"

for config in "${CONFIGS[@]}"; do
  echo "running ${config}"
  ssh "${REMOTE_HOST}" "bash -lc \"cd '${REMOTE_REPO}' && PYTHONPATH='${REMOTE_REPO}' '${REMOTE_VENV}/bin/python' src/runner/run_agentpoison_fullreact.py --config '${config}'\""
done

rsync -avz "${REMOTE_HOST}:${REMOTE_REPO}/results/" "./results/"
rsync -avz "${REMOTE_HOST}:${REMOTE_REPO}/artifacts/emnlp2026_p0/" "./artifacts/emnlp2026_p0/" || true

PYTHONPATH="${PWD}" python3 src/runner/summarize_agentpoison_emnlp_p0.py --allow-missing
PYTHONPATH="${PWD}" python3 src/runner/replay_flowfence_overhead.py

echo "emnlp_p0_${MODE}_complete"
