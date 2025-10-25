import pytest

from context import Grid, sample_board, SAMPLE_DIR, Cell

sample_board = sample_board


def test_board_from_values(sample_board):
    assert (
        Grid.from_value_matrix(
            [
                [7, 0, 0, 4, 9, 0, 0, 1, 2],
                [0, 1, 9, 2, 7, 5, 6, 4, 0],
                [2, 0, 0, 6, 1, 8, 0, 0, 0],
                [5, 8, 0, 9, 2, 0, 7, 6, 0],
                [0, 0, 0, 0, 5, 0, 9, 0, 1],
                [6, 0, 1, 8, 4, 0, 2, 0, 5],
                [0, 0, 0, 7, 3, 4, 0, 2, 6],
                [0, 0, 7, 0, 0, 0, 0, 5, 8],
                [1, 4, 6, 0, 8, 2, 0, 0, 9],
            ]
        )
        == sample_board
    )


def test_grid_from_string():
    grid_str = """
        530070000
        600195000
        098000060
        800060003
        400803001
        700020006
        060000280
        000419005
        000080079
    """

    grid = Grid.from_string(grid_str)
    assert grid.get_cell((0, 0)) == 5
    assert grid.get_cell((0, 1)) == 3
    assert grid.get_cell((1, 3)) == 1
    assert grid.get_cell((0, 5)) == 0
    with pytest.raises(ValueError):
        Grid.from_string("invalid")
    with pytest.raises(ValueError):
        Grid.from_string("123" * 20)
    grid_str_with_dots = "5.....123" * 9
    grid = Grid.from_string(grid_str_with_dots)
    assert grid.get_cell((0, 0)) == 5
    assert grid.get_cell((0, 1)) == 0  # dot converted to 0


@pytest.mark.parametrize("path", ((SAMPLE_DIR / "valid-1.csv"),))
def test_board_from_csv(path, sample_board):
    assert Grid.from_csv_file(str(path), delimiter=",") == sample_board


@pytest.mark.parametrize("delimiter", (",", ";", "|"))
def test_board_from_csv_is_valid(tmp_path, delimiter):
    csv_path = tmp_path / "board.csv"
    csv_path.write_text(
        "\n".join(delimiter.join(str(i + 1) for i in range(9)) for _ in range(9))
    )
    board = Grid.from_csv_file(str(csv_path), delimiter=delimiter)
    assert board.is_valid()


def test_construct_empty():
    empty_board = Grid.construct_empty()
    assert len(empty_board.rows) == 9
    assert all(len(u.values) == 9 for u in empty_board.rows)
    assert empty_board.is_valid()


def test_board_str(sample_board):
    assert str(sample_board) == "\n".join(
        (
            "Board: 36/45",
            " 7 0 0  4 9 0  0 1 2",
            " 0 1 9  2 7 5  6 4 0",
            " 2 0 0  6 1 8  0 0 0",
            "",
            " 5 8 0  9 2 0  7 6 0",
            " 0 0 0  0 5 0  9 0 1",
            " 6 0 1  8 4 0  2 0 5",
            "",
            " 0 0 0  7 3 4  0 2 6",
            " 0 0 7  0 0 0  0 5 8",
            " 1 4 6  0 8 2  0 0 9",
        )
    )


def test_grid_to_string(sample_board):
    grid_string = sample_board.to_string()
    assert len(grid_string) == 81
    assert all(c in "0123456789" for c in grid_string)
    # Round trip
    reconstructed = Grid.from_string(grid_string)
    assert reconstructed == sample_board


def test_grid_rotate_90_clockwise():
    # Test with values in bottom-right 3x3, expect rotated in top-left 3x3
    simple_grid = Grid.from_value_matrix(
        [[0] * 9] * 6
        + [
            [1, 2, 3] + [0] * 6,
            [4, 5, 6] + [0] * 6,
            [7, 8, 9] + [0] * 6,
        ]
    )
    rotated = simple_grid.rotate()
    # Expected: rotated 3x3 at top-left
    expected_values = [
        [7, 4, 1] + [0] * 6,
        [8, 5, 2] + [0] * 6,
        [9, 6, 3] + [0] * 6,
    ] + [[0] * 9] * 6
    expected = Grid.from_value_matrix(expected_values)
    assert rotated == expected


def test_rotate_360_degrees_returns_original(sample_board):
    # Rotating 4 times should equal original
    rotated = sample_board
    for _ in range(4):
        rotated = rotated.rotate()
    assert rotated == sample_board


# Cell tests
def test_cell_is_empty():
    cell = Cell(position=(0, 0), value=0)
    assert cell.is_empty() is True
    cell = Cell(position=(0, 1), value=5)
    assert cell.is_empty() is False
