#!/usr/bin/env python3
def print_gugudan(start: int = 1, end: int = 9) -> None:
    """Print multiplication tables (구구단) from start to end inclusive."""
    for i in range(start, end + 1):
        for j in range(1, 10):
            print(f"{i} x {j} = {i * j:2}", end="\t")
        print()

if __name__ == "__main__":
    print_gugudan()