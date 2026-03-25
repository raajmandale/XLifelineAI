from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any


class ManifestGraph:
    @staticmethod
    def save(manifest: dict[str, Any], path: str | Path) -> None:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    @staticmethod
    def load(path: str | Path) -> dict[str, Any]:
        return json.loads(Path(path).read_text(encoding="utf-8"))

    @staticmethod
    def create_lossy_copy(
        manifest: dict[str, Any],
        percent: float,
        seed: int | None = None
    ) -> dict[str, Any]:
        if not 0 <= percent < 1:
            raise ValueError("percent must be in [0, 1)")

        fragments = list(manifest.get("fragments", []))
        total = len(fragments)
        destroy_count = int(total * percent)

        if seed is not None:
            random.seed(seed)

        destroy_indices = (
            set(random.sample(range(total), destroy_count))
            if destroy_count else set()
        )

        lossy_fragments = []
        for frag in fragments:
            new_frag = dict(frag)
            frag_index = new_frag.get("index")

            if frag_index in destroy_indices:
                new_frag["destroyed"] = True
            else:
                new_frag["destroyed"] = False

            lossy_fragments.append(new_frag)

        lossy = dict(manifest)
        lossy["fragments"] = lossy_fragments
        lossy["destroyed_indices"] = sorted(destroy_indices)
        lossy["loss_percent"] = percent

        return lossy