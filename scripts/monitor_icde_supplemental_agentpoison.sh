#!/usr/bin/env bash
set -uo pipefail

REMOTE_HOST="${REMOTE_HOST:-wentian-server}"
REMOTE_REPO="${REMOTE_REPO:-/home/huang/agent-privacy-defense/FlowFence-Lite}"
REMOTE_VENV="${REMOTE_VENV:-${REMOTE_REPO}/.envs/FlowFence_py313}"
EXPECTED_RUNS="${EXPECTED_RUNS:-87}"
POLL_SECONDS="${POLL_SECONDS:-300}"
LOCAL_ARTIFACT_ROOT="${LOCAL_ARTIFACT_ROOT:-artifacts/icde2027_supplemental}"
LOG_DIR="${LOCAL_ARTIFACT_ROOT}/logs"
MONITOR_DIR="${LOCAL_ARTIFACT_ROOT}/monitor"
LOG_FILE="${LOG_DIR}/monitor.log"
STATUS_FILE="${MONITOR_DIR}/latest_status.json"
FINAL_FILE="${MONITOR_DIR}/final_status.json"

mkdir -p "${LOG_DIR}" "${MONITOR_DIR}"

log() {
  printf '[%s] %s\n' "$(date '+%F %T')" "$*" | tee -a "${LOG_FILE}"
}

remote() {
  ssh -o ConnectionAttempts=1 -o ConnectTimeout=8 "${REMOTE_HOST}" "$@"
}

remote_status() {
  remote "cd ${REMOTE_REPO} && python3 -c 'import json,pathlib,collections; expected=int(${EXPECTED_RUNS}); ds=list(pathlib.Path(\"results\").glob(\"icde_*\")); rows=[]; [rows.append(((d/\"status.txt\").read_text().strip() if (d/\"status.txt\").exists() else \"missing\", d.name)) for d in ds]; counts=collections.Counter(s for s,_ in rows); failed=[{\"status\":s,\"run\":n} for s,n in sorted(rows) if s!=\"success\"]; print(json.dumps({\"expected\":expected,\"dirs\":len(ds),\"success\":counts.get(\"success\",0),\"counts\":dict(counts),\"failed_or_missing\":failed[:60]}, indent=2))'"
}

remote_batch_running() {
  remote "pgrep -af run_icde_supplemental_agentpoison_remote.sh >/dev/null && echo yes || echo no"
}

remote_runner_running() {
  remote "pgrep -af run_agentpoison_fullreact.py >/dev/null && echo yes || echo no"
}

restart_remote_batch() {
  log "remote batch is not active and run set is incomplete; starting resumable remote runner"
  remote "cd ${REMOTE_REPO} && mkdir -p artifacts/icde2027_supplemental/logs && setsid bash scripts/run_icde_supplemental_agentpoison_remote.sh > artifacts/icde2027_supplemental/logs/nohup_monitor_restart.log 2>&1 < /dev/null & echo monitor_restart_started"
}

summarize_remote() {
  log "all expected runs succeeded; generating remote summaries and audit cases"
  remote "cd ${REMOTE_REPO} && PYTHONPATH=${REMOTE_REPO} ${REMOTE_VENV}/bin/python src/runner/summarize_icde_supplemental_agentpoison.py && python3 scripts/export_audit_cases.py"
}

sync_back() {
  log "syncing remote results and supplemental artifacts back to local workspace"
  rsync -avz "${REMOTE_HOST}:${REMOTE_REPO}/results/" ./results/ >>"${LOG_FILE}" 2>&1
  rsync -avz "${REMOTE_HOST}:${REMOTE_REPO}/artifacts/icde2027_supplemental/" "./${LOCAL_ARTIFACT_ROOT}/" >>"${LOG_FILE}" 2>&1
}

while true; do
  status_json="$(remote_status)"
  printf '%s\n' "${status_json}" > "${STATUS_FILE}"
  success_count="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["success"])' "${STATUS_FILE}")"
  dir_count="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["dirs"])' "${STATUS_FILE}")"
  batch_running="$(remote_batch_running)"
  runner_running="$(remote_runner_running)"
  log "progress success=${success_count}/${EXPECTED_RUNS} dirs=${dir_count} batch=${batch_running} runner=${runner_running}"

  if [ "${success_count}" -ge "${EXPECTED_RUNS}" ]; then
    summarize_remote
    sync_back
    python3 -c 'import json,sys,datetime; s=json.load(open(sys.argv[1])); s["monitor_status"]="complete"; s["completed_at"]=datetime.datetime.now().isoformat(timespec="seconds"); json.dump(s, open(sys.argv[2],"w"), indent=2)' "${STATUS_FILE}" "${FINAL_FILE}"
    log "monitor complete; final status written to ${FINAL_FILE}"
    exit 0
  fi

  if [ "${batch_running}" = "no" ] && [ "${runner_running}" = "no" ]; then
    restart_remote_batch
  fi

  sleep "${POLL_SECONDS}"
done
