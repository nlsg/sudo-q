from typing import Sequence, Callable, Iterator, TypeVar
from dataclasses import dataclass, field

from ..grid import Grid
from .protocols import Solver, SolvingStrategy
from .strategies import NakedSingle, HiddenSingle


T = TypeVar("T")


@dataclass
class StrategicSolver(Solver):
    strategies: Sequence[SolvingStrategy] = field(
        default_factory=lambda: [NakedSingle, HiddenSingle]
    )

    def solve(self, grid: Grid) -> Grid:
        while not grid.is_complete():
            for strategy in self.strategies:
                if updated_gird := strategy.apply(grid):
                    grid = updated_gird
                    break
            else:
                return grid
        return grid


@dataclass
class BacktrackingSolver(Solver):
    position_chooser: Callable[[Iterator[T]], T] = next

    def solve(self, grid: Grid) -> Grid:
        if not (position := self.position_chooser(grid.iter_positions(0), None)):
            return grid
        for candidate in grid.get_candidates(position):
            board = BacktrackingSolver().solve(grid.with_placement(position, candidate))
            if board.is_complete():
                return board
        return grid
