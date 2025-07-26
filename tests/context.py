import pytest
from pathlib import Path

from sudoq import Grid, Unit, Digit, Nine, Position, solvers, generators

TEST_DIR = Path(__file__).parent
SAMPLE_DIR = TEST_DIR / "assets" / "samples"


@pytest.fixture(scope="module")
def sample_board():
    return Grid.from_csv_file(str(SAMPLE_DIR / "valid-1.csv"))


@pytest.fixture(scope="module")
def solved_sample_board():
    return solvers.solvers.BacktrackingSolver().solve(
        Grid.from_csv_file(str(SAMPLE_DIR / "solved-1.csv"))
    )


__all__ = [Grid, Unit, Digit, Nine, TEST_DIR, Position, solvers, generators]
