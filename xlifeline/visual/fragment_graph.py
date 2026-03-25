def draw_fragment_graph(total: int, missing: list[int]) -> None:
    print("\nFragment Graph\n")

    for i in range(total):
        symbol = "X" if i in missing else "●"
        print(f"[{i:02}] {symbol}", end="  ")

        if (i + 1) % 8 == 0:
            print()

    print("\n")
    print("● = alive fragment")
    print("X = destroyed fragment")