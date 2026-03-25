from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from xlifeline import XLifeline
from xlifeline.storage.memory_store import MemoryStore


def main() -> None:
    memory = (
        "User: Analyze the Q1 financial dataset.\n"
        "Agent: Loading dataset.\n"
        "Agent: Running anomaly detection across revenue streams.\n"
        "Agent: Detecting unusual spike in region EU-West.\n"
        "Agent: Generating statistical summary.\n"
        "Agent: Preparing final insight report.\n"
    )

    xl = XLifeline(store=MemoryStore(), chunk_size=32)
    manifest = xl.save_text("demo-memory", memory, payload_name="agent_memory.txt")
    lossy = xl.simulate_loss("demo-memory", percent=0.40, seed=7)
    result = xl.rebuild("demo-memory", lossy=True)

    print("=" * 60)
    print("XLifelineAI — Corruption Demo")
    print("=" * 60)
    print(f"Fragments created: {manifest['total_fragments']}")
    print(f"Fragments destroyed: {len(lossy.get('destroyed_indices', []))}")
    print(f"Integrity status: {result['integrity']['status']}")
    print(f"Integrity score: {result['integrity']['integrity_score']}")
    print("\nRecovered text:\n")
    print(result.get("rebuilt_text") or "<binary payload>")
    print("\nSemantic repair output:\n")
    print(result.get("repaired_text") or "<no repair>")


if __name__ == "__main__":
    main()
