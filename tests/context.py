import pytest
from pathlib import Path

from sudoq import Grid, Unit, Digit, Nine, Position, solvers

TEST_DIR = Path(__file__).parent
SAMPLE_DIR = TEST_DIR / "assets" / "samples"


@pytest.fixture(scope="module")
def sample_board():
    return Grid.from_csv_file(str(SAMPLE_DIR / "valid-1.csv"))


__all__ = [Grid, Unit, Digit, Nine, TEST_DIR, Position, solvers]
