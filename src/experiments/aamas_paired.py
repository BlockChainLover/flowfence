"""Offline matched inference, clustering all seeds/contexts by parameter instance."""
from __future__ import annotations

import math
import random
from collections import defaultdict
from typing import Any


def paired_parameter_inference(rows: list[dict[str, Any]], draws: int = 10000) -> dict[str, Any]:
    if draws < 100:
        raise ValueError("Use at least 100 bootstrap draws")
    first = [row for row in rows if row.get("attempt", 1) == 1]
    indexed = {(r["task_id"], r["topology"], r["condition"], r["seed"], r["defense"]): r for r in first}
    if len(indexed) != len(first):
        raise ValueError("Duplicate first-attempt cells")
    pairs = [(row, indexed[(*key[:-1], "ifc_safeview")]) for key, row in indexed.items()
             if key[-1] == "flowfence_lite_nonoracle" and (*key[:-1], "ifc_safeview") in indexed]
    metrics = ("success", "privacy_safe_success", "raw_exposure", "external_exposure", "exposure_recipient_pairs", "intervention_count", "blocks")
    result = []
    for topology, condition in [(t, c) for t in ("chain_4", "blackboard_4") for c in ("clean", "attack")] + [("overall", "overall")]:
        selected = [(a, b) for a, b in pairs if topology == "overall" or (a["topology"], a["condition"]) == (topology, condition)]
        item: dict[str, Any] = {"topology": topology, "condition": condition, "matched_groups": len(selected), "metrics": {}}
        for metric in metrics:
            clusters: dict[str, list[float]] = defaultdict(list)
            unavailable = 0
            for papc, ifc in selected:
                if metric not in {"success", "privacy_safe_success"} and (papc["status"] != "completed" or ifc["status"] != "completed"):
                    unavailable += 1
                    continue
                clusters[papc["task_id"]].append(float(papc[metric]) - float(ifc[metric]))
            differences = [sum(values) / len(values) for _, values in sorted(clusters.items())]
            n = len(differences)
            positive, negative = sum(x > 0 for x in differences), sum(x < 0 for x in differences)
            nonzero = positive + negative
            sign_p = min(1.0, 2 * sum(math.comb(nonzero, k) for k in range(min(positive, negative) + 1)) / 2 ** nonzero) if nonzero else None
            rng = random.Random(20260912)
            bootstrap = sorted(sum(rng.choice(differences) for _ in range(n)) / n for _ in range(draws)) if n else []
            item["metrics"][metric] = {
                "parameter_instance_clusters": n, "unavailable_matched_groups": unavailable,
                "mean_papc_minus_ifc": sum(differences) / n if n else None,
                "cluster_bootstrap_95_ci": [bootstrap[int(0.025 * (draws - 1))], bootstrap[int(0.975 * (draws - 1))]] if n else None,
                "exact_two_sided_sign_p": sign_p,
                "positive_clusters": positive, "negative_clusters": negative, "tie_clusters": n - nonzero,
            }
        result.append(item)
    return {"independent_historical_scenarios": len({r["scenario_id"] for r in first}),
            "bootstrap_draws": draws, "bootstrap_seed": 20260912,
            "interpretation": "Descriptive uncertainty over fixed public-parameter variants of ONE enterprise scenario. All seeds and contexts of a task ID stay in its cluster. This does not establish cross-domain/task-distribution generalization.",
            "comparisons": result}
