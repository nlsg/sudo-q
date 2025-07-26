from typing import FrozenSet, Iterator
from collections import defaultdict
from typing import Optional

import itertools

from .protocols import SolvingStrategy
from ..grid import Grid
from ..core import Position


class NakedSingle(SolvingStrategy):
    @staticmethod
    def apply(grid: Grid) -> Grid | None:
        """unique candidate"""
        for position in grid.iter_positions(0):
            row, col = position
            candidates = grid.get_candidates(position)
            # sole candidate
            if len(candidates) == 1:
                return grid.with_placement(position, next(iter(candidates)))


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
                        return grid.with_placement(position, candidate)


class NakedPair(SolvingStrategy):
    @staticmethod
    def apply(grid: Grid) -> Optional[Grid]:
        for unit_positions in itertools.chain(
            NakedPair._iter_row_positions(),
            NakedPair._iter_col_positions(),
            NakedPair._iter_box_positions(),
        ):
            # Find all candidate pairs in this unit
            pair_map: dict[FrozenSet[int], list[Position]] = defaultdict(list)

            for pos in unit_positions:
                if (
                    len(candidates := grid.get_candidates(pos)) == 2
                    and grid.get_cell(pos) == 0
                ):
                    pair_map[frozenset(candidates)].append(pos)

            for pair, positions in pair_map.items():
                if len(positions) != 2:
                    continue  # only care about exactly two cells

                # Naked pair found — eliminate pair digits from other cells in unit
                affected_positions = [
                    pos
                    for pos in unit_positions
                    if pos not in positions and grid.get_cell(pos) == 0
                ]

                for pos in affected_positions:
                    candidates = grid.get_candidates(pos)
                    remaining = candidates - pair
                    if len(remaining) == 1:
                        # This cell became solvable due to the pair elimination
                        digit = next(iter(remaining))
                        return grid.with_placement(pos, digit)

        return None

    @staticmethod
    def _iter_row_positions() -> Iterator[Position]:
        return ([(row, col) for col in range(9)] for row in range(9))

    @staticmethod
    def _iter_col_positions() -> Iterator[Position]:
        return ([(row, col) for row in range(9)] for col in range(9))

    @staticmethod
    def _iter_box_positions() -> Iterator[Position]:
        return (
            [(r + dr, c + dc) for dr in range(3) for dc in range(3)]
            for r in (0, 3, 6)
            for c in (0, 3, 6)
        )
