import pytest
from pathlib import Path
from src.sudoq import Board, Unit, Digit, Nine, Position

TEST_DIR = Path(__file__).parent
SAMPLE_DIR = TEST_DIR / "assets" / "samples"


@pytest.fixture(scope="module")
def sample_board():
    return Board.from_csv_file(str(SAMPLE_DIR / "valid-1.csv"))


__all__ = [Board, Unit, Digit, Nine, TEST_DIR, Position]
