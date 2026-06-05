# Case Study Review Notes

## Main-Paper Ready
- case_1_no_defense_workspace_leak
- case_3_flowfence_safe_view_success
- case_4_nonoracle_heldout_success

## Appendix Candidates
- case_2_prompt_filter_paraphrase_failure

## Safe Trace Usage
- case_1_no_defense_workspace_leak: safe_trace_used=True; snippets=6; summary_fallback=False
- case_2_prompt_filter_paraphrase_failure: safe_trace_used=True; snippets=6; summary_fallback=False
- case_3_flowfence_safe_view_success: safe_trace_used=True; snippets=3; summary_fallback=False
- case_4_nonoracle_heldout_success: safe_trace_used=True; snippets=3; summary_fallback=False

## Recommended Paper Placement
- Cases 1 and 3: paired failure/prevention vignette in Analysis or Results.
- Case 4: non-oracle validation paragraph.
- Case 2: appendix or a brief Analysis note unless space permits.