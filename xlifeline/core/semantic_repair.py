from __future__ import annotations
import os


class SemanticRepair:
    """
    Semantic reconstruction layer for partially corrupted memory.
    Supports OpenAI-compatible APIs or safe local fallback.
    """

    def __init__(self, provider: str = "local"):
        self.provider = provider

    def repair(self, text: str) -> dict:
        if not text:
            return {
                "repaired_text": "",
                "confidence": 0.0,
            }

        if self.provider == "openai" and os.getenv("OPENAI_API_KEY"):
            try:
                from openai import OpenAI

                client = OpenAI()

                prompt = f"""
The following AI memory log is partially corrupted.
Reconstruct missing sections while preserving meaning.

Memory:
{text}
"""

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                )

                repaired = response.choices[0].message.content

                return {
                    "repaired_text": repaired,
                    "confidence": 0.92,
                }

            except Exception:
                pass

        repaired = text.replace("  ", " ").strip()

        return {
            "repaired_text": repaired,
            "confidence": 0.75,
        }

    def repair_text(self, text: str) -> str:
        """
        Compatibility method used by service.py
        Returns only repaired text.
        """
        return self.repair(text)["repaired_text"]