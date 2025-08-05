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

```python
from sudoq import Grid, solvers

# load a grid from:
# - nested-sequence
Grid.from_value_matrix((range(9) for _ in range(9))).is_valid() # False

# - a csv-file
from pathlib import Path
Grid.from_csv_file(Path("to a file"), delimiter="|")

# - a string
puzzle = Grid.from_string("""
    530070000
    600195000
    098000060
    800060003
    400803001
    700020006
    060000280
    000419005
    000080079
""")

# Solve it!
solver = solvers.StrategicSolver()
solution = solver.solve(puzzle)
solution.is_solved() # True
print(puzzle)
print(solution)

# test strategies
from sudoq import strategies

if (move := strategies.NakedPair().apply(puzzle)):
    print(f"Naked-pair found: {move}")

for strategy in strategies.all_strategies:
    if (placement := strategy.get_placement(puzzle)):
        print(f"Naked-pair found: {placement}")



```

## Project Structure

```
sudo-q/
├── src/
│   └── sudoq/           # Main package
│       ├── core.py      # Core types & constants
│       ├── grid.py      # Grid implementation
│       ├── unit.py      # Unit (row/col/box) logic
│       ├── solvers/     # Solving strategies
│       └── generators/  # Puzzle generators
├── tests/               # Test suite
│   ├── context.py
│   └── test_*.py
├── pyproject.toml       # Project metadata & dependencies
└── .pre-commit-config.yaml
```

## Features

### Board Representation

- Immutable grid structure
- Type-safe cell values
- Efficient internal state

### Solvers

- Strategic solver (human-like strategies)
- Backtracking solver
- Custom strategy support

<!-- START_STRATEGIES -->
### HiddenSingle
No description available.

### NakedPair
No description available.

### NakedSingle
No description available.

### NakedSubset
NakedSubset(subset_size: Literal[2, 3])

### NakedTriple
No description available.
<!-- END_STRATEGIES -->

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
