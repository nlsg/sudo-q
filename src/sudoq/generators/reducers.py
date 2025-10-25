from typing import Sequence, Optional
import random

from ..core import Position
from ..protocols import CellReducer
from ..grid import Grid


class RandomCellReducer(CellReducer):
    def select_position(self, grid: Grid) -> Optional[Position]:
        filled_positions = list(grid.iter_positions(lambda digit: digit != 0))
        if not filled_positions:
            return None
        return random.choice(filled_positions)


class DigitReducer(CellReducer):
    def __init__(self, digit: int, keep_count: int = 1):
        self.digit = digit
        self.keep_count = keep_count
        self._removed: set[Position] = set()

    def select_position(self, grid: Grid) -> Optional[Position]:
        digit_positions = set(grid.iter_positions(self.digit)) - self._removed
        if len(digit_positions) <= self.keep_count:
            return None

        position = random.choice(list(digit_positions))
        self._removed.add(position)
        return position


class CompositeReducer(CellReducer):
    def __init__(self, reducers: Sequence[CellReducer]):
        self.reducers = reducers
        self._current_index = 0

    def select_position(self, grid: Grid) -> Optional[Position]:
        if not self.reducers:
            return None

        start_index = self._current_index
        while True:
            current_reducer = self.reducers[self._current_index]
            self._current_index = (self._current_index + 1) % len(self.reducers)
            if position := current_reducer.select_position(grid):
                return position

            if self._current_index == start_index:
                return None
        return None


class SequentialReducer(CellReducer):
    def __init__(self, reducers: Sequence[CellReducer]):
        self.reducers = reducers
        self._current_index = 0

    def select_position(self, grid: Grid) -> Optional[Position]:
        for reducer in self.reducers:
            if position := reducer.select_position(grid):
                return position
            else:
                self._current_index += 1
        return None
