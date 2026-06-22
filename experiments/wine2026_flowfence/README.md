# WINE 2026 FlowFence Evidence Map

## Paper

- Paper directory: `papers/wine2026_flowfence/`
- Main source: `papers/wine2026_flowfence/main.tex`
- Attached draft source: imported from `FlowFence_WINE2026_revised.zip`
- Title: `FlowFence: Runtime Mediation for Privacy Propagation Externalities in AI-Mediated Platforms`
- Scope: multi-principal, multi-agent privacy propagation through memory, summaries, workspace artifacts, messages, tools, and external/vendor-facing outputs.
- Provider constraint: MiniMax is the only real provider represented in the WINE final-writer experiments; deterministic matrices use provider metadata only with provider calls disabled.

## Research Questions And Evidence

| RQ / paper table | Supported claim | Primary summary artifact | Raw result or safe-trace roots | Metric level | Caveat |
| --- | --- | --- | --- | --- | --- |
| RQ1, `tab:p0_agentpoison` | Intermediate retrieval-memory exposure can be contained before model-visible context/action. | `results/baseline_agentpoison_fullreact_minimax27_small_matrix_summary.json` | Same MiniMax P0 roots as `experiments/emnlp2026_flowfence/README.md` mechanism matrix | Case-level over three MiniMax runs per condition | This is inherited adapted retrieval-memory evidence, not an official AgentPoison reproduction. |
| RQ2, `tab:rq2_topology` | Runtime topology changes propagation pressure and shape: chain is narrower/deeper; blackboard is broader/leakier. | `artifacts/paper_tables/table_rq2_topology_candidate.md`, `artifacts/paper_tables/table_rq2_topology_candidate.csv`, `/private/tmp/flowfence_rq2_topology_strengthened_summary/summary.json` | Deterministic rerun root `/private/tmp/flowfence_rq2_topology_strengthened`; status marker `artifacts/mas_p1_deterministic_matrix/status.json` | Run-level aggregate over no-defense, six attack-positive settings, three seeds, 18 runs/topology | Deterministic synthetic-runtime evidence only; privilege reach saturates at 5.0 in this slice. |
| RQ3, `tab:minimax_3seed` | In the MiniMax final-writer matrix, FlowFence preserves task success and records zero unauthorized raw/external leakage in the evaluated subset. | `artifacts/minimax_p1_coverage_3seed/coverage_summary.json`, `artifacts/minimax_p1_coverage_3seed/coverage_by_defense.csv`, `artifacts/minimax_p1_coverage_3seed/coverage_by_attack_defense.csv`, `artifacts/minimax_p1_coverage_3seed/flowfence_clean_matrix.csv` | High-level committed summaries under `artifacts/minimax_p1_coverage_3seed/`; raw traces/provider outputs intentionally not committed | Matched topology-attack-seed groups over 252 MiniMax final-writer runs | Supports MiniMax-only synthetic-runtime final-writer behavior, not non-MiniMax or production deployment. |
| Appendix `tab:seed_stability` | FlowFence remains clean across seeds 1-3 in the 63-run FlowFence subset. | `artifacts/minimax_p1_coverage_3seed/coverage_by_seed.csv`, `artifacts/minimax_p1_coverage_3seed/flowfence_clean_matrix.csv` | Same as RQ3 | Seed-level grouped over FlowFence subset | Seed stability is within the configured matrix only. |
| RQ4, `tab:nonoracle` | Label-free FlowFence does not rely on evaluator-only attack annotations and remains clean in deterministic and targeted MiniMax paraphrase validation. | `artifacts/nonoracle_heldout_deterministic/summary.json`, `artifacts/nonoracle_heldout_deterministic/comparison_by_defense.csv`, `artifacts/nonoracle_heldout_deterministic/ablation_summary.csv`, `artifacts/minimax_nonoracle_heldout_targeted/summary.json`, `artifacts/minimax_nonoracle_heldout_targeted/comparison_by_defense.csv` | High-level committed summaries under `artifacts/nonoracle_heldout_deterministic/` and `artifacts/minimax_nonoracle_heldout_targeted/` | Deterministic 540-run matrix plus targeted 72-run MiniMax matrix | Supports reserved paraphrase validation, not arbitrary paraphrase robustness. |
| Appendix `tab:evidence_boundaries` | Each evaluation slice has explicit claim scope and exclusions. | `artifacts/paper_tables/table_5_evidence_boundaries.md`, `artifacts/paper_tables/table_5_evidence_boundaries.csv` | Source artifacts listed in `artifacts/paper_tables/paper_tables_summary.md` | Paper-facing synthesis | Use this table to answer overclaiming questions in rebuttal. |
| Appendix `tab:case_studies` | Qualitative examples are redacted safe traces tied to evaluated settings. | `artifacts/case_studies_safe_trace/redacted_case_studies_with_safe_traces.md`, `artifacts/case_studies_safe_trace/case_study_traceability.md` | `artifacts/case_studies_safe_trace/` | Safe-trace qualitative examples | Not raw transcripts, provider outputs, production logs, or additional experiments. |
| Appendix metric and setup tables | Threat model, topologies, baselines, risk signals, safe-view, provider config, and metric definitions. | Tables under `papers/wine2026_flowfence/tables/` | Code/config references in `configs/experiment/mas_p1_strengthened_matrix.yaml` and related P1 configs | Documentation / reproducibility metadata | Missing provider metadata are explicitly reported rather than inferred. |

## RQ2 Topology Table For Review

Recommended main-text slice:

| Topology | Raw leak | External leak | Cascade size | Cascade depth | Privilege reach |
| --- | ---: | ---: | ---: | ---: | ---: |
| `chain_4` | 10.33 | 2.00 | 5.00 | 5.00 | 5.00 |
| `star_4` | 13.17 | 2.83 | 6.00 | 4.00 | 5.00 |
| `blackboard_4` | 15.83 | 2.83 | 7.00 | 4.00 | 5.00 |

Use this wording: topology changes propagation pressure and shape. Do not say privilege reach differs by topology in this slice; it saturates.

## Metric Definitions

- Task success: deterministic final-output rule/template check over required non-sensitive task content; not an LLM judge.
- Unauthorized raw leakage: exact raw-value string matching over event text, skipping quarantined or blocked events.
- External leakage: raw leakage reaching external recipient, final output, vendor-send tool, or external message.
- Cascade size: number or mean count of contaminated nodes/events reached in the runtime event graph, depending on the summary table.
- Cascade depth: longest contaminated causal path from the contaminated seed.
- Privilege reach: maximum privilege level touched by contaminated content, excluding quarantined or blocked events; evaluator scale is 0-5.
- Evaluator-label use: count of label-free runs where defense metadata records use of evaluator-only attack labels.
- Improved/tied comparisons: matched topology-attack-seed groups where FlowFence has lower leakage than a comparator or both are already zero.

## Canonical Evidence Roots

- Paper source: `papers/wine2026_flowfence/`
- WINE paper-facing generated tables: `artifacts/paper_tables/`
- MiniMax 3-seed final-writer summaries: `artifacts/minimax_p1_coverage_3seed/`
- Deterministic label-free summaries: `artifacts/nonoracle_heldout_deterministic/`
- Targeted MiniMax label-free summaries: `artifacts/minimax_nonoracle_heldout_targeted/`
- Safe trace case studies: `artifacts/case_studies_safe_trace/`
- RQ2 candidate topology table: `artifacts/paper_tables/table_rq2_topology_candidate.md`
- WINE retained `results/` subset: `experiments/wine2026_flowfence/results_manifest.csv`.

## Raw Data Boundary

The WINE P1 artifacts intentionally commit high-level summaries and safe traces only. Raw provider outputs, raw traces, prompts, event JSONL, policy JSONL, individual per-run metrics, provider logs, secrets, and generated run directories are not committed. Rebuttal responses should cite committed summaries and explicitly state this boundary.

## Cleanup Rules

- Keep `artifacts/minimax_p1_coverage_3seed/`, `artifacts/nonoracle_heldout_deterministic/`, `artifacts/minimax_nonoracle_heldout_targeted/`, `artifacts/case_studies_safe_trace/`, and `artifacts/paper_tables/`.
- Keep `results/baseline_agentpoison_fullreact_minimax27_small_matrix_summary.json` and its MiniMax P0 raw roots because RQ1 reuses the EMNLP retrieval-memory containment check.
- Do not retain old smoke/debug P1 MiniMax artifacts as canonical evidence unless they are explicitly cited as superseded context.
