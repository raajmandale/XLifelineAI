from xlifeline.core.fragment_engine import FragmentEngine
from xlifeline.core.rebuild_engine import RebuildEngine
from xlifeline.storage.memory_store import MemoryStore
from xlifeline.adapters.agent_guard import AgentMemoryGuard

fragment = FragmentEngine()
rebuild = RebuildEngine()
store = MemoryStore()

guard = AgentMemoryGuard(fragment, rebuild, store)

memory = """
User: analyze dataset
Agent: running anomaly detection
Agent: preparing insights
"""

manifest = guard.write(memory)

# simulate fragment loss
store.delete_random(0.4)

recovered = guard.read(manifest)

print("\nRecovered Memory:\n")

print(recovered)