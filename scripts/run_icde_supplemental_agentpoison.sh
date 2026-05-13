#!/usr/bin/env bash
set -euo pipefail

REMOTE_HOST="${REMOTE_HOST:-wentian-server}"
REMOTE_REPO="${REMOTE_REPO:-/home/huang/agent-privacy-defense/FlowFence-Lite}"
REMOTE_VENV="${REMOTE_VENV:-${REMOTE_REPO}/.envs/FlowFence_py313}"
CONFIG_DIR="${1:-configs/experiment/icde_supplemental}"

ssh "${REMOTE_HOST}" "bash -lc \"cd '${REMOTE_REPO}' && python3 scripts/generate_icde_supplemental_configs.py\""

CONFIGS=()
while IFS= read -r config_path; do
  CONFIGS+=("${config_path}")
done < <(find "${CONFIG_DIR}" -maxdepth 1 -type f -name '*.yaml' | sort)
if [ "${#CONFIGS[@]}" -eq 0 ]; then
  echo "no_configs_found:${CONFIG_DIR}" >&2
  exit 1
fi

for config_path in "${CONFIGS[@]}"; do
  base_run_name="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["run_name"])' "${config_path}")"
  for repeat in v1 repeat1 repeat2; do
    if [ "${repeat}" = "v1" ]; then
      run_name="${base_run_name}"
    else
      run_name="${base_run_name%_v1}_${repeat}"
    fi
    echo "running ${config_path} -> ${run_name}"
    ssh "${REMOTE_HOST}" "bash -lc \"cd '${REMOTE_REPO}' && PYTHONPATH='${REMOTE_REPO}' '${REMOTE_VENV}/bin/python' src/runner/run_agentpoison_fullreact.py --config '${config_path}' --run-name '${run_name}'\""
  done
done

ssh "${REMOTE_HOST}" "bash -lc \"cd '${REMOTE_REPO}' && PYTHONPATH='${REMOTE_REPO}' '${REMOTE_VENV}/bin/python' src/runner/summarize_icde_supplemental_agentpoison.py\""
rsync -avz "${REMOTE_HOST}:${REMOTE_REPO}/results/" "./results/"
rsync -avz "${REMOTE_HOST}:${REMOTE_REPO}/artifacts/icde2027_supplemental/" "./artifacts/icde2027_supplemental/"

echo "icde_supplemental_agentpoison_complete"
