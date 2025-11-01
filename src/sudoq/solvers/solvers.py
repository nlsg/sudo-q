from typing import Sequence, Callable, Iterator, TypeVar
from dataclasses import dataclass, field

from ..grid import Grid
from ..core import Cell, Position, CellValue
from ..protocols import Solver, SolvingStrategy
from .strategies import all_strategies


T = TypeVar("T")


@dataclass
class StrategicSolver(Solver):
    """A solver that applies a sequence of strategies to resolve placements of the grid,
    until no more strategies are applicable or the grid is complete.

    In turns, each strategy applies exactly one placement to the grid, not until it is exhausted.
    """

    strategies: Sequence[SolvingStrategy] = field(
        default_factory=lambda: all_strategies
    )

    def solve(self, grid: Grid) -> Grid:
        while not grid.is_complete():
            for strategy in self.strategies:
                if updated_cell := strategy.get_placement(grid):
                    grid = grid.with_placement(updated_cell)
                    break
            else:
                return grid
        return grid


@dataclass
class BacktrackingSolver(Solver):
    """A solver that uses backtracking to find a solution for the grid."""

    position_chooser: Callable[[Iterator[Position]], Position] = next
    candidate_hook: Callable[[set[CellValue]], Iterator[CellValue]] = lambda s: s
    solve_step_hook: Callable[[Grid], Grid] = lambda g: g

    def solve(self, grid: Grid) -> Grid:
        if not (position := self.position_chooser(grid.iter_positions(0), None)):
            return grid
        for candidate in self.candidate_hook(grid.get_candidates(position)):
            board = self.solve_step_hook(
                BacktrackingSolver().solve(
                    grid.with_placement(Cell(position=position, value=candidate))
                )
            )
            if board.is_complete():
                return board
        return grid
