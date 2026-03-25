import argparse

from xlifeline import FragmentEngine, RebuildEngine


def main():

    parser = argparse.ArgumentParser(prog="xlifeline")

    sub = parser.add_subparsers(dest="cmd")

    frag = sub.add_parser("fragment")
    frag.add_argument("file")

    rebuild = sub.add_parser("rebuild")
    rebuild.add_argument("file")

    demo = sub.add_parser("demo")

    args = parser.parse_args()

    if args.cmd == "demo":
        from examples.resurrection_demo import main
        main()

    elif args.cmd == "fragment":

        with open(args.file, "rb") as f:
            data = f.read()

        engine = FragmentEngine()

        manifest = engine.fragment_bytes(data)

        print(f"Fragments created: {manifest['total_fragments']}")

    elif args.cmd == "rebuild":

        print("Rebuild command placeholder")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()