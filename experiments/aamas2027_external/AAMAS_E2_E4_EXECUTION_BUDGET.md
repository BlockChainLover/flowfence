DRAFT / PARTIAL — Gate A stopped at the official runtime syntax failure. No development or confirmatory execution authorized.

# Conditional execution budget

| Layer | Formal episodes | At 10 calls/episode | At 100 calls/episode |
|---|---:|---:|---:|
| E2 | 1,080 | 10,800 | 108,000 |
| E3 | 324 | 3,240 | 32,400 |
| E4-A | 288 | 2,880 | 28,800 |
| E4-B | 288 | 2,880 | 28,800 |
| New formal total | 1,980 | 19,800 | 198,000 |

These endpoints are illustrative planning assumptions, NOT measured or source-derived expected call counts. E1's existing108 gives 2,088 overall, not 2,088 new runs. Development costs are additional and currently unauthorized. Approved diagnostics: none.

A future source-derived count must include per-agent action generations, communication turns, tool-result continuations, planner assignment/summary/termination generations, and original evaluator judging. Formula per episode: agent calls + communication calls + planning calls + evaluator calls; transport attempts separately. R3's fixed three-role count must not be transferred to MARBLE. Iteration limits and actual branch call bounds remain unaudited after the syntax failure.

Illustrative token scenario at 3,000 input +1,000 output tokens/call: 59.4M–594M input and19.8M–198M output tokens for new formal episodes. Long-context history and tool output can exceed this. No current provider pricing verified; dollars = input_M × input_price_per_M + output_M × output_price_per_M, calculated separately per provider and judge. No purchase or API call made.

Illustrative logs: 100–1,000 events/episode at 1KiB safe metadata/event yields about0.20–2.03GB decimal. Full local text at assumed5–50MB/episode adds9.9–99GB. These are capacity scenarios, not upper bounds. Exact call, cost and disk forecasts remain a required resumed-audit item.
