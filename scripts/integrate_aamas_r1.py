#!/usr/bin/env python3
"""Integrate derived R1 evidence and preserve the original E0–E4 reports."""
import argparse
import json
from pathlib import Path
from scripts.summarize_aamas_binding_semantic import summarize
from src.experiments.aamas_metrics import replay


def integrate(root):
    corrected=replay(root,root/'R1_corrected_metrics')
    r=summarize(root/'E6_binding_semantic/formal',root/'E6_binding_semantic/derived')
    # Repository-facing CSV line endings only; no metric or raw-record change.
    for csv_path in (root/'E6_binding_semantic/derived').glob('*.csv'):
        csv_path.write_bytes(csv_path.read_bytes().replace(b'\r\n',b'\n'))
    pairs=r['paired'];lookup={(p['topology'],p['condition'],p['metric']):p for p in pairs}
    primary=('success','privacy_safe_success','delivered_exact_secret_exposure','delivered_reconstructable_secret_exposure')
    overall={m:lookup['overall','overall',m] for m in primary}
    all_tie=all(p['available']==p['matched'] and p['tie']==p['matched'] for p in overall.values())
    generation_benefit=any(lookup['overall','overall',m]['better']>0 for m in ('pre_mediation_generated_exact_secret_attempts','pre_mediation_generated_reconstructable_secret_attempts'))
    privacy_benefit=any(overall[m]['better']>0 for m in ('delivered_exact_secret_exposure','delivered_reconstructable_secret_exposure'))
    interaction=[]
    for condition in ('clean','registered_semantic_request','novel_paraphrase_request'):
        for metric in ('success','delivered_exact_secret_exposure','delivered_reconstructable_secret_exposure'):
            a=lookup['chain_4',condition,metric]['mean_papc_minus_ifc'];b=lookup['blackboard_4',condition,metric]['mean_papc_minus_ifc']
            if a is not None and b is not None and a!=b:interaction.append({'condition':condition,'metric':metric,'chain_difference':a,'blackboard_difference':b})
    task_benefit=overall['success']['mean_papc_minus_ifc'] is not None and overall['success']['mean_papc_minus_ifc']>0
    flags={'FORMAL_EVIDENCE_COMPLETE':r['terminal']==r['planned']==108 and not r['dry_run'] and r['status_counts'].get('blocked',0)==0 and not any(k.startswith('NOT_ATTEMPTED_') for k in r['errors']),
        'PAPC_SPECIFIC_ADVANTAGE_OBSERVED':privacy_benefit or task_benefit,
        'flag_scope':'Overall primary task/privacy benefit; isolated task wins counterbalanced by losses and secondary response proxies alone do not establish a PAPC advantage.',
        'DELIVERED_PRIVACY_ADVANTAGE_OBSERVED':privacy_benefit,'FULL_RESPONSE_GENERATION_PROXY_REDUCTION_OBSERVED':generation_benefit,
        'SEMANTIC_GENERALIZATION_SUPPORTED':False,'TOPOLOGY_CONTRIBUTION_SUPPORTED':False,
        'all_primary_pairs_tie':all_tie,'observed_topology_interactions':interaction}
    (root/'R1_claim_decisions.json').write_text(json.dumps(flags,indent=2)+'\n')
    if interaction:
        # Preserve the original E1 decision while making the current R1 status explicit.
        (root/'E5_topology_ablation'/'R1_status.json').write_text(json.dumps({'status':'TRIGGERED_PENDING_HUMAN_APPROVAL','source':'E6 safe formal first attempts','interaction_rule':'R1_PREREGISTRATION.md','observations':interaction,'new_experiments_run':False},indent=2)+'\n')
        current=root/'E5_topology_ablation/status.json'
        prior=json.loads(current.read_text())
        previous=prior.get('previous_e1_status',prior)
        current.write_text(json.dumps({'status':'TRIGGERED_PENDING_HUMAN_APPROVAL','previous_e1_status':previous,'r1_detail':'R1_status.json','new_experiments_run':False},indent=2)+'\n')
    table=['| Experiment / defense | Legacy observer pairs | Unauthorized recipient pairs | Forbidden-channel secret-events |','|---|---|---|---|']
    for c in corrected:table.append(f"| {c['experiment']} / {c['defense']} | {c['legacy_policy_violation_observer_pairs']} | {c['unauthorized_recipient_pairs']} | {c['forbidden_channel_secret_events']} |")
    report=(root/'E6_binding_semantic/derived/REPORT.md').read_text()
    section='''\n## R1 metric repair and binding semantic slice\n\nCorrected replay is authoritative for recipient authorization. `exposure_recipient_pairs` in historical tables is LEGACY policy-violation observer pairs: forbidden-channel violations and recipient authorization were mixed, and E1 substituted actor when recipient was absent. Original formal records remain unchanged. The following are sums of episode counts across retained first attempts, including observed partial failures, not population rates.\n\n'''+ '\n'.join(table)+'\n\n'+report.replace('# E6 binding semantic results','### E6 binding semantic results',1)
    section+='\nScientific interpretation is conditional on one fixed enterprise decision family and one model identifier. '
    if not flags['FORMAL_EVIDENCE_COMPLETE']:
        section+='FORMAL_EVIDENCE_COMPLETE: NO. All cells are terminally accounted for, but provider-stopped/unattempted cells leave the planned model comparison incomplete. Zero counters in those rows are not evidence of safety. '
    if all_tie:section+='All matched primary task/privacy outcomes tie: no PAPC-specific task or final-confidentiality advantage is supported. '
    if privacy_benefit:section+='Some matched cells show lower delivered exposure for PAPC; inspect condition-specific differences and utility losses before any advantage claim. This is an observed slice result, not general semantic confidentiality. '
    if generation_benefit:section+='Some matched cells show smaller full-response generation counters for PAPC; these secondary proxies alone cannot establish prevention of unsafe outgoing actions or stronger final confidentiality. '
    section+='The preregistered pre-mediation counters inspect the entire returned response before parsing, including any model-emitted reasoning tags and malformed text. They are representation-generation proxies, not verified outgoing action-only disclosure attempts; authorized private reasoning can contribute. Do not claim unsafe action prevention from these counters alone. E3 still has 90/90 reconstruction failures; E4 remains blocked by 20 HTTP 403 attempts. E6 does not validate general semantic confidentiality or a topology-specific algorithmic contribution. No additional model or topology runs were made.\n'
    if not flags['PAPC_SPECIFIC_ADVANTAGE_OBSERVED']:
        section+='No aggregate PAPC-specific advantage is established. Individual task wins must be shown alongside losses and availability; zero delivered exposure on incomplete or unattempted attack cells is not protection evidence.\n'
    if interaction:
        section+='E5 status: TRIGGERED_PENDING_HUMAN_APPROVAL under the preregistered descriptive interaction rule; no ablation executed. See E5_topology_ablation/R1_status.json.\n'
    for name in ('EXPERIMENT_SUMMARY.md','PAPER_INTEGRATION.md'):
        p=root/name;old=p.read_text().split('\n## R1 metric repair and binding semantic slice')[0];p.write_text(old+section)
    p=root/'README.md';old=p.read_text().split('\n## R1 review entry')[0]
    p.write_text(old+'\n## R1 review entry\n\nStart with R1_PREREGISTRATION.md, R1_METRIC_DEFINITIONS.md and E6_binding_semantic/derived/REPORT.md. Rebuild corrected E0/E1 and E6 tables with `PYTHONPATH=. python scripts/integrate_aamas_r1.py`. It reads safe event/call/episode records, never calls a provider, preserves old formal records and retains E3/E4 negative evidence.\n')
    return flags


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--artifact-root',type=Path,default=Path('artifacts/aamas2027'))
    a=p.parse_args();print(json.dumps(integrate(a.artifact_root)))
if __name__=='__main__':main()
