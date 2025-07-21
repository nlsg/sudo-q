import pytest
from pathlib import Path

from context import Board, SAMPLE_DIR, sample_board

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
    board = Board.from_csv_file(str(path))
    solved = Board.from_csv_file(str(solved_path))
    assert board.solve() == solved


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
    board = Board.from_csv_file(str(path))
    solved = Board.from_csv_file(str(solved_path))
    assert board.solve_backtracking() == solved
