from typing import Protocol, Sequence
import random

from ..grid import Grid
from ..core import Position
from ..solvers import BacktrackingSolver, StrategicSolver
from ..solvers.protocols import Solver


class PuzzleGenerator(Protocol):
    solver: Solver

    def fill_grid(self, grid: Grid) -> Grid: ...

    def generate(self, grid: Grid | None = None) -> Grid: ...


class CellReducer(Protocol):
    def reduce(self, grid: Grid) -> Grid:
        """solve the grid"""


class RandomCellReducer(CellReducer):
    def reduce(self, grid: Grid) -> Grid:
        return grid.with_placement(
            self._get_random_position(list(grid.iter_positions(0))), 0
        )

    @staticmethod
    def _get_random_position(excluded_positions: Sequence[Position]) -> Position:
        while (
            position := (
                random.choice(range(9)),
                random.choice(range(9)),
            )
        ) in excluded_positions:
            pass
        return position


class BasicPuzzleGenerator(PuzzleGenerator):
    solver = StrategicSolver()
    reducer = RandomCellReducer()

    def fill_grid(self, grid: Grid) -> Grid:
        return BacktrackingSolver(
            position_chooser=lambda position, *a: random.choice(list(position))
        ).solve(grid)

    def generate(self, grid: Grid | None = None) -> Grid:
        next_puzzle = puzzle = self.fill_grid(grid or Grid.construct_empty())
        for _ in range(81 - 12):
            if (
                not self.solver.solve(next_puzzle).is_complete()
                and not next_puzzle.is_complete()
            ):
                return puzzle
            puzzle = next_puzzle
            next_puzzle = self.reducer.reduce(puzzle)
