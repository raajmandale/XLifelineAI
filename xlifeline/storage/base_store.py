from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseStore(ABC):
    @abstractmethod
    def save_manifest(self, key: str, manifest: dict[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    def load_manifest(self, key: str, lossy: bool = False) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def save_lossy_manifest(self, key: str, manifest: dict[str, Any]) -> None:
        raise NotImplementedError
