import pytest


from context import Grid, Unit, Digit, Nine, SAMPLE_DIR


@pytest.mark.parametrize(
    ("values", "expectation"),
    [
        ((1, 2, 3, 4, 5, 6, 7, 8, 9), True),
        ((1, 2, 3, 4, 5, 6, 7, 8, 8), False),
        ((0, 0, 3, 4, 5, 6, 7, 8, 0), True),
        ((0, 0, 3, 3, 5, 6, 7, 8, 0), False),
    ],
)
def test_unit_is_valid(values: Nine[Digit], expectation: bool):
    assert Unit(values=values).is_valid() == expectation


def test_board_is_valid():
    board = Grid(rows=[Unit(values=(1, 2, 3, 4, 5, 6, 7, 8, 9)) for _ in range(9)])
    assert board.is_valid()


@pytest.mark.parametrize(
    "path",
    [SAMPLE_DIR / "valid-1.csv"],
)
def test_csv_is_valid(path):
    board = Grid.from_csv_file(path)
    assert board.is_valid()


@pytest.mark.parametrize(
    "path",
    [SAMPLE_DIR / "valid-1.csv"],
)
def test_contains_Digits(path):
    board = Grid.from_csv_file(path)
    for row in board.rows:
        for value in row.values:
            assert isinstance(value, int)
            assert 0 <= value <= 9
