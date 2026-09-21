# E2-A implementation-defect human review

Status: NOT_READY. Run stopped after53formal cells;667unattempted. No live/auditor patch, resume, rerun, replacement or outcome-based scientific change.

## Independently established defect

`run_e2a_formal.py` lines60–63 catches initialization/observer exceptions and saves a minimal `IMPLEMENTATION_DEFECT` observation. That path may have no trajectory and no stage fields. `summarize_e2a_formal.py` line29 accepts missing trajectory for such a record and continues. Its aggregate at line130 later unconditionally reads `planner_stage_success` from every episode. A minimal record emitted by the runner therefore produces `KeyError: 'planner_stage_success'`; failure accounting cannot complete for this supported runner failure path.

This defect was identified by inspection and confirmed with one isolated synthetic fixture, without any provider/evaluator request and without modifying formal evidence. **No real formal episode encountered a setup exception or this reporting failure.** The current53ordinary observations remain valid; the run-level defect count is1, episode-level defect count0. The user's rule requires stopping upon discovery, so new cells were stopped even though the faulty path had not occurred in live observations. This is not a model/provider failure, treatment-invariant failure or negative privacy finding.

## Exact zero-call reproduction

Run from repository root. It only creates and deletes temporary fixture files; it never calls the provider or original evaluator.

```sh
PYTHONPATH=.:/private/tmp/e2_s0_deps /opt/homebrew/bin/python3 - <<'PY'
import json, subprocess, sys, tempfile
from pathlib import Path
from src.e2_live.e2a import SCHEDULE, LABEL
from src.e2_live.pilot import load
with tempfile.TemporaryDirectory() as td:
    root=Path(td); run=root/'run'; run.mkdir(); private=root/'private'; private.mkdir()
    cell=load(SCHEDULE)[0]
    episode={**cell,'label':LABEL,'termination':'IMPLEMENTATION_DEFECT','valid':False,
             'implementation_defect_type':'RuntimeError',
             'live_integrity_defects':['RUNNER_SETUP_OR_AUDIT_EXCEPTION']}
    (run/'attempts.jsonl').write_text(json.dumps(cell)+'\n')
    (run/'episodes.jsonl').write_text(json.dumps(episode)+'\n')
    (run/'completion.json').write_text('{}\n')
    result=subprocess.run([sys.executable,'scripts/summarize_e2a_formal.py',
        '--run',str(run),'--private',str(private),'--output',str(root/'derived')],
        text=True,capture_output=True)
    assert result.returncode != 0
    assert "KeyError: 'planner_stage_success'" in result.stderr
    print({'confirmed_defect':True,'model_calls':0,'evaluator_calls':0})
PY
```

## Stop and preservation

`run/STOP` was written at2026-09-21T04:42:30.166955+00:00. Cell053was already in flight; it completed at04:42:31.620728+00:00 and the runner exited successfully. All53start timestamps precede STOP; no054attempt. There were141MiniMax requests, all metadata retained, and no retry. Private modes700/600; private directory Git-ignored. Source/evaluator pins, V3, prompts/schemas/model config/budgets, policies/fact generation, recognizer, R2/IFC, R3 and confirmatory manifest unchanged. See artifacts/aamas2027_e2a_formal/postrun_integrity.json.

## Scope and recommendation

There are40planned semantic tasks, but this prefix observed only27unique tasks (13TAT-QA and14HotpotQA). It is an incomplete, unbalanced prefix with one unmatched arm at cell053. Do not infer a full-tranche result, independent720samples, broad defense superiority or final four-type coverage. Quarantine and pre-handoff failures do not imply privacy success.

Recommended HUMAN decision: review the isolated failure-accounting defect and preservation evidence; decide whether to authorize a prospective reporting-only correction and a separately registered continuation of054–720. No completed cell needs or is authorized for rerun. No correction/continuation has been implemented or authorized. Next gate: HUMAN_IMPLEMENTATION_DEFECT_REVIEW_NO_EXECUTION. E2-B remains DEFERRED_NOT_SELECTED.
