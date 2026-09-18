#!/usr/bin/env python3
"""Diagnose MARBLE rating formatting and optionally apply the human-approved escape-only repair."""
import argparse
import difflib
import json
from pathlib import Path
import re
import subprocess
import sys
import traceback


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--benchmark', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--apply-approved', action='store_true', help='Apply only after human review of local formatting repair')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    name = 'marble/evaluator/evaluator_prompts.json'
    base = '8d60fa17b5596b44458a52d4296061b9fc13d6f2'
    def git(*a):
        return subprocess.check_output(['git', '-C', str(args.benchmark), *a], text=True, stderr=subprocess.DEVNULL)
    source = git('show', base + ':' + name)
    data = json.loads(source)
    kwargs = dict(task='TASK {literal}', communications='COMMS', summary='SUMMARY', agent_profiles='ROLES', agent_tasks='TASKS', results='RESULTS')
    checks = []
    for category in ('Planning', 'Communication'):
        prompt = data['Graph'][category]['prompt']
        try:
            prompt.format(**kwargs)
        except KeyError:
            (args.output/(category+'_MINIMAL_STACK.txt')).write_text(traceback.format_exc())
        else:
            raise AssertionError('expected original failure')
        fixed = re.sub(r'(?<!\{)\{"rating": (X|4|2)\}(?!\})', r'{{"rating": \1}}', prompt)
        expected = re.sub(r'\{(task|communications|summary|agent_profiles|agent_tasks|results)\}', lambda m:kwargs[m[1]], prompt)
        assert fixed.format(**kwargs) == expected
        assert fixed.count('{{"rating":') == 3
        checks.append(dict(category=category,original_failure='KeyError: rating',rendered_bytes_equal_intended=True,json_examples=3))
    # Operate on original bytes, retaining whitespace and every other prompt.
    repaired = re.sub(r'(?<!\{)\{(\\"rating\\": (?:X|4|2))\}(?!\})', r'{{\1}}', source)
    assert repaired != source
    parsed = json.loads(repaired)
    for category in ('Planning', 'Communication'):
        assert parsed['Graph'][category]['prompt'].format(**kwargs) == re.sub(r'\{(task|communications|summary|agent_profiles|agent_tasks|results)\}', lambda m:kwargs[m[1]], data['Graph'][category]['prompt'])
    patch = ''.join(difflib.unified_diff(source.splitlines(True), repaired.splitlines(True), fromfile='a/'+name, tofile='b/'+name))
    (args.output/'marble_rating_braces.patch').write_text(patch)
    # Search every reachable version at current and historical paths, not just branch tips.
    paths = sorted({p for p in git('log','--all','--format=','--name-only','--','*evaluator*prompt*').splitlines() if p.endswith('.json')})
    candidates=[]; versions=0
    for path in paths:
        for commit in git('log','--all','--format=%H','--',path).splitlines():
            try:version=json.loads(git('show',commit+':'+path))
            except (subprocess.CalledProcessError, ValueError):continue
            versions += 1
            try:prompts=[version['Graph'][c]['prompt'] for c in ('Planning','Communication')]
            except KeyError:continue
            if not all('"rating"' in p for p in prompts):continue
            try:
                for p in prompts:p.format(**kwargs)
            except (KeyError,ValueError):continue
            candidates.append({'commit':commit,'path':path})
    report=dict(python=sys.version,checks=checks,history_paths=paths,history_versions=versions,upstream_candidates=candidates,
                base_and_40ddb54_same_template=git('show','40ddb54b5a379b53196d1bdf20e861dc6f922e19:'+name)==source,
                classification='C_LOCAL_NONSEMANTIC_FORMATTING_ONLY_HUMAN_APPROVED',semantic_change=False,applied=False)
    # Classification recorded before the benchmark mutation.
    (args.output/'RATING_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n')
    if args.apply_approved:
        assert not candidates, 'review official candidate before applying a local patch'
        target=args.benchmark/name
        assert target.read_text() in (source,repaired)
        target.write_text(repaired)
        report['applied']=True
        (args.output/'RATING_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))

if __name__ == '__main__':
    main()
