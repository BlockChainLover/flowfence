# Second model candidates — no selection, no calls

Checked official documentation2026-09-18. All candidates are independent of the MiniMax primary family. Model names are API IDs, not promises of immutable weights; save returned model/version metadata later. Entitlements untested. No second-provider experiment configuration was added.

| Provider / identifier | Context and tools | API/sampling constraints | Integration/capability risk |
|---|---|---|---|
| DeepSeek / deepseek-flash |1M context, tools, thinking/nonthinking; currently V4.1-Flash |OpenAI-compatible endpoint https://api.deepseek.com; mode must be explicitly fixed, no verified deterministic seed guarantee |MARBLE LiteLLM1.52-era router may not recognize current ID; explicit compatible endpoint adapter and current parameter validation required. Preserve identical tool set, text-only modality and budgets. |
| DeepSeek / deepseek-v4-pro |1M context, tools, thinking/nonthinking; currently V4-Pro-0813 |Same endpoint; continued availability explicitly documented after2026-09-14 |Same routing/mode risks; lower provider concurrency limit. Do not interpret larger context as extra allowed context or add provider tools. |
| Moonshot / kimi-k3 |1M context, tool_choice auto/none/required |OpenAI-compatible https://api.moonshot.ai/v1; fixed temperature1,top_p.95,n1; reasoning_effort low/high/max; preserved reasoning history required |MARBLE hardcodes temperature0 and lacks reasoning-history controls; cannot silently drop arguments. Later approved model-specific profile required. Native swarm/vision features must stay unused. |

DeepSeek price per1M tokens: Flash uncached input$0.15–0.30/output$0.60–1.20; Pro$0.66–1.32/$1.98–3.96 (off-peak to peak). Sources: [official pricing](https://api-docs.deepseek.com/quick_start/pricing/?push_animated=1&show_loading=0&theme=light&webview_progress_bar=1), [availability/version notes](https://api-docs.deepseek.com/updates/), [tool API](https://api-docs.deepseek.com/guides/tool_calls/). No seeds or sampling ranges inferred where not verified. Further parameter contract review required before candidate selection.

Kimi source: [official parameter reference](https://platform.kimi.ai/docs/api/models-overview), [K3 guide](https://platform.kimi.ai/docs/guide/kimi-k3-quickstart). Current Kimi dollar rate not reliably extracted from official pricing page; leave unavailable. Primary MiniMax current rate also unverified, so numeric relative-cost ratios are not claimed. Compare later using the same token basket and verified prices.

Kimi2.6 considered but not a recommended viable direct route: official docs say forced required tool_choice unsupported, whereas MARBLE communication requires it. Do not weaken that agent capability for provider compatibility.

Budget parity requires fixed observable tools, maximum context admitted and action budget in both defense arms. Different model sampling behavior is reported, not mislabeled independent seeds. Choosing a final family/model remains a human decision.
