from __future__ import annotations

from typing import Any


def integrity_report(rebuild_result: dict[str, Any]) -> dict[str, Any]:
    score = float(rebuild_result.get("integrity_score", 0.0))
    complete = bool(rebuild_result.get("complete", False))
    hash_match = bool(rebuild_result.get("hash_match", False))

    if complete and hash_match:
        status = "exact_recovery"
    elif score >= 0.85:
        status = "high_partial_recovery"
    elif score >= 0.50:
        status = "partial_recovery"
    else:
        status = "degraded_recovery"

    return {
        "status": status,
        "integrity_score": round(score, 4),
        "complete": complete,
        "hash_match": hash_match,
        "missing_indices": rebuild_result.get("missing_indices", []),
        "invalid_indices": rebuild_result.get("invalid_indices", []),
        "total_fragments": rebuild_result.get("total_fragments", 0),
        "recovered_fragments": rebuild_result.get("recovered_fragments", 0),
    }