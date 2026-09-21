#!/usr/bin/env python3
"""Render E2-A saved summary tables; never invoke a model or evaluator."""
import argparse
import json
from pathlib import Path


def load(path): return json.loads(path.read_text())


def table(headers, rows):
    return '\n'.join(['| '+' | '.join(headers)+' |', '| '+' | '.join(['---']*len(headers))+' |'] +
                     ['| '+' | '.join(str(v) for v in row)+' |' for row in rows])


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,default=Path('artifacts/aamas2027_e2a_formal'))
    p.add_argument('--report',type=Path,default=Path('E2A_FORMAL_REPORT.md'))
    a=p.parse_args();d=a.root/'derived';s=load(d/'summary.json');reg=load(a.root/'combined_registration.json') if (a.root/'combined_registration.json').exists() else load(a.root/'run/registration.json')
    privacy=load(d/'privacy_summary.json');execution=load(d/'execution_summary.json')
    status='COMPLETED' if s['readiness']=='COMPLETED' else 'NOT_READY'
    text=['# E2-A formal report', '', '**FORMAL CONFIRMATORY EVIDENCE — PARTIAL E2 TRANCHE**', '',
          f'Status: {status}. Preregistration commit: `{reg["E2A_FORMAL_PREREG_COMMIT"]}`.',
          'Primary semantic units: **40 public benchmark tasks**, 20 TAT-QA and20 HotpotQA. The720episodes are repeated observations, not720independent samples. P1=15/P2=15/P3=10/P4=0. Fact type is coupled to family; no causal fact-type comparison.', '',
          'BIRD was withdrawn before formal execution due to runtime-capability infeasibility under the frozen160000-byte guard; zero formal BIRD episodes. This is neither a negative privacy result nor a failed defense experiment. All historical IDs remain preserved. E2_B_STATUS: DEFERRED_NOT_SELECTED. Broader60-task E2 is incomplete.', '',
          '## Execution', '',
          f'Expected720; attempted{s["attempted"]}; finished{s["finished"]}; valid ordinary observations{s["valid"]}; completed finals{s["completed_finals"]}; unattempted by hard stop{s["unattempted_by_hard_stop"]}; pending/in-flight{s["remaining_pending_or_inflight"]}.', '',
          table(['Termination','Count'],sorted(s['termination_counts'].items())), '',
          'Provider and infrastructure failure counters overlap under the retained historical reporting convention. Transport timeout flags can overlap provider failures; do not add overlapping counters. A schema-valid final is not necessarily a correct answer.', '',
          table(['Family','Condition','Defense','Repetition','Attempted','Finals'],[(r['family'],r['condition'],r['defense'],r['repetition'],r['attempted'],r['completed_finals']) for r in execution['groups']]), '',
          '## Treatment', '',
          table(['Condition','Scheduled','Valid finance','Mediated','Quarantined','Released','Delivered','Pre-handoff failure'],[(k,v['scheduled'],v['valid_finance_handoff'],v['entered_mediation'],v['quarantined'],v['released'],v['delivered'],v['not_reached_early_failure']) for k,v in s['contamination'].items()]), '',
          f'Conditional entry: {s["treatment_entry_given_valid_handoff"]}. Each contaminated episode has separate stage/treatment/writer/final accounting in derived/stage_treatment_reachability.json. Non-reachability is not privacy success. Terminal R2 quarantine permits no replacement semantic handoff or writer.', '',
          '## Raw-value privacy', '',
          table(['Family','Condition','Defense','TRUE','FALSE','UNKNOWN'],[(r['family'],r['condition'],r['defense'],r['TRUE'],r['FALSE'],r['UNKNOWN']) for r in privacy['groups']]), '',
          'TRUE requires an observed unauthorized raw release; FALSE requires completed observation under the frozen rule. UNKNOWN remains unknown. No semantic, paraphrase or reconstruction privacy judge.', '',
          '## Original-evaluator utility', '',
          table(['Family','Metric','Success/attempted','Rate over attempted','Scored','Success/scored','Unknown'],[(f,'EM == 1.0' if f=='tatqa' else 'joint_em == 1.0',f'{v["success"]}/{v["attempted"]}',v['success']/v['attempted'] if v['attempted'] else None,v['scored'],f'{v["success"]}/{v["scored"]}',v['task_unknown']) for f,v in sorted(s['family_counts'].items())]), '',
          'Original metric vectors are retained in derived/evaluator_summary.json; complete evaluator inputs/outputs are retained privately. No pooled cross-family utility score. Failed ordinary episodes remain in attempted denominators. Task-level counts by family/condition/defense are in derived/execution_summary.json. TAT source-context clustering and Hotpot entity/title/context dependence restrict independence claims.', '',
          '## Integrity', '',
          f'Saved-evidence paired initial requests verified: {s["paired_initial_live_requests_verified"]}; implementation defects: {len(s["implementation_defects"])}. Frozen requests, treatment entry, release observations, raw privacy and original evaluator vectors are audited from saved trajectories by summarize_e2a_formal.py.',
          'Postrun frozen-file verification is recorded separately in postrun_integrity.json when execution terminates. Until that file exists, final integrity is pending. V3, stage schemas, prompts, model settings, budgets, policies, fact generation, recognizer, IFC, R2 and R3 remain subject to the original pins and Git comparison.', '',
          '## Artifacts and limits', '',
          '- Amendment: E2A_PREREGISTRATION_AMENDMENT.md',
          '- Frozen schedule: E2A_FORMAL_CELL_SCHEDULE.json',
          '- Run/artifact index: artifacts/aamas2027_e2a_formal/derived/artifact_index.json',
          '- Treatment audit: artifacts/aamas2027_e2a_formal/derived/stage_treatment_reachability.json',
          '- Failure audit: artifacts/aamas2027_e2a_formal/derived/failure_audit.json',
          '- Privacy summary: artifacts/aamas2027_e2a_formal/derived/privacy_summary.json',
          '- Evaluator summary: artifacts/aamas2027_e2a_formal/derived/evaluator_summary.json',
          '- Reproduction: E2A_FORMAL_REPRODUCTION.md', '',
          'Only TAT-QA/HotpotQA under the frozen standardized V3 harness are in scope. No four-type, complete E2, other-provider or general confidentiality claim. No formal reruns, replacements or outcome-based design changes. Stop after720or any implementation defect for human scientific review; do not select E2-B.']
    if 'E2A_REPORTING_FIX_COMMIT' in s:
        text += ['', '## Reporting correction and immutable continuation', '',
                 f'Reporting-fix commit: `{s["E2A_REPORTING_FIX_COMMIT"]}`. Original001–053 retained:53; original reruns:0. Continuation attempted:{s["continuation_attempted"]}/667; preflight:{s["continuation_preflight"]}.',
                 'The historical reporting-only defect was corrected prospectively with human authorization. No original episode triggered it or was invalidated. No source run was rewritten. Missing stage observations stay nullable/unavailable; no outcome is inferred from absent data.',
                 'Combined source index: '+str(a.root/'combined_index.json')+'. Reproduction: E2A_CONTINUATION_REPRODUCTION.md.']
    rendered='\n'.join(text)+'\n'
    rendered=rendered.replace('artifacts/aamas2027_e2a_formal/derived/',str(a.root/'derived')+'/')
    a.report.write_text(rendered)
    print(json.dumps({'report':str(a.report),'status':status,'attempted':s['attempted']}))

if __name__=='__main__':main()
