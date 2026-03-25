from __future__ import annotations

from typing import Any

from .core.fragment_engine import FragmentEngine
from .core.integrity import integrity_report
from .core.manifest_graph import ManifestGraph
from .core.rebuild_engine import RebuildEngine
from .core.semantic_repair import SemanticRepair
from .storage.base_store import BaseStore
from .storage.local_store import LocalStore


class XLifeline:
    """
    High-level service interface for XLifelineAI.

    Handles:
    - fragmentation
    - manifest storage
    - simulated loss
    - rebuild operations
    - integrity verification
    - optional semantic repair
    """

    def __init__(self, store: BaseStore | None = None, chunk_size: int = 64) -> None:
        self.store = store or LocalStore()

        self.fragment_engine = FragmentEngine(chunk_size=chunk_size)
        self.rebuild_engine = RebuildEngine()
        self.semantic_repair = SemanticRepair()

    # -----------------------------
    # SAVE OPERATIONS
    # -----------------------------

    def save_bytes(self, key: str, payload: bytes, payload_name: str | None = None) -> dict[str, Any]:
        manifest = self.fragment_engine.fragment_bytes(
            payload, payload_name=payload_name or key
        )

        self.store.save_manifest(key, manifest)

        return manifest

    def save_text(self, key: str, text: str, payload_name: str | None = None) -> dict[str, Any]:
        manifest = self.fragment_engine.fragment_text(
            text, payload_name=payload_name or key
        )

        self.store.save_manifest(key, manifest)

        return manifest

    # -----------------------------
    # LOAD
    # -----------------------------

    def load_manifest(self, key: str, lossy: bool = False) -> dict[str, Any]:
        return self.store.load_manifest(key, lossy=lossy)

    # -----------------------------
    # VERIFY INTEGRITY
    # -----------------------------

    def verify(self, key: str, lossy: bool = False) -> dict[str, Any]:
        manifest = self.load_manifest(key, lossy=lossy)

        rebuild_result = self.rebuild_engine.rebuild_payload(manifest)

        return integrity_report(rebuild_result)

    # -----------------------------
    # SIMULATE DATA LOSS
    # -----------------------------

    def simulate_loss(self, key: str, percent: float, seed: int | None = 42) -> dict[str, Any]:
        manifest = self.load_manifest(key)

        lossy_manifest = ManifestGraph.create_lossy_copy(
            manifest,
            percent=percent,
            seed=seed,
        )

        self.store.save_lossy_manifest(key, lossy_manifest)

        return lossy_manifest

    # -----------------------------
    # REBUILD
    # -----------------------------

    def rebuild(
        self,
        key: str,
        lossy: bool = False,
        repair_text: bool = True,
    ) -> dict[str, Any]:

        manifest = self.load_manifest(key, lossy=lossy)

        rebuild_result = self.rebuild_engine.rebuild_payload(manifest)

        report = integrity_report(rebuild_result)

        result: dict[str, Any] = dict(rebuild_result)

        result["integrity"] = report

        if repair_text and rebuild_result.get("rebuilt_text"):
            repaired = self.semantic_repair.repair_text(rebuild_result["rebuilt_text"])
            result["repaired_text"] = repaired

        return result