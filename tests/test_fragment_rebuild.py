from xlifeline.service import XLifeline
from xlifeline.storage.memory_store import MemoryStore


def test_exact_fragment_rebuild_roundtrip() -> None:
    xl = XLifeline(store=MemoryStore(), chunk_size=10)

    text = "XLifelineAI makes AI memory resilient."
    xl.save_text("session-1", text)

    result = xl.rebuild("session-1")

    assert result["integrity"]["status"] == "exact_recovery"
    assert result["integrity"]["integrity_score"] == 1.0
    assert result["rebuilt_text"] == text


def test_partial_recovery_marks_gaps() -> None:
    xl = XLifeline(store=MemoryStore(), chunk_size=8)

    xl.save_text("session-2", "User: hello\nAgent: hi there\n")
    xl.simulate_loss("session-2", percent=0.4, seed=1)

    result = xl.rebuild("session-2", lossy=True)

    assert result["integrity"]["integrity_score"] < 1.0
    assert "[XLIFELINE_GAP]" in result["rebuilt_text"]