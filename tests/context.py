import pytest
from pathlib import Path

from sudoq import Grid, Unit, Digit, Nine, Position, solvers, generators, Cell

TEST_DIR = Path(__file__).parent
SAMPLE_DIR = TEST_DIR / "assets" / "samples"


@pytest.fixture(scope="module", params=("valid-1", "valid-2"))
def solvable_grid(request):
    return Grid.from_csv_file(SAMPLE_DIR / f"{request.param}.csv")


@pytest.fixture(scope="module")
def sample_board():
    return Grid.from_csv_file(str(SAMPLE_DIR / "valid-1.csv"))


@pytest.fixture(scope="module")
def solved_sample_board():
    return solvers.BacktrackingSolver().solve(
        Grid.from_csv_file(str(SAMPLE_DIR / "solved-1.csv"))
    )


__all__ = [Grid, Unit, Digit, Nine, TEST_DIR, Position, solvers, generators, Cell]
