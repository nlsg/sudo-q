from pathlib import Path
from sudoq import Grid
from sudoq.solvers import StrategicSolver


def validate_puzzle_files():
    puzzle_files = Path("tests/assets/samples").glob("*.csv")
    for file in puzzle_files:
        print(f"Validating puzzle in {file}...")
        grid = Grid.from_csv_file(file)
        if not grid.is_valid():
            print(f"Invalid puzzle in {file}")
            return 1
        if not StrategicSolver().solve(grid).is_complete():
            print(f"Unsolvable puzzle in {file}")
            return 1
    return 0


if __name__ == "__main__":
    exit(validate_puzzle_files())
