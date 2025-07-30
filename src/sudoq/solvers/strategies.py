from typing import FrozenSet, Iterator, Optional, Literal
from collections import defaultdict
from dataclasses import dataclass

import itertools

from .protocols import SolvingStrategy
from ..grid import Grid
from ..core import Position, Cell


class NakedSingle(SolvingStrategy):
    @staticmethod
    def apply(grid: Grid) -> Grid | None:
        """unique candidate"""
        for position in grid.iter_positions(0):
            row, col = position
            candidates = grid.get_candidates(position)
            # sole candidate
            if len(candidates) == 1:
                return Cell(position=position, value=next(iter(candidates)))


class HiddenSingle:
    @staticmethod
    def apply(grid: Grid) -> Grid | None:
        empty_positions = list(grid.iter_positions(0))
        for position in empty_positions:
            row, col = position
            candidates = grid.get_candidates(position)
            # unique candidate
            box_positions = list(grid.get_box_positions(position))
            for empties_set in (
                (p for p in empty_positions if p[0] == row and p[1] != col),
                (p for p in empty_positions if p[0] != row and p[1] == col),
                (p for p in empty_positions if p != position and p in box_positions),
            ):
                empties_set = list(empties_set)
                for candidate in candidates:
                    if not any(
                        candidate in grid.get_candidates(pos) for pos in empties_set
                    ):
                        return Cell(position=position, value=candidate)


@dataclass
class NakedSubset(SolvingStrategy):
    subset_size: Literal[2, 3]

    def apply(self, grid: Grid) -> Optional[Cell]:
        for unit_positions in itertools.chain(
            self._iter_row_positions(),
            self._iter_col_positions(),
            self._iter_box_positions(),
        ):
            subset_map: dict[FrozenSet[int], list[Position]] = defaultdict(list)

            for pos in unit_positions:
                candidates = grid.get_candidates(pos)
                if len(candidates) <= self.subset_size and grid.get_cell(pos) == 0:
                    key = frozenset(candidates)
                    if 1 < len(key) <= self.subset_size:
                        subset_map[key].append(pos)

            for subset, positions in subset_map.items():
                if len(subset) == len(positions) == self.subset_size:
                    affected_positions = [
                        pos
                        for pos in unit_positions
                        if pos not in positions and grid.get_cell(pos) == 0
                    ]

                    for pos in affected_positions:
                        candidates = grid.get_candidates(pos)
                        remaining = candidates - subset
                        if len(remaining) == 1:
                            digit = next(iter(remaining))
                            return Cell(position=pos, value=digit)

        return None

    @staticmethod
    def _iter_row_positions() -> Iterator[list[Position]]:
        return ([(row, col) for col in range(9)] for row in range(9))

    @staticmethod
    def _iter_col_positions() -> Iterator[list[Position]]:
        return ([(row, col) for row in range(9)] for col in range(9))

    @staticmethod
    def _iter_box_positions() -> Iterator[list[Position]]:
        return (
            [(r + dr, c + dc) for dr in range(3) for dc in range(3)]
            for r in (0, 3, 6)
            for c in (0, 3, 6)
        )


class NakedPair(NakedSubset):
    def __init__(self):
        super().__init__(subset_size=2)


class NakedTriple(NakedSubset):
    def __init__(self):
        super().__init__(subset_size=3)
