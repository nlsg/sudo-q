from typing import Protocol, Optional, runtime_checkable

from .grid import Grid
from .core import Cell, Position


class Solver(Protocol):
    """might apply one or different strategies to solve a board"""

    def solve(self, grid: Grid) -> Grid:
        """shall always return a Grid, even if it is not solved completely"""


@runtime_checkable
class SolvingStrategy(Protocol):
    def get_placement(self, grid: Grid) -> Cell | None:
        """solve the grid"""


class CellReducer(Protocol):
    """Protocol for selecting positions to remove from grid"""

    def select_position(self, grid: Grid) -> Optional[Position]:
        """Select next position to remove"""
