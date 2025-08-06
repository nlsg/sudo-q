from typing import Optional, Literal
from dataclasses import dataclass

import itertools

from ..protocols import SolvingStrategy
from ..grid import Grid
from ..core import Cell
from ..core import iter_unit_positions


class NakedSingle(SolvingStrategy):
    @staticmethod
    def get_placement(grid: Grid) -> Grid | None:
        """unique candidate"""
        for position in grid.iter_positions(0):
            row, col = position
            candidates = grid.get_candidates(position)
            # sole candidate
            if len(candidates) == 1:
                return Cell(position=position, value=next(iter(candidates)))


class HiddenSingle(SolvingStrategy):
    @staticmethod
    def get_placement(grid: Grid) -> Grid | None:
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
class HiddenSubset(SolvingStrategy):
    subset_size: Literal[2, 3]

    def get_placement(self, grid: Grid) -> Optional[Cell]:
        for unit_positions in iter_unit_positions():
            empty_positions = [pos for pos in unit_positions if grid.get_cell(pos) == 0]

            all_candidates = set().union(
                *(grid.get_candidates(pos) for pos in empty_positions)
            )

            # Check all possible candidate combinations
            for candidates in itertools.combinations(all_candidates, self.subset_size):
                candidates_set = set(candidates)

                positions = [
                    pos
                    for pos in empty_positions
                    if candidates_set & grid.get_candidates(pos)
                ]

                if len(positions) == self.subset_size:
                    for pos in positions:
                        candidates = grid.get_candidates(pos)
                        to_eliminate = candidates - candidates_set
                        if to_eliminate:
                            remaining = candidates & candidates_set
                            if len(remaining) == 1:
                                return Cell(position=pos, value=next(iter(remaining)))
        return None


class HiddenPair(HiddenSubset):
    def __init__(self):
        super().__init__(subset_size=2)


class HiddenTriple(HiddenSubset):
    def __init__(self):
        super().__init__(subset_size=3)


class HiddenQuad(HiddenSubset):
    def __init__(self):
        super().__init__(subset_size=4)


@dataclass
class NakedSubset(SolvingStrategy):
    subset_size: Literal[2, 3, 4]

    def get_placement(self, grid: Grid) -> Optional[Cell]:
        for unit_positions in iter_unit_positions():
            subset_cells = [
                (pos, grid.get_candidates(pos))
                for pos in unit_positions
                if grid.get_cell(pos) == 0
                and 1 < len(grid.get_candidates(pos)) <= self.subset_size
            ]

            for positions in itertools.combinations(
                [p for p, _ in subset_cells], self.subset_size
            ):
                subset = set().union(*(grid.get_candidates(pos) for pos in positions))

                if len(subset) == self.subset_size:
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


class NakedPair(NakedSubset):
    def __init__(self):
        super().__init__(subset_size=2)


class NakedTriple(NakedSubset):
    def __init__(self):
        super().__init__(subset_size=3)


class NakedQuad(NakedSubset):
    def __init__(self):
        super().__init__(subset_size=4)


all_strategies = (
    NakedSingle(),
    HiddenSingle(),
    #
    NakedPair(),
    NakedTriple(),
    NakedQuad(),
    #
    HiddenPair(),
    HiddenTriple(),
    HiddenQuad(),
)
