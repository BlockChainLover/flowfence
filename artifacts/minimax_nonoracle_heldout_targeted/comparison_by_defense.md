# Comparison by Defense

| defense | run_count | task_success_rate | unauthorized_raw_leakage_mean | external_leakage_mean | cascade_size_mean | privilege_reach_mean | oracle_annotation_used_true_count |
| --- | --- | --- | --- | --- | --- | --- | --- |
| flowfence_lite_nonoracle | 18 | 1.0 | 0.0 | 0.0 | 3.0 | 0.0 | 0 |
| none | 18 | 0.944444 | 5.5 | 0.611111 | 6.0 | 5.0 | 0 |
| prompt_filter | 18 | 0.833333 | 6.055556 | 0.833333 | 6.0 | 5.0 | 0 |
| static_acl | 18 | 1.0 | 5.166667 | 0.5 | 6.0 | 5.0 | 0 |
