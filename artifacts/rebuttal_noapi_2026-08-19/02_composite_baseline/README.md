# Experiment B - Strong Defense-in-Depth Baseline

`acl_content_runtime` applies the existing Static ACL condition first, then the existing direct prompt-filter surface rule before runtime transitions and again on external/final candidates. Matches block; there is no safe-view rewrite. Policy records explicitly set `papc_features_used=false`.

New runs: 90/90; failures: 0. Reference schema-refresh runs: 180.
