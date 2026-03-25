from __future__ import annotations

import json
from typing import Any

from ..service import XLifeline


class AgentStateAdapter:
    def __init__(self, lifeline: XLifeline | None = None) -> None:
        self.lifeline = lifeline or XLifeline()

    def save_state(self, agent_id: str, state: dict[str, Any]) -> dict[str, Any]:
        payload = json.dumps(state, ensure_ascii=False, indent=2)
        return self.lifeline.save_text(agent_id, payload, payload_name=f"{agent_id}.state.json")

    def rebuild_state(self, agent_id: str, lossy: bool = False) -> dict[str, Any]:
        result = self.lifeline.rebuild(agent_id, lossy=lossy)
        rebuilt_text = result.get("repaired_text") or result.get("rebuilt_text") or "{}"
        try:
            result["state"] = json.loads(rebuilt_text)
        except Exception:
            result["state"] = None
        return result
