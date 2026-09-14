#!/usr/bin/env python3
"""Run R1.1 E6-v2 using preregistered transport retries and a hard live pilot gate."""
from __future__ import annotations
import argparse
import concurrent.futures
import json
import os
import subprocess
import threading
from pathlib import Path
from src.common.provider_loader import load_provider_profile
from src.experiments.aamas_binding_semantic import BindingDryClient,matrix_cells
from src.experiments.aamas_binding_v2 import V2BindingEpisode as BindingEpisode, V2MiniMaxClient, TransportClient, TransportBudget, load_config, check_pilot
from src.experiments.aamas_llm_agents import utc_now
from src.runtime.policy import default_secret_policies


def run(config,tasks,profile,hashes,output,private_output=None,dry_run=False,source_sha=None,provider_settings=None,pilot=None):
    if not dry_run and config["phase"] == "formal":
        pc,_,_,_=load_config(Path("configs/experiment/aamas2027/e6_v2_pilot.json"))
        if pilot is None: raise ValueError("Live formal requires --pilot")
        check_pilot(pilot,pc)
        if json.loads((pilot/"registration.json").read_text())["source_preregistration_sha"] != source_sha:
            raise ValueError("Pilot must use the same pushed engineering amendment")
    output=output.resolve()
    if not dry_run:
        if private_output is None: raise ValueError('Live runs require private audit outside the repository')
        private_output=private_output.resolve(); repo=Path.cwd().resolve()
        if private_output==repo or repo in private_output.parents or private_output==output or output in private_output.parents:
            raise ValueError('Private full trace must be outside repository and artifact directory')
    output.mkdir(parents=True,exist_ok=False)
    if private_output is not None:
        private_output.mkdir(parents=True,exist_ok=False); private_output.chmod(0o700)
    registration={'config':config,'config_hashes':hashes,'source_preregistration_sha':source_sha,'system_prompt':profile['system_prompt'],'dry_run':dry_run,'registered_at':utc_now(),'planned_cells':matrix_cells(config)}
    (output/'registration.json').write_text(json.dumps(registration,indent=2)+'\n')
    lock=threading.Lock(); rows=[]
    def sink(kind,row):
        text=json.dumps(row,sort_keys=True)
        if any(p.raw_value in text for p in default_secret_policies()): raise ValueError('Raw secret in safe audit')
        with lock, (output/(kind+'.jsonl')).open('a') as f:
            f.write(text+'\n'); f.flush()
    def private_sink(row):
        if private_output is None: return
        with lock:
            fd=os.open(str(private_output/(row['run_id']+'.jsonl')),os.O_CREAT|os.O_WRONLY|os.O_APPEND,0o600)
            with os.fdopen(fd,'a') as f: f.write(json.dumps(row,sort_keys=True)+'\n')
    budget=TransportBudget(config["max_provider_requests"],sink,private_sink)
    by_id={t['task_id']:t for t in tasks}
    settings=provider_settings
    def job(cell):
        gen=config['generation']
        client=BindingDryClient() if dry_run else TransportClient(V2MiniMaxClient(model=config['model'],temperature=gen['temperature'],max_tokens=gen['max_tokens'],timeout_seconds=gen['timeout_seconds'],provider_settings=settings),budget)
        ep=BindingEpisode(by_id[cell['task_id']],cell['topology'],cell['condition'],cell['defense'],cell['seed'],config,client,sink,private_sink=private_sink,profile=profile)
        with budget.lock: stopped=budget.stop_reason
        if stopped:
            # Preserve every unstarted cell as blocked, with no provider request.
            ep.client=UnavailableClient()
        row=ep.run()
        with lock: rows.append(row)
    with concurrent.futures.ThreadPoolExecutor(max_workers=config['concurrency']) as pool:
        list(pool.map(job,matrix_cells(config)))
    result={'planned':len(matrix_cells(config)),'terminal':len(rows),'completed':sum(r['status']=='completed' for r in rows),'failed':sum(r['status']=='failed' for r in rows),'blocked':sum(r['status']=='blocked' for r in rows),'provider_requests':budget.attempts,'stop_reason':budget.stop_reason,'dry_run':dry_run,'completed_at':utc_now()}
    (output/'completion.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


class UnavailableClient:
    def available(self): return False


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--config',type=Path,required=True); p.add_argument('--output',type=Path,required=True)
    p.add_argument('--private-output',type=Path); p.add_argument('--provider-env',type=Path)
    p.add_argument("--pilot",type=Path)
    p.add_argument('--source-sha',required=True); p.add_argument('--dry-run',action='store_true')
    a=p.parse_args(); c,t,profile,hashes=load_config(a.config)
    # Credentials stay only in memory, never enter config registration.
    if a.provider_env and not a.dry_run:
        settings=load_provider_profile(str(a.provider_env),c['provider_profile'])
        if settings['model_name']!=c['model']: raise ValueError('Model profile mismatch')
        # Build client via existing environment loader, passed separately below.
        provider_settings=settings
    else: provider_settings=None
    actual=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
    if actual!=a.source_sha: raise ValueError('Recorded source SHA differs from checked out source')
    if not a.dry_run and subprocess.check_output(['git','diff','--name-only','HEAD'],text=True).strip():
        raise ValueError('Live source must match the pushed preregistration/amendment commit')
    print(json.dumps(run(c,t,profile,hashes,a.output,a.private_output,a.dry_run,a.source_sha,provider_settings=provider_settings,pilot=a.pilot)))

if __name__=='__main__': main()
