from dataclasses import dataclass, field
from typing import Sequence
import random

from ..grid import Grid
from ..core import Cell
from ..solvers import BacktrackingSolver, StrategicSolver
from ..protocols import Solver, CellReducer
from .reducers import CompositeReducer


@dataclass
class PuzzleGenerator:
    reducers: Sequence[CellReducer]
    solver: Solver = field(default_factory=StrategicSolver)
    min_clues: int = 17
    max_clues: int | None = 81

    def fill_grid(self, grid: Grid | None) -> Grid:
        return BacktrackingSolver(
            solve_step_hook=Grid.rotate,
            position_chooser=lambda position, _: random.choice(list(position)),
        ).solve(grid or Grid.construct_empty())

    def generate(self, grid: Grid | None = None, tries=10) -> Grid:
        _puzzle = None
        for _ in range(tries):
            if (puzzle := self._generate(grid)).count_filled() <= self.max_clues:
                return puzzle
            if not _puzzle or _puzzle.count_filled() > puzzle.count_filled():
                _puzzle = puzzle
        return _puzzle

    def _generate(self, grid: Grid | None = None) -> Grid:
        next_puzzle = puzzle = self.fill_grid(grid)

        reducer = CompositeReducer(self.reducers)
        while next_puzzle.count_filled() > self.min_clues:
            if not self.solver.solve(next_puzzle).is_complete():
                return puzzle

            puzzle = next_puzzle
            if position := reducer.select_position(puzzle):
                next_puzzle = puzzle.with_placement(Cell(position=position, value=0))
            else:
                break

        return puzzle
