#!/usr/bin/env bash
set -uo pipefail

REMOTE_REPO="${REMOTE_REPO:-/home/huang/agent-privacy-defense/FlowFence-Lite}"
REMOTE_VENV="${REMOTE_VENV:-${REMOTE_REPO}/.envs/FlowFence_py313}"
EXPECTED_RUNS="${EXPECTED_RUNS:-87}"
POLL_SECONDS="${POLL_SECONDS:-300}"
LOG_DIR="${REMOTE_REPO}/artifacts/icde2027_supplemental/logs"
MONITOR_DIR="${REMOTE_REPO}/artifacts/icde2027_supplemental/monitor"
LOG_FILE="${LOG_DIR}/remote_monitor.log"
STATUS_FILE="${MONITOR_DIR}/latest_status.json"
FINAL_FILE="${MONITOR_DIR}/final_status.json"

mkdir -p "${LOG_DIR}" "${MONITOR_DIR}"
cd "${REMOTE_REPO}" || exit 1

log() {
  printf '[%s] %s\n' "$(date '+%F %T')" "$*" | tee -a "${LOG_FILE}"
}

write_status() {
  EXPECTED_RUNS="${EXPECTED_RUNS}" python3 - <<'PY' > "${STATUS_FILE}"
import collections
import json
import os
import pathlib

expected = int(os.environ["EXPECTED_RUNS"])
dirs = list(pathlib.Path("results").glob("icde_*"))
rows = []
for run_dir in dirs:
    status_path = run_dir / "status.txt"
    status = status_path.read_text(encoding="utf-8").strip() if status_path.exists() else "missing"
    rows.append((status, run_dir.name))
counts = collections.Counter(status for status, _ in rows)
failed = [{"status": status, "run": name} for status, name in sorted(rows) if status != "success"]
print(json.dumps({
    "expected": expected,
    "dirs": len(dirs),
    "success": counts.get("success", 0),
    "counts": dict(counts),
    "failed_or_missing": failed[:100],
}, indent=2))
PY
}

json_field() {
  python3 -c 'import json,sys; print(json.load(open(sys.argv[1], encoding="utf-8"))[sys.argv[2]])' "${STATUS_FILE}" "$1"
}

batch_running() {
  pgrep -af run_icde_supplemental_agentpoison_remote.sh >/dev/null && echo yes || echo no
}

runner_running() {
  pgrep -af run_agentpoison_fullreact.py >/dev/null && echo yes || echo no
}

restart_batch() {
  log "batch inactive while incomplete; starting resumable runner"
  setsid bash scripts/run_icde_supplemental_agentpoison_remote.sh \
    > "${LOG_DIR}/nohup_remote_monitor_restart.log" 2>&1 < /dev/null &
}

summarize() {
  log "all expected runs succeeded; generating summaries and audit cases"
  PYTHONPATH="${REMOTE_REPO}" "${REMOTE_VENV}/bin/python" \
    src/runner/summarize_icde_supplemental_agentpoison.py \
    2>&1 | tee -a "${LOG_DIR}/remote_monitor_summary.log"
  python3 scripts/export_audit_cases.py \
    2>&1 | tee -a "${LOG_DIR}/remote_monitor_audit_export.log"
}

while true; do
  write_status
  success_count="$(json_field success)"
  dir_count="$(json_field dirs)"
  batch_state="$(batch_running)"
  runner_state="$(runner_running)"
  log "progress success=${success_count}/${EXPECTED_RUNS} dirs=${dir_count} batch=${batch_state} runner=${runner_state}"

  if [ "${success_count}" -ge "${EXPECTED_RUNS}" ]; then
    summarize
    python3 -c 'import datetime,json,sys; s=json.load(open(sys.argv[1], encoding="utf-8")); s["monitor_status"]="complete"; s["completed_at"]=datetime.datetime.now().isoformat(timespec="seconds"); json.dump(s, open(sys.argv[2],"w", encoding="utf-8"), indent=2)' "${STATUS_FILE}" "${FINAL_FILE}"
    log "remote monitor complete; final status written to ${FINAL_FILE}"
    exit 0
  fi

  if [ "${batch_state}" = "no" ] && [ "${runner_state}" = "no" ]; then
    restart_batch
  fi

  sleep "${POLL_SECONDS}"
done
