from typing import Sequence
from dataclasses import dataclass, field

from ..grid import Grid
from .protocols import Solver, SolvingStrategy
from .strategies import NakedSingle, HiddenSingle


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


class BacktrackingSolver(Solver):
    def solve(self, grid: Grid) -> Grid:
        if not (position := next(grid.iter_positions(0), None)):
            return grid
        for candidate in grid.get_candidates(position):
            board = BacktrackingSolver().solve(grid.with_placement(position, candidate))
            if board.is_solved():
                return board
        return grid
