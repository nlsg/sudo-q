import pytest
from pathlib import Path

from context import Grid, SAMPLE_DIR, sample_board, solved_sample_board, solvers

sample_board = sample_board
solved_sample_board = solved_sample_board


def test_StrategicSolver(sample_board, solved_sample_board):
    assert solvers.StrategicSolver().solve(sample_board) == solved_sample_board


def test_solve_against_backtracking(sample_board):
    assert solvers.StrategicSolver().solve(
        sample_board
    ) == solvers.BacktrackingSolver.solve(sample_board)


@pytest.mark.parametrize(
    ("strategy"),
    (
        solvers.strategies.HiddenSingle,
        solvers.strategies.NakedSingle,
    ),
)
def test_strategies(strategy, sample_board, solved_sample_board):
    assert (
        solvers.StrategicSolver(strategies=(strategy,)).solve(sample_board)
        == solved_sample_board
    )


def test_unsolvable():
    assert not solvers.StrategicSolver().solve(Grid.construct_empty()).is_solved()


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
    assert solvers.BacktrackingSolver.solve(grid) == solved
