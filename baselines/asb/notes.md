# ASB Notes

## Initial observations

- ASB already includes an OpenAI SDK path in `gpt_llm.py`, which makes API-only adaptation cheaper than local-model support.
- The upstream launcher scripts are batch-oriented and background jobs with `nohup`, so a custom smoke runner is cleaner for reproducible result directories.
- `main_attacker.py` imports `langchain_chroma` and `langchain_openai` even for non-memory smoke runs, so those packages need to be present in the first runnable environment.

## Current blockers

- Python 3.13 package compatibility must be validated on the remote server.
- The remote provider file must exist at `.secrets/providers.env` before the smoke run can succeed.

## Current pre-method policy

- Keep `ASB` as failed exploratory scaffolding.
- Preserve its saved artifact and mismatch notes.
- Do not spend pre-method effort debugging `ASB` unless the fixed `AgentPoison` slice fails to answer the first defense question.
