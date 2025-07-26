import pytest

from context import Grid, sample_board, SAMPLE_DIR

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
