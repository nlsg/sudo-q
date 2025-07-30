from typing import Iterator, get_args, Sequence, Union
from dataclasses import dataclass

from .core import Cell, Digit, Nine, Index, Position
from .unit import Unit

import typing

if typing.TYPE_CHECKING:
    from pathlib import Path


@dataclass(frozen=True)
class Grid:
    rows: Nine[Unit]

    @classmethod
    def from_value_matrix(cls, value_matrix: Sequence[Sequence[Digit]]) -> "Grid":
        grid = cls(
            rows=tuple(Unit(tuple(map(int, tuple(values)))) for values in value_matrix)
        )
        if len(grid.rows) != 9 or not all(len(unit.values) == 9 for unit in grid.rows):
            raise ValueError("Sudoku grid has faulty shape")
        return grid

    @classmethod
    def from_csv_file(cls, path: Union["Path", str], delimiter=",") -> "Grid":
        with open(path) as csv:
            return cls.from_value_matrix(
                value_matrix=tuple(
                    list(map(int, line))
                    for raw_line in csv.readlines()
                    if (line := raw_line.strip("\n ").split(delimiter))[0]
                )
            )

    @classmethod
    def from_string(cls, grid_string: str) -> "Grid":
        clean = "".join(c if c != "." else "0" for c in grid_string if c not in " \n\t")

        if len(clean) != 81:
            raise ValueError("Grid string must contain exactly 81 digits")

        return cls.from_value_matrix(
            tuple(tuple(tuple(clean[i : i + 9]) for i in range(0, 81, 9)))
        )

    @classmethod
    def construct_empty(cls) -> "Grid":
        return cls.from_value_matrix(((0,) * 9,) * 9)

    def with_placement(self, cell: Cell) -> "Grid":
        row, col = cell.position
        changed_unit = Unit(
            values=tuple(
                cell.value if i == col else v for i, v in enumerate(self.rows[row])
            )
        )
        return Grid(
            rows=(
                tuple(
                    list(self.rows[:row]) + [changed_unit] + list(self.rows[row + 1 :])
                )
            )
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

    def is_complete(self) -> bool:
        return all(unit.is_complete() for unit in self.rows)

    def count_empty(self) -> int:
        return len(list(self.iter_positions(0)))

    def count_filled(self) -> int:
        return 81 - self.count_empty()

    def __eq__(self, other: "Grid"):
        return isinstance(other, Grid) and all(
            own_unit == other_unit
            for own_unit, other_unit in zip(self.iter_rows(), other.iter_rows())
        )

    def __str__(self):
        def format_unit(unit):
            return " ".join(
                map(
                    lambda iv: f" {iv[1]}" if not iv[0] % 3 else str(iv[1]),
                    enumerate(unit.values),
                )
            )

        return f"Board: {self.count_empty()}/{self.count_filled}" + "\n".join(
            map(
                lambda iv: f"\n{iv[1]}" if not iv[0] % 3 else str(iv[1]),
                enumerate(format_unit(u) for u in self.rows),
            )
        )
