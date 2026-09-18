# Shared-state publication/access

SHARED_STATE_MEDIATION: NOT_FEASIBLE with the pinned exposed state APIs and current generic adapters.

Actual read-after-write probes cover BaseMemory.update/stringification/retrieve_all, SharedMemory update/retrieve/retrieve_all, engine memory, environment.state/get_state and planner.current_progress/create_prompt. Clean state return values match in both defenses. The original state capabilities remain available in both arms.

In all six environment/arm fixtures, direct writes to SharedMemory.storage, engine.memory.storage, environment.state and planner.current_progress are visible on the next ordinary read/model prompt assembly without a release event. These are positive bypass observations, not an argument about needing to enumerate arbitrary trajectories. The public backing objects and attributes have no single benchmark-owned pre-publication interface. Wrapping update/get_memory_str alone cannot certify them.

A correctly attributed model gateway can remove the value at a later worker model ingress, but that does not undo shared publication, protect non-model consumers, or solve the demonstrated session identity problem. Direct mutable storage is therefore not reclassified as diagnostic/private just because one mocked model output is clean.

A complete design would need ownership-aware stores and explicit access/publication boundaries for both containers and planner/environment attributes. Retrofitting such a representation while preserving aliasing and capability semantics is a cross-cutting runtime design task, beyond the permitted bounded boundary audit. It is not hidden inside a wrapper class here. No state interface is removed, and no one-off handler hook is added. This conclusion is scoped to the current interface, not all future runtime implementations.
