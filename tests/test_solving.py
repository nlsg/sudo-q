import pytest
from pathlib import Path

from context import Grid, SAMPLE_DIR, sample_board, solvers

sample_board = sample_board


def test_get_cell(sample_board):
    assert sample_board.get_cell((0, 0)) == 7
    assert sample_board.get_cell((4, 4)) == 5
    assert sample_board.get_cell((8, 8)) == 9


def test_with_placement(sample_board):
    for position, value in (
        ((8, 7), 7),
        ((2, 2), 6),
        ((1, 8), 7),
    ):
        board = sample_board.with_placement(position, value)
        assert board.get_cell(position) == value


@pytest.mark.parametrize(
    ("path", "solved_path"),
    (
        (
            (SAMPLE_DIR / "valid-1.csv"),
            (SAMPLE_DIR / "solved-1.csv"),
        ),
    ),
)
def test_solve(path: Path, solved_path: Path):
    grid = Grid.from_csv_file(str(path))
    solved = Grid.from_csv_file(str(solved_path))
    assert solvers.StrategicSolver().solve(grid) == solved


@pytest.mark.parametrize(
    ("path"),
    (SAMPLE_DIR / "valid-1.csv",),
)
def test_solve_against_backtracking(path: Path):
    grid = Grid.from_csv_file(str(path))
    assert solvers.StrategicSolver().solve(grid) == solvers.BacktrackingSolver.solve(
        grid
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
