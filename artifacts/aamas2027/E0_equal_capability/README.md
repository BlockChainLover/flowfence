# E0: equal-capability IFC-SafeView

Complete: 270 deterministic episodes, one historical enterprise task, three topologies, ten attack settings (including clean), three seeds, three defenses. PAPC is the non-oracle existing implementation; comparison contains90 PAPC/IFC pairs.

Both guards share the same event calls, policy registry, protected-value substring semantics, generator and exact-value safe-view validator. IFC returns before PAPC risk/topology/request features are computed, allows authorized raw values on allowed channels, otherwise rewrites through the shared view and blocks invalid views. No threshold or attack selection was changed after formal outcomes.

The additive evaluation adapter corrects three historical harness limitations for every defense: incomplete intermediate interception; premediation and240-character-truncated measurement; final-candidate behavior selected by defense name. It retains historical attack inputs, route patterns and scripted candidate templates. Therefore this is a corrected matched evaluation, not byte-identical WINE reproduction. Template utility is still weak and privacy-sensitive; use E1 structured correctness for stronger task evidence.

PAPC and IFC both have90/90 success and90/90 privacy-safe success, zero raw/external exposure and zero unique exposed pairs. All90 privacy and utility comparisons tie. Mean interventions are1.2 PAPC vs0.9 IFC; blocks0.3 vs0.0. PAPC intervention better/tie/worse=0/66/24; blocks=0/63/27. These results do not support PAPC superiority over equal capabilities.

Metrics: raw_exposure counts delivered secret-event violations; external_exposure counts exposed external events; exposure_recipient_pairs counts unique protected-item/recipient pairs. Cascade counts delivered events carrying observed poisoned instructions or unauthorized raw values; it does not propagate an unconditional historical ancestor contamination bit. Quarantine hides the raw source and may release only the common validated view. Only in-memory text is measured; saved audits contain IDs, action counts and measurements without private or poison content. `status=complete` denotes completed execution, success is separate.

The sign test averages differences within the sole task cluster, so p=1 and no task-population significance claim is possible; seed repetitions do not create independent tasks. Failed runs would stay in the task denominator and incomplete privacy pairs would be marked unavailable. Formal execution failed0 and excluded0.

Run: `PYTHONPATH=. python3 scripts/run_aamas_equal.py --config configs/experiment/aamas2027/e0_equal.json --output artifacts/aamas2027/E0_equal_capability/formal` (use a fresh output path for another execution).

Rebuild: same command with `--summarize-only`; no API needed. Raw episode and event JSONL are in formal/.
