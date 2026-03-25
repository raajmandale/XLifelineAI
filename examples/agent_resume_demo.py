from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import time

from xlifeline import XLifeline
from xlifeline.storage.memory_store import MemoryStore


def slow_print(text: str, delay: float = 0.01) -> None:
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()


def main() -> None:
    memory = (
        "User: Analyze the financial dataset from Q1.\n"
        "Agent: Loading dataset...\n"
        "Agent: Running anomaly detection across revenue streams.\n"
        "Agent: Detecting unusual spike in region EU-West.\n"
        "Agent: Generating statistical summary.\n"
        "Agent: Preparing final insight report.\n"
    )

    xl = XLifeline(store=MemoryStore(), chunk_size=28)
    manifest = xl.save_text("agent-run", memory)
    lossy = xl.simulate_loss("agent-run", percent=0.45, seed=11)
    result = xl.rebuild("agent-run", lossy=True)

    print("\n" + "=" * 60)
    print("XLifelineAI — Agent Resume Demo")
    print("=" * 60)
    print(f"Fragments created: {manifest['total_fragments']}")
    print(f"Fragments destroyed: {len(lossy.get('destroyed_indices', []))}")
    print(f"Recovered semantic context: {round(result['integrity']['integrity_score'] * 100)}%")

    print("\nRecovered Memory:\n")
    print(result.get("repaired_text") or result.get("rebuilt_text") or "")

    print("\nAgent Resume Simulation:\n")
    slow_print("Agent: Context restored.")
    slow_print("Agent: Continuing anomaly detection...")
    slow_print("Agent: Generating final insight report.")
    slow_print("✔ AI task completed successfully.")
    slow_print("XLifelineAI: memory survived destruction.")


if __name__ == "__main__":
    main()
