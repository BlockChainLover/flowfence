# E2: runtime and audit storage microbenchmark

Complete: 3 modes × 3 event counts (1K, 10K, 100K) × 5 timing repetitions = 45 trials and 1,665,000 timed calls, plus 2,000 warmup calls per trial. No LLM calls; no failed or excluded trial. The eight cyclic event/channel recipes use the existing enterprise policy registry and real uppercase runtime event types. The mediator-off control constructs a minimal pass-through result without running a detector or risk scoring.

These records are timing trials, not completed tasks. Task utility is null and `utility_measured=false`. The required-schema exposure fields are zero placeholders because this benchmark does not evaluate privacy outcomes; do not aggregate those fields with E0/E1/E3 privacy measurements.

The timer encloses only the mediator function, including the same control dispatch and timer overhead for every mode. It excludes audit construction, serialization, loop bookkeeping, network, and LLM latency. The mode order rotates across repetitions. The exact nanosecond frequency histograms in `formal/episodes.jsonl` retain all measured samples including outliers; all quantiles use linear interpolation and are recomputable from those histograms.

| Mode | Mean µs | p50 µs | p95 µs | p99 µs | Events/s | Audit bytes/event |
|---|---:|---:|---:|---:|---:|---:|
| Off | 0.467 | 0.458 | 0.500 | 0.584 | 2,142,486 | 1,077.76 |
| IFC-SafeView | 2.770 | 1.125 | 6.041 | 6.792 | 361,028 | 1,525.47 |
| PAPC | 6.294 | 7.833 | 9.250 | 12.458 | 158,874 | 2,370.54 |

Values above pool the five 100K trials; full results include all three sizes. P50 above mean for PAPC reflects the mixture of cheap and expensive event paths. PAPC costs approximately 5.83 µs/event more than pass-through and 3.52 µs/event more than IFC on this host and event mix.

Storage is measured by actually serializing all 100K `EventRecord` objects per mode and the `PolicyDecisionRecord` emitted when an intervention fires, using the repository's sorted-key UTF-8 JSONL representation. Cumulative byte counts are saved at 1K, 10K, and 100K events. Identical repeated timing trials reuse these exact byte counts. Full hundreds-of-megabytes audit streams are discarded after byte measurement; `formal/serialized_audit_fixtures.jsonl` retains actual serialized examples, and a smoke test verifies their byte counts exactly. Content previews are omitted from this shareable audit variant. This is a measurement of that privacy-safe record layout, not private full-trajectory storage or disk write latency.

At 100K events the measured audit sizes are 107,776,381 / 152,547,216 / 237,054,161 bytes for off / IFC / PAPC. Normalizing bytes/event to a stated reference of 24 events gives 25.26 / 35.75 / 55.56 KiB per reference task. This normalized figure is not observed whole-workflow task storage. Storage growth is approximately linear, with small changes from numeric step fields.

Limitations: one host, short synthetic content, four original exact-value policies, and the specified allow/rewrite/lease event mix. It is not a concurrency/load test or a worst-case quarantine benchmark. No production latency guarantee or large-context scaling claim is supported.

Run:

```bash
PYTHONPATH=. python3 scripts/run_aamas_stress.py --config configs/experiment/aamas2027/e2_overhead.json --output artifacts/aamas2027/E2_overhead/formal --tables artifacts/aamas2027/tables
```

Existing raw data are intentionally not overwritten; use a fresh output directory to rerun. Rebuild summaries from the retained raw measurements:

```bash
PYTHONPATH=. python3 scripts/run_aamas_stress.py --config configs/experiment/aamas2027/e2_overhead.json --output artifacts/aamas2027/E2_overhead/formal --tables artifacts/aamas2027/tables --summarize-only
```
