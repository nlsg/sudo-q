import pytest
from pathlib import Path

from context import (
    Grid,
    SAMPLE_DIR,
    sample_board,
    solved_sample_board,
    solvable_grid,
    solvers,
    Cell,
    strategies,
)

sample_board = sample_board
solved_sample_board = solved_sample_board
solvable_grid = solvable_grid


def test_StrategicSolver(sample_board, solved_sample_board):
    assert solvers.StrategicSolver().solve(sample_board) == solved_sample_board


def test_solve_against_backtracking(solvable_grid):
    assert solvers.StrategicSolver().solve(
        solvable_grid
    ) == solvers.BacktrackingSolver().solve(solvable_grid)


@pytest.mark.parametrize(
    ("strategy"),
    (
        strategies.HiddenSingle,
        strategies.NakedSingle,
    ),
)
def test_strategies(strategy, sample_board, solved_sample_board):
    assert (
        solvers.StrategicSolver(strategies=(strategy,)).solve(sample_board)
        == solved_sample_board
    )


def test_unsolvable():
    assert not solvers.StrategicSolver().solve(Grid.construct_empty()).is_complete()


@pytest.mark.parametrize(
    ("path", "solved_path"),
    (
        (
            (SAMPLE_DIR / "valid-1.csv"),
            (SAMPLE_DIR / "solved-1.csv"),
        ),
    ),
)
def test_solve_backtracking(path: Path, solved_path: Path):
    grid = Grid.from_csv_file(str(path))
    solved = Grid.from_csv_file(str(solved_path))
    assert solvers.BacktrackingSolver().solve(grid) == solved


def test_naked_pair():
    # from: https://www.sudokuwiki.org/naked_candidates
    grid_values = [
        [4, 0, 0, 2, 3, 4, 5, 3, 8],
        [0, 3, 2, 0, 9, 4, 1, 0, 0],
        [0, 9, 5, 3, 0, 0, 2, 4, 0],
        *[[0] * 9 for _ in range(6)],
    ]

    grid = Grid.from_value_matrix(grid_values)

    cell = strategies.NakedPair().get_placement(grid)
    assert cell == Cell(position=(1, 0), value=8)


def test_naked_triple():
    # from: https://www.sudokuwiki.org/naked_candidates
    grid_values = [
        [2, 9, 4, 5, 1, 3, 0, 0, 6],
        [6, 0, 0, 8, 4, 2, 3, 1, 9],
        [3, 0, 0, 6, 9, 7, 2, 5, 4],
        [0, 0, 0, 0, 5, 6, 0, 0, 0],
        [0, 4, 0, 0, 8, 0, 0, 6, 0],
        [0, 0, 0, 4, 7, 0, 0, 0, 0],
        [7, 3, 0, 1, 6, 4, 0, 0, 5],
        [9, 0, 0, 7, 3, 5, 0, 0, 1],
        [4, 0, 0, 9, 2, 8, 6, 3, 7],
    ]

    grid = Grid.from_value_matrix(grid_values)

    placement = strategies.NakedTriple().get_placement(grid)
    assert placement == Cell(position=(5, 7), value=9)


def test_naked_quad():
    # from: https://www.sudokuwiki.org/naked_candidates
    grid_values = [
        [0, 0, 0, 4, 3, 0, 0, 8, 6],
        [0, 0, 0, 0, 2, 0, 0, 4, 0],
        [0, 9, 0, 0, 7, 8, 5, 2, 0],
        [3, 7, 1, 8, 5, 6, 2, 9, 4],
        [4, 0, 0, 1, 4, 2, 3, 7, 5],
        [4, 0, 0, 3, 9, 7, 6, 1, 8],
        [2, 0, 0, 7, 0, 3, 8, 5, 9],
        [0, 3, 9, 2, 0, 5, 4, 6, 7],
        [7, 0, 0, 9, 0, 4, 1, 3, 2],
    ]

    grid = Grid.from_value_matrix(grid_values)
    cell = strategies.NakedQuad().get_placement(grid)
    assert cell == Cell(position=(0, 1), value=2)
