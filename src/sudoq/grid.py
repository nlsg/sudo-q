from typing import Iterator, get_args
from dataclasses import dataclass
import random

from .core import Digit, Nine, Index, Position
from .unit import Unit


@dataclass(frozen=True)
class Grid:
    rows: Nine[Unit]

    @classmethod
    def from_csv_file(cls, path: str, delimiter=",") -> "Grid":
        with open(path) as csv:
            return cls(
                rows=tuple(
                    Unit(list(map(int, line)))
                    for raw_line in csv.readlines()
                    if (line := raw_line.strip("\n ").split(delimiter))[0]
                )
            )

    @classmethod
    def construct_empty(cls) -> "Grid":
        return cls(rows=[Unit(values=[0] * 9)] * 9)

    def generate_solved(self) -> "Grid":
        return self.solve_backtracking()

    def generate_puzzle(self) -> "Grid":
        next_puzzle = puzzle = self.generate_solved()

        def get_random_position() -> Position:
            while (
                position := (
                    random.choice(get_args(Index)),
                    random.choice(get_args(Index)),
                )
            ) not in self.iter_empty_positions():
                pass
            return position

        while True:
            if next_puzzle.solve() is None and not next_puzzle.is_solved():
                return puzzle
            puzzle = next_puzzle
            next_puzzle = puzzle.with_placement(get_random_position(), 0)

    def with_placement(self, position: Position, value: Digit) -> "Grid":
        row, col = position
        changed_unit = Unit(
            values=[value if i == col else v for i, v in enumerate(self.rows[row])]
        )
        return Grid(
            rows=(list(self.rows[:row]) + [changed_unit] + list(self.rows[row + 1 :]))
        )

    def get_candidates(self, position: Position) -> set[Digit]:
        return (
            self.get_row(position).get_candidates()
            & self.get_col(position).get_candidates()
            & self.get_box(position).get_candidates()
        )

    def iter_positions(self, value: Digit = 0) -> Iterator[Position]:
        for row_index, unit in enumerate(self.iter_rows()):
            for col_index, val in enumerate(unit):
                if val == value:
                    yield row_index, col_index

    def get_cell(self, position: Position) -> Digit:
        row, col = position
        return self.rows[row][col]

    def get_row(self, position: Position) -> Unit:
        row, _ = position
        return self.rows[row]

    def get_col(self, position: Position) -> Unit:
        _, col = position
        return Unit(values=[self.rows[i][col] for i in get_args(Index)])

    def get_box(self, position: Position) -> Unit:
        return Unit(
            values=list(
                self.rows[row][col] for row, col in self.get_box_positions(position)
            )
        )

    def get_box_positions(self, position: Position) -> Iterator[Position]:
        row, col = position
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        return ((start_row + r, start_col + c) for r in range(3) for c in range(3))

    def iter_rows(self) -> Iterator[Unit]:
        for row in self.rows:
            yield row

    def iter_cols(self) -> Iterator[Unit]:
        for i in get_args(Index):
            yield self.get_col((0, i))

    def iter_boxes(self) -> Iterator[Unit]:
        for row_offset in 0, 3, 6:
            for col_offset in 0, 3, 6:
                yield self.get_box((row_offset, col_offset))

    def is_valid(self) -> bool:
        return all(u.is_valid() for u in self.rows)

    def is_solved(self) -> bool:
        return all(unit.is_complete() for unit in self.rows)

    def __eq__(self, other: "Grid"):
        return isinstance(other, Grid) and all(
            own_unit == other_unit
            for own_unit, other_unit in zip(self.iter_rows(), other.iter_rows())
        )

    def __str__(self):
        empty_cells = len(list(self.iter_positions(0)))

        def format_unit(unit):
            return " ".join(
                map(
                    lambda iv: f" {iv[1]}" if not iv[0] % 3 else str(iv[1]),
                    enumerate(unit.values),
                )
            )

        return f"Board: {empty_cells}/{81 - empty_cells}" + "\n".join(
            map(
                lambda iv: f"\n{iv[1]}" if not iv[0] % 3 else str(iv[1]),
                enumerate(format_unit(u) for u in self.rows),
            )
        )
