from typing import Protocol

from ..grid import Grid


class Solver(Protocol):
    """might apply one or different strategies to solve a board"""

    def solve(self, grid: Grid) -> Grid:
        """shall always return a Grid, even if it is not solved completely"""


class SolvingStrategy(Protocol):
    def apply(self, grid: Grid) -> Grid | None:
        """solve the grid"""
