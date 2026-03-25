from __future__ import annotations

from typing import Any


class ContinuityEngine:
    """
    Turns rebuild results into usable runtime context.

    Modes:
    - exact: no loss
    - patched: loss occurred but semantic repair produced usable text
    - degraded: loss remains visible in context
    """

    GAP_TOKEN = "[XLIFELINE_GAP]"

    def prepare_context(
        self,
        rebuild_result: dict[str, Any],
        user_prompt: str | None = None,
    ) -> dict[str, Any]:
        rebuilt_text = rebuild_result.get("rebuilt_text", "") or ""
        repaired_text = rebuild_result.get("repaired_text", "") or ""
        integrity = rebuild_result.get("integrity", {}) or {}

        integrity_score = float(integrity.get("integrity_score", 0.0))
        missing_indices = rebuild_result.get("missing_indices", []) or []

        if integrity_score == 1.0 and not missing_indices:
            mode = "exact"
            usable_context = rebuilt_text
        elif repaired_text and self.GAP_TOKEN not in repaired_text:
            mode = "patched"
            usable_context = repaired_text
        else:
            mode = "degraded"
            usable_context = rebuilt_text or repaired_text

        if user_prompt:
            prompt_context = (
                f"Recovered continuity mode: {mode}\n"
                f"Recovered context:\n{usable_context}\n\n"
                f"User follow-up:\n{user_prompt}"
            )
        else:
            prompt_context = usable_context

        return {
            "continuity_mode": mode,
            "usable_context": usable_context,
            "prompt_context": prompt_context,
            "integrity_score": integrity_score,
        }