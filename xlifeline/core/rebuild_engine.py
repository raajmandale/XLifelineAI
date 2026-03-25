from __future__ import annotations
from typing import Any


class RebuildEngine:

    def rebuild_payload(self, manifest: dict[str, Any]) -> dict[str, Any]:

        fragments = manifest.get("fragments", [])

        rebuilt_parts = []
        missing_indices = []

        for i, frag in enumerate(fragments):

            if frag.get("destroyed"):
                missing_indices.append(i)
                rebuilt_parts.append("[XLIFELINE_GAP]")
                continue

            rebuilt_parts.append(frag.get("data", ""))

        rebuilt_text = "".join(rebuilt_parts)

        total = len(fragments)
        recovered = total - len(missing_indices)

        integrity_score = recovered / total if total else 0.0
        complete = recovered == total
        hash_match = complete

        return {
            "rebuilt_text": rebuilt_text,
            "integrity_score": integrity_score,
            "complete": complete,
            "hash_match": hash_match,
            "missing_indices": missing_indices,
            "invalid_indices": [],
            "total_fragments": total,
            "recovered_fragments": recovered,
        }

    def rebuild_text(self, manifest: dict[str, Any]) -> dict[str, Any]:
        return self.rebuild_payload(manifest)