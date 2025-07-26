from .protocols import SolvingStrategy
from ..grid import Grid


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
