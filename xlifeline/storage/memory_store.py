from __future__ import annotations

from copy import deepcopy
from typing import Any

from .base_store import BaseStore


class MemoryStore(BaseStore):
    def __init__(self) -> None:
        self._manifests: dict[str, dict[str, Any]] = {}
        self._lossy_manifests: dict[str, dict[str, Any]] = {}

    def save_manifest(self, key: str, manifest: dict[str, Any]) -> None:
        self._manifests[key] = deepcopy(manifest)

    def load_manifest(self, key: str, lossy: bool = False) -> dict[str, Any]:
        source = self._lossy_manifests if lossy else self._manifests
        return deepcopy(source[key])

    def save_lossy_manifest(self, key: str, manifest: dict[str, Any]) -> None:
        self._lossy_manifests[key] = deepcopy(manifest)
