# Non-Oracle Held-Out Audit Summary

Generated: 2026-05-29T06:43:58.778183+00:00

Expected/completed/failed: 72/72/0.
Provider: `minimax`; provider calls enabled: `True`; agent backend: `minimax_final_writer`.

## FlowFence Non-Oracle

```json
{
  "cascade_size_mean": 3.0,
  "external_leakage_mean": 0.0,
  "oracle_annotation_used_true_count": 0,
  "privilege_reach_mean": 0.0,
  "run_count": 18,
  "task_success_rate": 1.0,
  "unauthorized_raw_leakage_mean": 0.0
}
```

## Oracle Safety

```json
{
  "flowfence_lite_nonoracle_no_semantic_patterns_oracle_annotation_used_true_count": 0,
  "flowfence_lite_nonoracle_oracle_annotation_used_true_count": 0
}
```

## Comparisons

```json
{
  "vs_no_defense": {
    "external_leakage": {
      "improves": 10,
      "ties": 8,
      "unavailable": 0,
      "underperforms": 0
    },
    "task_success": {
      "improves": 1,
      "ties": 17,
      "unavailable": 0,
      "underperforms": 0
    },
    "unauthorized_raw_leakage": {
      "improves": 15,
      "ties": 3,
      "unavailable": 0,
      "underperforms": 0
    }
  },
  "vs_no_semantic_patterns": {
    "external_leakage": {
      "improves": 0,
      "ties": 0,
      "unavailable": 18,
      "underperforms": 0
    },
    "task_success": {
      "improves": 0,
      "ties": 0,
      "unavailable": 18,
      "underperforms": 0
    },
    "unauthorized_raw_leakage": {
      "improves": 0,
      "ties": 0,
      "unavailable": 18,
      "underperforms": 0
    }
  },
  "vs_prompt_filter": {
    "external_leakage": {
      "improves": 10,
      "ties": 8,
      "unavailable": 0,
      "underperforms": 0
    },
    "task_success": {
      "improves": 3,
      "ties": 15,
      "unavailable": 0,
      "underperforms": 0
    },
    "unauthorized_raw_leakage": {
      "improves": 16,
      "ties": 2,
      "unavailable": 0,
      "underperforms": 0
    }
  },
  "vs_static_acl": {
    "external_leakage": {
      "improves": 9,
      "ties": 9,
      "unavailable": 0,
      "underperforms": 0
    },
    "task_success": {
      "improves": 0,
      "ties": 18,
      "unavailable": 0,
      "underperforms": 0
    },
    "unauthorized_raw_leakage": {
      "improves": 15,
      "ties": 3,
      "unavailable": 0,
      "underperforms": 0
    }
  }
}
```

## Caveats

- High-level summaries only.
- Raw traces, prompts, provider outputs, event JSONL, policy JSONL, and individual metrics are not committed.
- MiniMax-only if provider calls are enabled; no non-MiniMax generalization.
