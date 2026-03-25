from __future__ import annotations

from .base import BaseModelAdapter


class MockModelAdapter(BaseModelAdapter):
    """
    Deterministic local fallback model.

    This is intentionally simple and reliable:
    - no network dependency
    - stable demos
    - stable tests
    """

    def generate(self, prompt: str, context: str | None = None) -> str:
        prompt_l = prompt.lower().strip()
        context_l = (context or "").lower()

        # Signature demo path
        if "tcp/ip" in prompt_l and "5" in prompt_l:
            return (
                "1. Devices create data at the application layer.\n"
                "2. TCP breaks data into ordered, reliable segments.\n"
                "3. IP wraps segments into packets and routes them across networks.\n"
                "4. Routers forward packets toward the destination host.\n"
                "5. The receiver reassembles data and delivers it to the application."
            )

        if "continue" in prompt_l and "tcp/ip" in context_l:
            return (
                "3. IP wraps segments into packets and routes them across networks.\n"
                "4. Routers forward packets toward the destination host.\n"
                "5. The receiver reassembles data and delivers it to the application."
            )

        if "quantum basics" in prompt_l:
            return (
                "Quantum basics:\n"
                "1. Qubits can represent more than one state.\n"
                "2. Superposition enables probabilistic state combinations.\n"
                "3. Entanglement creates correlated outcomes across qubits.\n"
                "4. Measurement collapses the state.\n"
                "5. Quantum algorithms exploit these properties for specific problems."
            )

        if "continue" in prompt_l and context:
            return (
                "Using reconstructed context, continuing the task from the last stable point.\n"
                "Recovered context remains partially usable and execution can proceed."
            )

        if context:
            return (
                "Using available context, I can continue from the recovered memory state.\n"
                f"Prompt received: {prompt}"
            )

        return f"Mock response: {prompt}"