from typing import Protocol

from .grid import Grid
from .core import Cell


class Solver(Protocol):
    """might apply one or different strategies to solve a board"""

    def solve(self, grid: Grid) -> Grid:
        """shall always return a Grid, even if it is not solved completely"""


class SolvingStrategy(Protocol):
    def get_placement(self, grid: Grid) -> Cell | None:
        """solve the grid"""
