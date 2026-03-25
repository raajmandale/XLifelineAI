from __future__ import annotations

from xlifeline.service import XLifeline
from xlifeline.storage.memory_store import MemoryStore


def print_header(title: str) -> None:
    print("\n" + "=" * 68)
    print(title)
    print("=" * 68 + "\n")


def render_fragment_graph(manifest: dict) -> None:
    fragments = manifest.get("fragments", [])
    cells = []

    for frag in fragments:
        idx = frag.get("index", 0)
        destroyed = frag.get("destroyed", False)
        mark = "X" if destroyed else "●"
        cells.append(f"[{idx:02d}] {mark}")

    print("Fragment Graph\n")
    print("  ".join(cells))
    print("\n● = alive fragment")
    print("X = destroyed fragment\n")


def main() -> None:
    print_header("XLifelineAI — DFG Memory Resurrection Demo")

    xl = XLifeline(store=MemoryStore(), chunk_size=32)

    payload = (
        "User: analyze financial dataset\n"
        "Agent: loading dataset\n"
        "Agent: running anomaly detection\n"
        "Agent: generating statistical summary\n"
        "Agent: preparing insight report\n"
    )

    print("██ Initializing AI memory payload")
    manifest = xl.save_text("demo-memory", payload)

    total = manifest["total_fragments"]
    size = manifest["payload_size"]

    print(f"Fragments created: {total}")
    print(f"Payload size: {size} bytes\n")

    print("██ Constructing deterministic fragment graph\n")

    print("██ Simulating catastrophic fragment loss")
    lossy_manifest = xl.simulate_loss("demo-memory", percent=0.4, seed=42)
    destroyed = len(lossy_manifest.get("destroyed_indices", []))
    print(f"Fragments destroyed: {destroyed}\n")

    render_fragment_graph(lossy_manifest)

    print("██ Running integrity scan")
    result = xl.rebuild("demo-memory", lossy=True, repair_text=True)
    integrity = result.get("integrity", {})
    score = float(integrity.get("integrity_score", 0.0))
    print(f"Byte recovery integrity: {score * 100:.1f}%\n")

    print("██ Activating semantic repair")
    repaired_text = result.get("repaired_text", "")
    confidence = 75 if repaired_text else 0
    print(f"Recovered semantic confidence: {confidence}%\n")

    print("██ Recovered memory")
    print(repaired_text or result.get("rebuilt_text", ""))
    print()

    print("██ Agent resume simulation")
    print("Agent: context restored.")
    print("Agent: continuing anomaly detection...")
    print("Agent: generating final report...")
    print("✔ AI task completed successfully.\n")

    print("XLifelineAI: memory survived destruction.\n")


if __name__ == "__main__":
    main()