from __future__ import annotations

import json
from typing import Any

from ..service import XLifeline


class ChatMemoryAdapter:
    def __init__(self, lifeline: XLifeline | None = None) -> None:
        self.lifeline = lifeline or XLifeline()

    def save_messages(self, session_id: str, messages: list[dict[str, Any]]) -> dict[str, Any]:
        payload = json.dumps(messages, ensure_ascii=False, indent=2)
        return self.lifeline.save_text(session_id, payload, payload_name=f"{session_id}.chat.json")

    def rebuild_messages(self, session_id: str, lossy: bool = False) -> dict[str, Any]:
        result = self.lifeline.rebuild(session_id, lossy=lossy)
        rebuilt_text = result.get("repaired_text") or result.get("rebuilt_text") or "[]"
        try:
            result["messages"] = json.loads(rebuilt_text)
        except Exception:
            result["messages"] = None
        return result
