# Rebuttal Quick Lookup - 2026-06-22

## Start Here

Use this file as the first stop during rebuttal. It points to the canonical paper, evidence, metric, and cleanup locations after the two-paper organization work.

## Active Papers

| Paper | Source directory | Evidence map | Contract |
| --- | --- | --- | --- |
| EMNLP retrieval-memory containment | `papers/emnlp2026_flowfence/` | `experiments/emnlp2026_flowfence/README.md` | `research/contract/emnlp2026_flowfence.md` |
| WINE privacy propagation externalities | `papers/wine2026_flowfence/` | `experiments/wine2026_flowfence/README.md` | `research/contract/wine2026_flowfence.md` |

## Common Rebuttal Questions

| Question | First file to open | Supporting files |
| --- | --- | --- |
| Which paper table supports which claim? | `experiments/emnlp2026_flowfence/README.md`, `experiments/wine2026_flowfence/README.md` | Paper `main.tex` and `tables/` under each retained paper directory |
| What does each metric mean? | Per-paper evidence map `Metric Definitions` section | WINE metric table `papers/wine2026_flowfence/tables/table_metric_impl.tex`; EMNLP appendix metrics in `papers/emnlp2026_flowfence/main.tex` |
| Which raw `results/` entries must be kept? | `results/canonical_evidence_manifest.csv` | `experiments/emnlp2026_flowfence/results_manifest.csv`, `experiments/wine2026_flowfence/results_manifest.csv` |
| Which `results/` entries are redundant? | `results/cleanup_candidates_manifest.csv` | `research/notes/rebuttal_cleanup_manifest_2026-06-22.md` |
| Which old `papers/` entries can be deleted? | `research/notes/paper_cleanup_candidates_manifest.csv` | `scripts/rebuttal_cleanup.py --scope papers` dry-run output |
| Is the repository physically clean yet? | `research/notes/rebuttal_organization_completion_audit_2026-06-22.md` | `find papers -maxdepth 1 -mindepth 1 -print | sort`; `results/evidence_manifest_summary.md` |
| How do we safely execute cleanup? | `scripts/rebuttal_cleanup.py --help` | `research/notes/rebuttal_cleanup_manifest_2026-06-22.md` |

## Evidence Boundaries

- EMNLP evidence is mainly retrieval-memory containment on an adapted AgentPoison full-ReAct axis.
- WINE evidence is multi-agent privacy propagation with MiniMax final-writer and deterministic synthetic-runtime slices.
- MiniMax is the only real provider allowed for current-phase WINE experiments.
- WINE P1 raw provider outputs and raw traces are intentionally not committed; use committed high-level summaries and safe traces.
- Do not claim official AgentPoison reproduction, production safety, arbitrary adaptive robustness, or non-MiniMax generalization.

## Cleanup Status

Current state:

- Evidence maps: complete.
- Per-paper contracts: complete.
- Result manifests: complete.
- Safe cleanup script: complete and dry-run validated.
- Physical deletion: pending explicit approval.

Dry-run counts:

- Paper cleanup candidates: 17.
- Result cleanup candidates: 97.
- Total cleanup candidates: 114.

Execution commands after approval:

```bash
python3 scripts/rebuttal_cleanup.py --scope papers --execute --confirm DELETE_REBUTTAL_CLEANUP
python3 scripts/rebuttal_cleanup.py --scope results --execute --confirm DELETE_REBUTTAL_CLEANUP
```
