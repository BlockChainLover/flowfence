#!/usr/bin/env bash
set -uo pipefail

REMOTE_REPO="${REMOTE_REPO:-/home/huang/agent-privacy-defense/FlowFence-Lite}"
REMOTE_VENV="${REMOTE_VENV:-${REMOTE_REPO}/.envs/FlowFence_py313}"
CONFIG_DIR="${1:-configs/experiment/icde_supplemental}"
LOG_DIR="${REMOTE_REPO}/artifacts/icde2027_supplemental/logs"
mkdir -p "${LOG_DIR}"

cd "${REMOTE_REPO}" || exit 1
python3 scripts/generate_icde_supplemental_configs.py

run_one() {
  local config_path="$1"
  local run_name="$2"
  local status_path="results/${run_name}/status.txt"
  if [ -f "${status_path}" ] && grep -q '^success$' "${status_path}"; then
    echo "skip_success ${run_name}"
    return 0
  fi
  echo "start ${config_path} ${run_name}"
  PYTHONPATH="${REMOTE_REPO}" "${REMOTE_VENV}/bin/python" \
    src/runner/run_agentpoison_fullreact.py \
    --config "${config_path}" \
    --run-name "${run_name}"
  local code="$?"
  echo "finish ${run_name} code=${code}"
  return 0
}

while IFS= read -r config_path; do
  base_run_name="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["run_name"])' "${config_path}")"
  for repeat in v1 repeat1 repeat2; do
    if [ "${repeat}" = "v1" ]; then
      run_name="${base_run_name}"
    else
      run_name="${base_run_name%_v1}_${repeat}"
    fi
    run_one "${config_path}" "${run_name}" 2>&1 | tee -a "${LOG_DIR}/batch_runs.log"
  done
done < <(find "${CONFIG_DIR}" -maxdepth 1 -type f -name '*.yaml' | sort)

PYTHONPATH="${REMOTE_REPO}" "${REMOTE_VENV}/bin/python" \
  src/runner/summarize_icde_supplemental_agentpoison.py \
  2>&1 | tee -a "${LOG_DIR}/batch_summary.log"

python3 scripts/export_audit_cases.py \
  2>&1 | tee -a "${LOG_DIR}/audit_export.log"

echo "remote_icde_supplemental_complete"
