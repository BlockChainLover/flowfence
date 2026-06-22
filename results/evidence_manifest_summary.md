# Results Evidence Manifest Summary

Generated on 2026-06-22 from the current top-level `results/` directory and the two paper evidence maps. Updated after physical cleanup on 2026-06-22.

## Counts

- Current top-level `results/` entries: 158
- Canonical retained entries: 155
- Cleanup candidates: 97
- Cleanup candidates still present: 0
- Unclassified cleanup candidates: 0

The current top-level count includes the retained canonical entries plus generated manifest files. Cleanup candidates remain recorded for auditability, but their `exists` field is now `false`.

## Manifest Files

- `results/canonical_evidence_manifest.csv`: retained result entries and the evidence source that requires each one.
- `results/cleanup_candidates_manifest.csv`: non-canonical result entries and the reason each can be deleted after approval.
- `experiments/emnlp2026_flowfence/results_manifest.csv`: EMNLP-facing subset of retained result entries.
- `experiments/wine2026_flowfence/results_manifest.csv`: WINE-facing `results/` subset; WINE P1 evidence primarily lives under `artifacts/`.

## Safety Note

The reviewed cleanup candidates were deleted with `scripts/rebuttal_cleanup.py --scope results --execute --confirm DELETE_REBUTTAL_CLEANUP`. Use `results/cleanup_candidates_manifest.csv` as the audit trail for deleted non-canonical result families.
