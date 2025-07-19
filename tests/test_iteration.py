import pytest
from pathlib import Path


from context import Board, SAMPLE_DIR


def iter_offsets():
    for row_offset in 0, 3, 6:
        for col_offset in 0, 3, 6:
            yield row_offset, col_offset


def get_lines_of_csv(path: str) -> list[list[int]]:
    with open(str(path)) as fp:
        return [
            list(map(int, sanitized_line.split(",")))
            for line in fp.readlines()
            if (sanitized_line := line.strip("\n "))
        ]


@pytest.mark.parametrize("path", (SAMPLE_DIR / "valid-1.csv",))
def test_iter_rows(path: Path):
    board = Board.from_csv_file(str(path))
    lines = get_lines_of_csv(str(path))
    for line, unit in zip(lines, board.iter_rows()):
        assert unit.values == line


@pytest.mark.parametrize("path", (SAMPLE_DIR / "valid-1.csv",))
def test_iter_cols(path: Path):
    board = Board.from_csv_file(str(path))
    lines = get_lines_of_csv(path)
    for i, unit in enumerate(board.iter_cols()):
        assert unit.values == [lines[j][i] for j in range(9)]


@pytest.mark.parametrize("path", (SAMPLE_DIR / "valid-1.csv",))
def test_iter_boxes(path: Path):
    board = Board.from_csv_file(str(path))
    lines = get_lines_of_csv(path)
    for (row_offset, col_offset), unit in zip(iter_offsets(), board.iter_boxes()):
        box = list(
            lines[row_offset + i][col_offset + r] for i in range(3) for r in range(3)
        )
        assert unit.values == box
