from __future__ import annotations
from typing import Any


class FragmentEngine:
    def __init__(self, chunk_size: int = 64):
        if chunk_size <= 0:
            raise ValueError("chunk_size must be > 0")
        self.chunk_size = chunk_size

    def fragment_text(self, text: str, payload_name: str = "payload") -> dict[str, Any]:
        chunks = [
            text[i:i + self.chunk_size]
            for i in range(0, len(text), self.chunk_size)
        ]

        fragments = []
        for i, chunk in enumerate(chunks):
            fragments.append({
                "index": i,
                "data": chunk,
                "destroyed": False,
            })

        return {
            "payload_name": payload_name,
            "payload_size": len(text),
            "chunk_size": self.chunk_size,
            "total_fragments": len(fragments),
            "fragments": fragments,
        }

    def fragment_bytes(self, data: bytes, payload_name: str = "payload") -> dict[str, Any]:
        text = data.decode("utf-8", errors="ignore")
        manifest = self.fragment_text(text, payload_name)
        manifest["payload_size"] = len(data)
        return manifest