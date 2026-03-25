from __future__ import annotations

from xlifeline.core.continuity_engine import ContinuityEngine
from xlifeline.model.base import BaseModelAdapter
from xlifeline.model.mock_model import MockModelAdapter
from xlifeline.runtime.commands import RuntimeCommandProcessor
from xlifeline.runtime.session import RuntimeSession
from xlifeline.service import XLifeline


class XLifelineRuntimeApp:
    def __init__(
        self,
        service: XLifeline | None = None,
        model: BaseModelAdapter | None = None,
    ) -> None:
        self.service = service or XLifeline(chunk_size=32)
        self.model = model or MockModelAdapter()
        self.continuity = ContinuityEngine()
        self.session = RuntimeSession()
        self.commands = RuntimeCommandProcessor(
            service=self.service,
            model=self.model,
            continuity=self.continuity,
            session=self.session,
        )

    def banner(self) -> str:
        return (
            "\n"
            "====================================================================\n"
            "XLifelineAI Runtime — Local AI that survives memory loss\n"
            "====================================================================\n"
            "Type /help for commands.\n"
        )

    def run(self) -> None:
        print(self.banner())

        while True:
            try:
                line = input("xlifeline> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nExiting XLifelineAI Runtime.")
                break

            if not line:
                continue

            if line.lower() in {"/exit", "exit", "quit"}:
                print("Exiting XLifelineAI Runtime.")
                break

            output = self.commands.execute(line)
            if output:
                print(output)