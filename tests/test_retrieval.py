import pytest
from pathlib import Path

from context import Grid, SAMPLE_DIR, Nine, Position, Digit


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
    board = Grid.from_csv_file(str(path))
    lines = get_lines_of_csv(str(path))
    for line, unit in zip(lines, board.iter_rows()):
        assert unit.values == line


@pytest.mark.parametrize("path", (SAMPLE_DIR / "valid-1.csv",))
def test_iter_cols(path: Path):
    board = Grid.from_csv_file(str(path))
    lines = get_lines_of_csv(path)
    for i, unit in enumerate(board.iter_cols()):
        assert unit.values == [lines[j][i] for j in range(9)]


@pytest.mark.parametrize("path", (SAMPLE_DIR / "valid-1.csv",))
def test_iter_boxes(path: Path):
    board = Grid.from_csv_file(str(path))
    lines = get_lines_of_csv(path)
    for (row_offset, col_offset), unit in zip(iter_offsets(), board.iter_boxes()):
        box = list(
            lines[row_offset + i][col_offset + r] for i in range(3) for r in range(3)
        )
        assert unit.values == box


@pytest.mark.parametrize(
    ("path", "position", "expectation"),
    (
        ((SAMPLE_DIR / "valid-1.csv"), (0, 0), (7, 0, 0, 0, 1, 9, 2, 0, 0)),
        ((SAMPLE_DIR / "valid-1.csv"), (1, 2), (7, 0, 0, 0, 1, 9, 2, 0, 0)),
        ((SAMPLE_DIR / "valid-1.csv"), (3, 3), (9, 2, 0, 0, 5, 0, 8, 4, 0)),
    ),
)
def test_get_box(path: Path, position: Position, expectation: Nine[Digit]):
    board = Grid.from_csv_file(str(path))
    u1 = board.get_box(position)
    assert tuple(u1.values) == tuple(expectation)


@pytest.mark.parametrize(
    ("path", "position", "expectation"),
    (
        ((SAMPLE_DIR / "valid-1.csv"), (0, 2), (7, 0, 0, 4, 9, 0, 0, 1, 2)),
        ((SAMPLE_DIR / "valid-1.csv"), (2, 8), (2, 0, 0, 6, 1, 8, 0, 0, 0)),
    ),
)
def test_get_row(path: Path, position: Position, expectation: Nine[Digit]):
    board = Grid.from_csv_file(str(path))
    u1 = board.get_row(position)
    assert tuple(u1.values) == tuple(expectation)


@pytest.mark.parametrize(
    ("path", "position", "expectation"),
    (
        ((SAMPLE_DIR / "valid-1.csv"), (0, 2), (0, 9, 0, 0, 0, 1, 0, 7, 6)),
        ((SAMPLE_DIR / "valid-1.csv"), (2, 7), (1, 4, 0, 6, 0, 0, 2, 5, 0)),
    ),
)
def test_get_col(path: Path, position: Position, expectation: Nine[Digit]):
    board = Grid.from_csv_file(str(path))
    u1 = board.get_col(position)
    assert tuple(u1.values) == tuple(expectation)
