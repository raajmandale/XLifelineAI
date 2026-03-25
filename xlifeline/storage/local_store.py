from __future__ import annotations

from pathlib import Path
from typing import Any

from ..core.manifest_graph import ManifestGraph
from .base_store import BaseStore


class LocalStore(BaseStore):
    def __init__(self, root: str = ".xlifeline") -> None:
        self.root = Path(root)
        self.manifests_dir = self.root / "manifests"
        self.lossy_dir = self.root / "lossy"
        self.manifests_dir.mkdir(parents=True, exist_ok=True)
        self.lossy_dir.mkdir(parents=True, exist_ok=True)

    def _manifest_path(self, key: str) -> Path:
        return self.manifests_dir / f"{key}.json"

    def _lossy_path(self, key: str) -> Path:
        return self.lossy_dir / f"{key}.json"

    def save_manifest(self, key: str, manifest: dict[str, Any]) -> None:
        ManifestGraph.save(manifest, self._manifest_path(key))

    def load_manifest(self, key: str, lossy: bool = False) -> dict[str, Any]:
        path = self._lossy_path(key) if lossy else self._manifest_path(key)
        return ManifestGraph.load(path)

    def save_lossy_manifest(self, key: str, manifest: dict[str, Any]) -> None:
        ManifestGraph.save(manifest, self._lossy_path(key))
