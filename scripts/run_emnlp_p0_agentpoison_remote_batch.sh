#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-formal}"
REPO="${REPO:-/home/huang/agent-privacy-defense/FlowFence-Lite}"
VENV="${VENV:-${REPO}/.envs/FlowFence_py313}"

cd "${REPO}"
mkdir -p artifacts/emnlp2026_p0/logs artifacts/emnlp2026_p0/monitor

if [[ "${MODE}" != "formal" && "${MODE}" != "same_axis" ]]; then
  echo "usage: $0 [formal|same_axis]" >&2
  exit 2
fi

PYTHONPATH="${REPO}" "${VENV}/bin/python" scripts/generate_emnlp_p0_configs.py >/dev/null

if [[ "${MODE}" == "formal" ]]; then
  CONFIG_QUERY=(find configs/experiment/emnlp_p0 -maxdepth 1 -name 'agentpoison_*.yaml' ! -name '*minimax27_paraphrase_aware*' ! -name '*minimax27_prompt_quoting*')
else
  CONFIG_QUERY=(find configs/experiment/emnlp_p0 -maxdepth 1 \( -name 'agentpoison_minimax27_paraphrase_aware_keyword_filter_*.yaml' -o -name 'agentpoison_minimax27_prompt_quoting_isolation_*.yaml' \))
fi

CONFIGS=()
while IFS= read -r config; do
  CONFIGS+=("${config}")
done < <("${CONFIG_QUERY[@]}" | sort)

write_status() {
  local current="${1:-}"
  local completed=0
  local failed=0
  local missing=0
  local run_name=""
  local config_path=""
  for config_path in "${CONFIGS[@]}"; do
    run_name="$(PYTHONPATH="${REPO}" "${VENV}/bin/python" - "$config_path" <<'PY'
import sys
from pathlib import Path
import yaml
print(yaml.safe_load(Path(sys.argv[1]).read_text())["run_name"])
PY
)"
    if [[ -f "results/${run_name}/status.txt" ]]; then
      if grep -q '^success' "results/${run_name}/status.txt"; then
        completed=$((completed + 1))
      else
        failed=$((failed + 1))
      fi
    else
      missing=$((missing + 1))
    fi
  done
  PYTHONPATH="${REPO}" "${VENV}/bin/python" - "$MODE" "$current" "${#CONFIGS[@]}" "$completed" "$failed" "$missing" <<'PY'
import json, sys, time
mode, current, expected, completed, failed, missing = sys.argv[1:]
payload = {
    "status": "running" if int(missing) or current else "complete",
    "mode": mode,
    "current_config": current,
    "expected": int(expected),
    "completed": int(completed),
    "failed": int(failed),
    "missing": int(missing),
    "updated_at_epoch": time.time(),
}
path = f"artifacts/emnlp2026_p0/monitor/{mode}_latest_status.json"
open(path, "w", encoding="utf-8").write(json.dumps(payload, indent=2))
print(json.dumps(payload, indent=2))
PY
}

write_status ""
for config in "${CONFIGS[@]}"; do
  run_name="$(PYTHONPATH="${REPO}" "${VENV}/bin/python" - "$config" <<'PY'
import sys
from pathlib import Path
import yaml
print(yaml.safe_load(Path(sys.argv[1]).read_text())["run_name"])
PY
)"
  if [[ -f "results/${run_name}/status.txt" ]] && grep -q '^success' "results/${run_name}/status.txt"; then
    echo "skip existing ${run_name}"
    continue
  fi
  write_status "${config}"
  echo "running ${config}"
  if ! PYTHONPATH="${REPO}" "${VENV}/bin/python" src/runner/run_agentpoison_fullreact.py --config "${config}"; then
    echo "failed ${config}" >&2
  fi
  write_status ""
done

PYTHONPATH="${REPO}" "${VENV}/bin/python" src/runner/summarize_agentpoison_emnlp_p0.py --allow-missing
PYTHONPATH="${REPO}" "${VENV}/bin/python" src/runner/replay_flowfence_overhead.py
write_status ""
cp "artifacts/emnlp2026_p0/monitor/${MODE}_latest_status.json" "artifacts/emnlp2026_p0/monitor/${MODE}_final_status.json"
