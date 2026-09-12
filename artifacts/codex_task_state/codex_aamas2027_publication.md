# AAMAS results publication

- Goal: publish the completed experiment evidence to BlockChainLover/flowfence and supply a GPT review prompt.
- Branch: codex/aamas2027-experiment-extension; PR base codex/wine2026-rebuttal-noapi to isolate the AAMAS increment.
- Completed work: selected existing package-allowlisted safe records and reports for version control; added review prompt. No experiment reruns or result changes.
- Changed files: artifacts/aamas2027 reports and formal/pilot safe records, FINAL_DELIVERY_VALIDATION.json, GPT_REVIEW_PROMPT.md, this state file, publication entry in research/logs/progress.md.
- Validation commands: existing validate_safe_artifacts over package allowlist; targeted pytest tests/test_aamas_*.py; git diff --cached --check; remote branch SHA verification after push.
- Known limitations: public repository; private full trajectories and credentials remain excluded. Experiment MANIFEST records the original packaging state and source SHA ab30af9, not the later publication commit. Existing unrelated WINE working-tree changes are preserved.
- Resume instructions: review the AAMAS PR using artifacts/aamas2027/GPT_REVIEW_PROMPT.md. Do not merge or rerun paid experiments as part of publication.
