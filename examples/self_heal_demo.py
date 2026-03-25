from xlifeline.core.self_heal import SelfHealingWatcher
from xlifeline.core.integrity import IntegrityEngine
from xlifeline.core.rebuild_engine import RebuildEngine
from xlifeline.storage.memory_store import MemoryStore

integrity = IntegrityEngine()
rebuild = RebuildEngine()
store = MemoryStore()

watcher = SelfHealingWatcher(integrity, rebuild, store)

watcher.watch(manifest)