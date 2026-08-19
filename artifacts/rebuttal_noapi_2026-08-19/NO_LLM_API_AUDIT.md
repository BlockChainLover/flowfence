# No LLM API Audit

Experiments:
- Experiment A
- Experiment B

Provider calls expected: 0
Provider calls observed: 0

Verification:
- Every matrix config sets `agent_backend: scripted_deterministic`, `provider_calls_enabled: false`, and `no_llm_api_required: true`.
- `sweep_mas.py` rejects `no_llm_api_required=true` with provider calls enabled before constructing a provider client.
- Remote commands did not pass `--allow-provider-calls`; provider credential variables were removed from the experiment process environment.
- Every per-run metric records `provider_call_count=0`; aggregate A count=0 and aggregate B/reference count=0.
- Every new run records `oracle_annotation_use_count=0`; aggregate A count=0 and aggregate B/reference count=0.
- Importing the MiniMax client module does not initialize a client or make a request. The provider branch is unreachable when `provider_calls_enabled=false`.
- `environment/provider_network_log_search.txt` is empty after searching experiment logs for MiniMax endpoint, chat-completion, HTTP-request, and provider-request markers.
