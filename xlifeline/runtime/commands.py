from __future__ import annotations

from typing import Any

from xlifeline.core.continuity_engine import ContinuityEngine
from xlifeline.model.base import BaseModelAdapter
from xlifeline.runtime.metrics import format_integrity_summary, format_rebuild_summary
from xlifeline.runtime.session import RuntimeSession
from xlifeline.service import XLifeline


class RuntimeCommandProcessor:
    def __init__(
        self,
        service: XLifeline,
        model: BaseModelAdapter,
        continuity: ContinuityEngine,
        session: RuntimeSession,
    ) -> None:
        self.service = service
        self.model = model
        self.continuity = continuity
        self.session = session

    def help_text(self) -> str:
        return (
            "\nAvailable commands:\n"
            "/help                     Show this help\n"
            "/ask <prompt>             Ask the runtime a question\n"
            "/memory-status            Show current integrity state\n"
            "/corrupt-memory <0-1>     Simulate fragment loss\n"
            "/rebuild                  Rebuild current memory\n"
            "/continue <prompt>        Continue task from recovered state\n"
            "/demo-resurrection        Run built-in continuity demo\n"
            "/benchmark                Run simple corruption benchmark\n"
            "/reset                    Reset session\n"
            "/exit                     Exit runtime\n"
        )

    def execute(self, line: str) -> str:
        raw = line.strip()
        if not raw:
            return ""

        if not raw.startswith("/"):
            return "Commands must start with '/'. Try /help"

        parts = raw.split(maxsplit=1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        handlers = {
            "/help": self._cmd_help,
            "/ask": self._cmd_ask,
            "/memory-status": self._cmd_memory_status,
            "/corrupt-memory": self._cmd_corrupt_memory,
            "/rebuild": self._cmd_rebuild,
            "/continue": self._cmd_continue,
            "/demo-resurrection": self._cmd_demo_resurrection,
            "/benchmark": self._cmd_benchmark,
            "/reset": self._cmd_reset,
        }

        handler = handlers.get(cmd)
        if not handler:
            return f"Unknown command: {cmd}. Try /help"

        return handler(arg)

    def _persist_session(self) -> None:
        transcript = self.session.transcript()
        self.service.save_text(self.session.active_key, transcript, payload_name=self.session.active_key)

    def _cmd_help(self, _: str) -> str:
        return self.help_text()

    def _cmd_ask(self, arg: str) -> str:
        prompt = arg.strip()
        if not prompt:
            return "Usage: /ask <prompt>"

        context = self.session.transcript() or None
        reply = self.model.generate(prompt, context=context)

        self.session.append_user(prompt)
        self.session.append_assistant(reply)
        self._persist_session()

        return f"User: {prompt}\n\nAgent:\n{reply}"

    def _cmd_memory_status(self, _: str) -> str:
        if not self.session.messages:
            return "No session memory exists yet. Use /ask first."

        report = self.service.verify(self.session.active_key, lossy=self.session.lossy_mode)
        return format_integrity_summary(report)

    def _cmd_corrupt_memory(self, arg: str) -> str:
        if not self.session.messages:
            return "No session memory exists yet. Use /ask first."

        try:
            percent = float(arg.strip())
        except ValueError:
            return "Usage: /corrupt-memory <0-1>"

        lossy_manifest = self.service.simulate_loss(self.session.active_key, percent=percent, seed=42)
        self.session.lossy_mode = True

        destroyed = lossy_manifest.get("destroyed_indices", [])
        return (
            f"Memory corruption simulated.\n"
            f"Destroyed fragments: {len(destroyed)}\n"
            f"Destroyed indices: {destroyed}"
        )

    def _cmd_rebuild(self, _: str) -> str:
        if not self.session.messages:
            return "No session memory exists yet. Use /ask first."

        result = self.service.rebuild(self.session.active_key, lossy=self.session.lossy_mode, repair_text=True)
        return (
            format_rebuild_summary(result)
            + "\n\nRecovered text:\n"
            + (result.get("rebuilt_text", "") or "")
            + "\n\nSemantic repair output:\n"
            + (result.get("repaired_text", "") or "")
        )

    def _cmd_continue(self, arg: str) -> str:
        prompt = arg.strip()
        if not prompt:
            return "Usage: /continue <prompt>"

        if not self.session.messages:
            return "No session memory exists yet. Use /ask first."

        rebuild_result = self.service.rebuild(
            self.session.active_key,
            lossy=self.session.lossy_mode,
            repair_text=True,
        )

        continuity = self.continuity.prepare_context(rebuild_result, user_prompt=prompt)
        reply = self.model.generate(prompt, context=continuity["usable_context"])

        self.session.append_user(prompt)
        self.session.append_assistant(reply)
        self.session.lossy_mode = False
        self._persist_session()

        return (
            f"Continuity mode: {continuity['continuity_mode']}\n"
            f"Recovered integrity: {continuity['integrity_score']:.3f}\n\n"
            f"Agent:\n{reply}"
        )

    def _cmd_demo_resurrection(self, _: str) -> str:
        self.session.reset()

        out = []
        out.append(self._cmd_ask("Explain TCP/IP in 5 structured steps"))
        out.append(self._cmd_corrupt_memory("0.5"))
        out.append(self._cmd_memory_status(""))
        out.append(self._cmd_continue("Continue from step 3"))

        return "\n\n" + ("\n" + ("-" * 68) + "\n").join(out)

    def _cmd_benchmark(self, _: str) -> str:
        sample = "User: Explain TCP/IP in 5 structured steps\nAgent: 1. ... 2. ... 3. ... 4. ... 5. ..."
        rows: list[str] = ["| Loss % | Integrity | Status |", "|---:|---:|---|"]

        for p in (0.0, 0.25, 0.50, 0.75):
            key = f"benchmark-{int(p * 100)}"
            self.service.save_text(key, sample, payload_name=key)
            if p > 0:
                self.service.simulate_loss(key, percent=p, seed=42)
            result = self.service.rebuild(key, lossy=(p > 0), repair_text=True)
            report = result.get("integrity", {})
            rows.append(
                f"| {int(p * 100)} | {float(report.get('integrity_score', 0.0)):.2f} | {report.get('status', 'unknown')} |"
            )

        return "\n".join(rows)

    def _cmd_reset(self, _: str) -> str:
        self.session.reset()
        return "Session reset."