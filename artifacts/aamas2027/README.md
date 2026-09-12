# AAMAS 2027 experiment artifact

Current R1 status: **partial formal evidence**. Start with [R1_REVIEWER_HANDOFF.md](R1_REVIEWER_HANDOFF.md). Provider execution stopped by the preregistered infrastructure-failure rule; no PAPC advantage is established.

Start with `EXPERIMENT_SUMMARY.md`, `PAPER_INTEGRATION.md`, `MANIFEST.json`, and `PRIOR_EVIDENCE_AUDIT.md`. Tables are CSV/JSON; raw records are safe JSONL with text omitted. E0/E1 are workflow episodes, E2 rows are timing trials, and E3 rows are injected representation probes. Do not pool their utility/privacy metrics.

From the extracted bundle root (Python 3.10+; experiment/report execution uses the standard library, tests additionally require pytest>=7.0):

```bash
PYTHONPATH=. python scripts/package_aamas2027.py --reports-only
PYTHONPATH=. python -m pytest tests/test_aamas_*.py
PYTHONPATH=. python scripts/run_aamas_equal.py --help
PYTHONPATH=. python scripts/run_aamas_llm_agents.py --help
PYTHONPATH=. python scripts/run_aamas_stress.py --help
```

Exact original experiment commands and generation settings are in MANIFEST/config registrations. Use a new output directory to rerun; historical/formal outputs must not be overwritten. MiniMax live runs require credentials supplied through the environment, never committed files. Dry-run fixtures only verify wiring and are not model evidence. Reports use first-attempt formal LLM rows, retain failed/blocked/linked retry attempts, and keep pilot separate.

Bundle inclusion uses explicit source/config file names and safe artifact basename rules. It contains only AAMAS experiment dependencies, configs, source, tests, text-free episode/event/call records, latency histograms, summaries, tables, logs, manifest, and reports. Historical archives, raw model prompts/responses, private credentials, environment files, caches, and virtual environments are excluded. Public synthetic protected-value fixtures intentionally occur in executable policy/attack/test/data source so replay works; this is distinct from safe result records, which are scanned for those registered raw values before packaging. No assertion is made that executable source contains no synthetic fixture values.

Source-versus-generated exposure counters separate exogenous injected material from LLM-generated actions. Original WINE summaries are audit references only and are not bundled; the attack-ranking rows and relevant history are preserved in `prior_evidence_inventory.json` and `PRIOR_EVIDENCE_AUDIT.md`.

## R1 review entry

Start with R1_PREREGISTRATION.md, R1_METRIC_DEFINITIONS.md and E6_binding_semantic/derived/REPORT.md. Rebuild corrected E0/E1 and E6 tables with `PYTHONPATH=. python scripts/integrate_aamas_r1.py`. It reads safe event/call/episode records, never calls a provider, preserves old formal records and retains E3/E4 negative evidence.
