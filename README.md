# Sudo-q

A modern, type-safe Sudoku solver and puzzle generator implemented in Python.

## Overview

Sudo-q provides a comprehensive API for working with Sudoku puzzles:

- 🧩 Generate unique, solvable puzzles
- ✅ Validate board states
- 🔍 Solve using multiple strategies
- 🏗️ Build custom solving algorithms

## Installation

Requires Python 3.12+

Using standard pip:

```sh
pip install .

# editable install
pip install -e ".[dev]"
```

Using uv (faster installation):

```sh
uv sync
uv pip install -e .
```

## Quick Start

<!-- START_INJECT_CODE_EXAMPLE -->
```python
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
                    f"{strategy.__class__.__name__} applicable: {placement}
 Apply? [Y]es "
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

```<!-- END_INJECT_CODE_EXAMPLE -->

## Features

### Board Representation

- Immutable grid structure
- Type-safe cell values
- Efficient internal state

### Solvers

- Strategic solver (human-like strategies)
- Backtracking solver
- Custom strategy support

<!-- START_INJECTctSTRATEGIES -->
### HiddenPair
No description available.

### HiddenQuad
No description available.

### HiddenSingle
No description available.

### HiddenSubset
HiddenSubset(subset_size: Literal[2, 3])

### HiddenTriple
No description available.

### NakedPair
No description available.

### NakedQuad
No description available.

### NakedSingle
No description available.

### NakedSubset
NakedSubset(subset_size: Literal[2, 3, 4])

### NakedTriple
No description available.
<!-- END_INJECT_STRATEGIES -->

### Generators

- Difficulty-based generation
- Unique solution guarantee
- Configurable patterns

### Validation

- Full board validation
- Unit consistency checks
- Solution verification

## Contributing

open for contributions and feature requests

### Development
install pre-commit hooks:
```sh
pre-commit install
```
```sh
# Run tests
pytest

# Run tests with coverage
pytest --cov=sudoq

# Format code
ruff format .

# Run linter
ruff check .
```


## License

MIT License - See LICENSE file for details

---

**Note:** This project uses modern Python features and follows strict type checking. Ensure you're using Python 3.12 or newer.
