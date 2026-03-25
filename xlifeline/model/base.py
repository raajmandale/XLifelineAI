from __future__ import annotations

from abc import ABC, abstractmethod


class BaseModelAdapter(ABC):
    """
    Minimal model adapter interface.
    """

    @abstractmethod
    def generate(self, prompt: str, context: str | None = None) -> str:
        raise NotImplementedError