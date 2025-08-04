from sudoq import Grid, solvers, strategies

from pathlib import Path


# load a grid from:
# - nested-sequence
Grid.from_value_matrix((range(9) for _ in range(9))).is_valid()  # False

# - a csv-file
Grid.from_csv_file(Path("tests", "assets", "samples", "hard-1.csv"), delimiter=",")

# - a string


puzzle = Grid.from_string("""
    530 070 000
    600 195 000
    098 000 060
    800 060 003
    400 803 001
    700 020 006
    060 000 280
    000 419 005
    000 080 079
""")

# Solve it!
solver = solvers.StrategicSolver()
solution = solver.solve(puzzle)
solution.is_valid()  # True - basic rules are satisfied
solution.is_complete()  # True - all cells are filled
print(puzzle)
print(solution)


if move := strategies.NakedPair().get_placement(puzzle):
    print(f"Naked-pair found: {move}")

print(puzzle)
while not puzzle.is_complete():
    for strategy in strategies.all_strategies:
        if placement := strategy.get_placement(puzzle):
            if (
                input(
                    f"{strategy.__class__.__name__} applicable: {placement}\n Apply? [Y]es "
                )
                .lower()
                .startswith("y")
            ):
                puzzle = puzzle.with_placement(placement)
                print("grid updated!")
                print(puzzle)
    else:
        print("No more strategies applicable, exiting.")
        break
