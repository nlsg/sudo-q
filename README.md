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
<!-- END_INJECT_CODE_EXAMPLE -->

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
