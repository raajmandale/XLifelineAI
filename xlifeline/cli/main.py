from __future__ import annotations

import argparse

from xlifeline.runtime.app import XLifelineRuntimeApp


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="xlifeline",
        description="XLifelineAI Runtime — Local AI that survives memory loss",
    )

    sub = parser.add_subparsers(dest="command")

    sub.add_parser("chat", help="Start interactive runtime chat")
    sub.add_parser("demo", help="Run the built-in resurrection demo")
    sub.add_parser("benchmark", help="Run the benchmark table")

    args = parser.parse_args()

    app = XLifelineRuntimeApp()

    if args.command == "demo":
        print(app.banner())
        print(app.commands.execute("/demo-resurrection"))
        return

    if args.command == "benchmark":
        print(app.banner())
        print(app.commands.execute("/benchmark"))
        return

    # default: interactive chat
    app.run()


if __name__ == "__main__":
    main()