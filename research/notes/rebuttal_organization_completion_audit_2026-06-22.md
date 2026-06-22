# Rebuttal Organization Completion Audit - 2026-06-22

## Objective Requirements

1. Keep only the EMNLP and WINE paper drafts under `papers/`; delete unused paper material.
2. Create one `experiments/` folder per paper with a Markdown evidence map linking paper tables, claims, metrics, and raw/source artifacts.
3. Clean `results/` so necessary raw results remain and redundant smoke/diagnostic results are removed.
4. Add per-paper contract docs under `research/contract/`.
5. Update research logs and durable Codex task state.

## Current Evidence

| Requirement | Status | Evidence |
| --- | --- | --- |
| Two paper evidence maps | done | `experiments/emnlp2026_flowfence/README.md`, `experiments/wine2026_flowfence/README.md` |
| Per-paper result manifests | done | `experiments/emnlp2026_flowfence/results_manifest.csv`, `experiments/wine2026_flowfence/results_manifest.csv` |
| Per-paper contracts | done | `research/contract/emnlp2026_flowfence.md`, `research/contract/wine2026_flowfence.md` |
| Results classification | done | `results/canonical_evidence_manifest.csv`, `results/cleanup_candidates_manifest.csv`, `results/evidence_manifest_summary.md` |
| Paper cleanup classification | done | `research/notes/paper_cleanup_candidates_manifest.csv` |
| Safe cleanup execution path | done | `scripts/rebuttal_cleanup.py --help`; default is dry-run |
| Logs/task state | done | `research/logs/roadmap.md`, `research/logs/progress.md`, `artifacts/codex_task_state/codex_rebuttal_repo_organization.md` |
| Rebuttal quick lookup | done | `research/notes/rebuttal_quick_lookup_2026-06-22.md` |
| Physical `papers/` cleanup | done | `find papers -maxdepth 1 -mindepth 1 -print | sort` shows only `papers/README.md`, `papers/emnlp2026_flowfence`, and `papers/wine2026_flowfence`. |
| Physical `results/` cleanup | done | `python3 scripts/rebuttal_cleanup.py --scope results` reports 97 missing cleanup candidates and 0 existing cleanup candidates; retained manifests still resolve. |
| Top-level experiment cleanup | done | `experiments/` contains `README.md` and one subfolder per retained paper. Legacy top-level planning files were removed after their useful state was superseded by per-paper evidence maps and the progress log. |

## Completion Verdict

The objective is complete as of the 2026-06-22 audit pass:

- `papers/` is physically limited to the two retained paper directories and navigation README.
- `experiments/` has one canonical evidence-map folder per retained paper.
- `results/` keeps retained raw/supporting evidence and generated manifests; reviewed smoke, diagnostic, AgentDojo, ASB, dry-run, and superseded pre-method cleanup candidates have been removed.
- `research/contract/` contains independent EMNLP and WINE contracts.
- `research/logs/progress.md` and the durable Codex task-state file record the cleanup and validation steps.

## Cleanup Commands Used

Dry runs and execution:

```bash
python3 scripts/rebuttal_cleanup.py --scope papers
python3 scripts/rebuttal_cleanup.py --scope results
python3 scripts/rebuttal_cleanup.py --scope papers --execute --confirm DELETE_REBUTTAL_CLEANUP
python3 scripts/rebuttal_cleanup.py --scope results --execute --confirm DELETE_REBUTTAL_CLEANUP
```

Post-cleanup verification:

```bash
find papers -maxdepth 1 -mindepth 1 -print | sort
find experiments -maxdepth 2 -type f -print | sort
python3 - <<'PY'
import csv
for path in [
    'results/canonical_evidence_manifest.csv',
    'results/cleanup_candidates_manifest.csv',
]:
    rows = list(csv.DictReader(open(path)))
    print(path, len(rows), sum(r.get('exists') == 'true' for r in rows))
PY
git status --short
```
