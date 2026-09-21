# Descriptive tables for the AAMAS review revision

All outputs aggregate saved results. No model calls, source evaluator calls, privacy relabeling, experiment reruns or new task selection were performed.

- `e2a_public_utility_tables.{csv,json}`: all 12 family × condition × defense groups; 60 attempts per group, including failures. Primary privacy totals remain TRUE 0 / FALSE 421 / UNKNOWN 299. The JSON also records clean intervention observations and incomplete IFC runtime delivery/invocation accounting.
- `e2a_public_utility_table.tex`: generated table values used by the manuscript.
- `controlled_task_clusters.csv`: byte-preserving copy of historical safe task-cluster evidence at `9615ca34`.
- `recognizer_controlled.json`: initial independent descriptive controlled-outcome audit, despite its historical filename; it is not a detector accuracy dataset.
- `controlled_cluster_reanalysis.json`: recomputation of the six-cluster estimates, exact enumeration of 46,656 resamples, and sign tests. This is explicitly post hoc, not preregistered inference.

Run from the repository root with its Git history available:

```bash
PYTHONPATH=. python3 scripts/recompute_aamas2027_public_tables.py --episodes artifacts/aamas2027_e2a_combined/derived/episode_summary.json.gz
PYTHONPATH=. python3 scripts/recompute_aamas2027_controlled_clusters.py
```

Both scripts support `--help`. Output files here may be regenerated; original formal evidence is not overwritten. In a standalone manuscript ZIP, the included summaries can be read without the repo, but source recomputation requires the referenced repository evidence and history.
