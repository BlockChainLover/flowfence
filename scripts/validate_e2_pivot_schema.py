#!/usr/bin/env python3
"""Check P0 interface shapes only; does not execute or certify a runtime."""
import argparse
import json
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dependency-path', type=Path, help='Optional directory containing jsonschema')
    parser.add_argument('--output', type=Path, help='Optional shape-check report path')
    args = parser.parse_args()
    if args.dependency_path:
        sys.path.insert(0, str(args.dependency_path))
    from jsonschema import Draft202012Validator
    root = Path(__file__).resolve().parents[1]
    inputs = root / 'experiments/e2_pivot_p0'
    schema = json.loads((inputs / 'HARNESS_SCHEMA.json').read_text())
    fixtures = json.loads((inputs / 'SCHEMA_FIXTURES.json').read_text())
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    checks = []
    for group, expected in [('positive', True), ('negative', False)]:
        for fixture in fixtures[group]:
            accepted = validator.is_valid(fixture['value'])
            checks.append({'id': fixture['id'], 'expected_accept': expected,
                           'accepted': accepted, 'pass': accepted == expected})
    report = {'scope': 'JSON_SCHEMA_SHAPE_ONLY', 'checks': checks,
              'passed': sum(c['pass'] for c in checks), 'total': len(checks),
              'runtime_implemented': False, 'models_executed': 0,
              'limitations': ['No authority/provenance authenticity check',
                             'No state/effect mediation execution',
                             'No evaluator or source integration',
                             'No frozen-defense behavioral parity validation']}
    output = json.dumps(report, indent=2) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output)
    print(output, end='')
    return 0 if report['passed'] == report['total'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
