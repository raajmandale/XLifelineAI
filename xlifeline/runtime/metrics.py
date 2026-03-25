from __future__ import annotations

from typing import Any


def format_integrity_summary(report: dict[str, Any]) -> str:
    status = report.get("status", "unknown")
    score = float(report.get("integrity_score", 0.0))
    recovered = report.get("recovered_fragments", 0)
    total = report.get("total_fragments", 0)

    return (
        f"Integrity status: {status}\n"
        f"Integrity score: {score:.3f}\n"
        f"Recovered fragments: {recovered}/{total}"
    )


def format_rebuild_summary(result: dict[str, Any]) -> str:
    integrity = result.get("integrity", {}) or {}
    status = integrity.get("status", "unknown")
    score = float(integrity.get("integrity_score", 0.0))
    missing = result.get("missing_indices", []) or []

    return (
        f"Rebuild status: {status}\n"
        f"Integrity score: {score:.3f}\n"
        f"Missing indices: {missing}"
    )