# S1 clustering and balanced selection constraints — version 1

Defined before final eligibility or ID selection. These keys describe dependence; they do not assert independent questions.

BIRD: database identity plus source difficulty/category where present. Development/confirmatory records disjoint by ID; exactly20 confirmatory and3 development. Confirmatory maximum2 per database; seek maximum database coverage. Database overlap across splits is permitted and reported (only11 DBs); no claim of independent DB environments.

TAT-QA: source table/context UID. No context can occur in both development and confirmatory. At most1 selected question per context across all23 selections. A table is not necessarily a unique company/report; preserve source metadata and report that limitation.

HotpotQA: source bridge/comparison type, exact Unicode title identity, and sorted title-set context signature. Report shared-title frequencies, exact context duplicates and connected components of the title-overlap graph; no invented semantic entity resolver. Select23 records with pairwise disjoint supplied-title sets across development/confirmatory; confirmatory must include both bridge and comparison, at least5 of each. Questions are still not assumed independent merely because titles do not match.

Balance feasibility is a constraint problem over eligible (task,type) pairs:20 per family,15 each P1/P2/P3/P4, one type per question, ≥3 reserved development tasks per family respecting above clusters. Use no model/defense outcomes. A witness is an existence proof, not final selection. Until prerequisites are verified, do not emit selected IDs or a purported final assignment. If feasible and all user prerequisites pass, write and Git-record the deterministic selection algorithm before it emits final IDs. Use lexicographic source IDs and source-only cluster metadata for all tie-breaking; no favorable-result seed search.
