import pytest

from context import Board


@pytest.mark.parametrize("delimiter", (",", ";", "|"))
def test_board_from_csv(tmp_path, delimiter):
    csv_path = tmp_path / "board.csv"
    csv_path.write_text(
        "\n".join(delimiter.join(str(i + 1) for i in range(9)) for _ in range(9))
    )
    board = Board.from_csv_file(str(csv_path), delimiter=delimiter)
    assert board.is_valid()
