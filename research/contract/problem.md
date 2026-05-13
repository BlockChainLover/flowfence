# Problem

- task:
  Build a runtime defense for text-first, tool-enabled multi-agent LLM systems that reduces unauthorized privacy leakage and contaminated-content propagation across messages, memory, shared workspace artifacts, tools, and final outputs.
- privacy-defense setting:
  Instrumented simulated multi-agent runtime with logged actions, machine-readable secret policies, and local replayable tools.
- threat model:
  In-scope attacks are prompt injection through tool outputs, shared-memory poisoning, shared-summary poisoning, shared-workspace poisoning, compromised low-trust agents, and memory-extraction-style querying. Out of scope are OS compromise, network compromise, raw model-weight theft, evaluator-label compromise, and multimodal channels in MVP.
- why this topic matters:
  In multi-agent systems, privacy failures propagate through internal channels that output-only evaluation misses. Shared memory and shared workspaces can amplify a single contamination event into broader cross-agent leakage and privilege escalation.
- non-goals:
  Proving formal security guarantees, supporting multimodal agents in MVP, claiming defense across all frameworks, or implementing the full proposed method before at least one baseline is reproducible.
