from __future__ import annotations
from typing import get_args, Sequence, Union, TypeVar, Generic, Iterator, Callable
from pathlib import Path
from functools import partial
import math

from dataclasses import dataclass, field

from .core import Cell, Position, NineDigits, BaseGrid, CellValue
from .unit import Unit


T = TypeVar("T")


@dataclass(frozen=True)
class Grid(BaseGrid, Generic[T]):
    rows: tuple[Unit[T], ...]
    digit_type: type[T] = field(default=NineDigits)

    @property
    def Unit(self) -> type[Unit[T]]:
        return partial(Unit, digit_type=self.digit_type)

    @property
    def N(self) -> int:
        return len(self.digit_set)

    @property
    def digit_set(self) -> frozenset[T]:
        return frozenset(get_args(self.digit_type))

    @property
    def box_side(self) -> int:
        bs = int(math.sqrt(self.N))
        if bs**2 != self.N:
            raise ValueError("Grid size must be a perfect square")
        return bs

    @classmethod
    def from_value_matrix(cls, value_matrix: Sequence[Sequence], digit_type=None):
        if digit_type is None:
            digit_type = NineDigits

        N = len(frozenset(get_args(digit_type)))
        rows = []
        for values in value_matrix:
            v_tuple = tuple(values)
            if len(v_tuple) != N:
                raise ValueError("Grid row has faulty length")
            rows.append(Unit(values=v_tuple, digit_type=digit_type))
        if len(rows) != N:
            raise ValueError("Grid has faulty number of rows")
        return cls(rows=tuple(rows), digit_type=digit_type)

    @classmethod
    def from_csv_file(cls, path: Union[Path, str], delimiter=",", digit_type=None):
        if digit_type is None:
            digit_type = NineDigits
        with open(path) as csv:
            value_matrix = [
                [int(x.strip()) for x in line]
                for raw_line in csv.readlines()
                if (line := raw_line.strip("\n ").split(delimiter))[0]
            ]
        return cls.from_value_matrix(value_matrix, digit_type)

    @classmethod
    def from_string(cls, grid_string: str, digit_type=None):
        if digit_type is None:
            digit_type = NineDigits
        N = len(frozenset(get_args(digit_type)))
        clean = "".join(c if c != "." else "0" for c in grid_string if c not in " \n\t")
        if len(clean) != N * N:
            raise ValueError(f"Grid string must contain exactly {N * N} values")
        return cls.from_value_matrix(
            [
                [int(c) if c.isdigit() else c for c in clean[i : i + N]]
                for i in range(0, N * N, N)
            ],
            digit_type,
        )

    @classmethod
    def construct_empty(cls, digit_type=None):
        if digit_type is None:
            digit_type = NineDigits
        N = len(frozenset(get_args(digit_type)))
        return cls(
            rows=tuple(Unit(values=(0,) * N, digit_type=digit_type) for _ in range(N)),
            digit_type=digit_type,
        )

    def with_placement(self, cell: Cell) -> Grid[T]:
        row, col = cell.position
        changed_unit = self.Unit(
            values=tuple(
                cell.value if i == col else v for i, v in enumerate(self.rows[row])
            ),
        )
        return Grid(
            digit_type=self.digit_type,
            rows=(
                tuple(
                    tuple(self.rows[:row])
                    + (changed_unit,)
                    + tuple(self.rows[row + 1 :])
                )
            ),
        )

    def get_candidates(self, position: Position) -> set[T]:
        return (
            self.get_row(position).get_candidates()
            & self.get_col(position).get_candidates()
            & self.get_box(position).get_candidates()
        )

    def iter_positions(
        self, value_or_predicate: Union[CellValue, Callable[[CellValue], bool]] = 0
    ) -> Iterator[Position]:
        for row_index, unit in enumerate(self.iter_rows()):
            for col_index, val in enumerate(unit):
                if (
                    callable(value_or_predicate) and value_or_predicate(val)
                ) or val == value_or_predicate:
                    yield row_index, col_index

    def get_cell(self, position: Position) -> CellValue:
        row, col = position
        return self.rows[row][col]

    def get_row(self, position: Position) -> Unit[T]:
        row, _ = position
        return self.rows[row]

    def get_col(self, position: Position) -> Unit[T]:
        _, col = position
        return self.Unit(
            values=tuple(self.rows[i][col] for i in range(self.N)),
        )

    def get_box(self, position: Position) -> Unit[T]:
        return Unit(
            values=tuple(
                self.rows[row][col] for row, col in self.get_box_positions(position)
            ),
            digit_type=self.digit_type,
        )

    def get_box_positions(self, position: Position) -> Iterator[Position]:
        row, col = position
        bs = self.box_side
        start_row = (row // bs) * bs
        start_col = (col // bs) * bs
        return ((start_row + r, start_col + c) for r in range(bs) for c in range(bs))

    def iter_rows(self) -> Iterator[Unit[T]]:
        return iter(self.rows)

    def iter_cols(self) -> Iterator[Unit[T]]:
        for i in range(self.N):
            yield self.get_col((0, i))

    def iter_boxes(self) -> Iterator[Unit[T]]:
        bs = self.box_side
        for row_offset in range(0, self.N, bs):
            for col_offset in range(0, self.N, bs):
                yield self.get_box((row_offset, col_offset))

    def is_valid(self) -> bool:
        return all(u.is_valid() for u in self.rows)

    def is_complete(self) -> bool:
        return all(unit.is_complete() for unit in self.rows)

    def count_digit(self, digit: CellValue) -> int:
        return len(list(self.iter_positions(digit)))

    def count_filled(self) -> int:
        return self.N**2 - self.count_digit(0)

    def __eq__(self, other: Grid):
        return (
            isinstance(other, BaseGrid)
            and self.digit_type == other.digit_type
            and all(
                own_unit == other_unit
                for own_unit, other_unit in zip(self.iter_rows(), other.iter_rows())
            )
        )

    def to_string(self) -> str:
        """Serialize the grid to a compact string."""
        return "".join(str(val) for row in self.rows for val in row)

    def rotate(self) -> Grid[T]:
        """Return a new grid rotated 90 degrees clockwise."""

        return self.from_value_matrix(
            [
                [self.rows[self.N - 1 - j][i] for j in range(self.N)]
                for i in range(self.N)
            ],
            self.digit_type,
        )

    def __str__(self):
        def format_unit(unit):
            return " ".join(
                f" {v}" if not i % self.box_side else str(v)
                for i, v in enumerate(unit.values)
            )

        return f"Board: {self.count_digit(0)}/{self.count_filled()}" + "\n".join(
            f"\n{v}" if not i % self.box_side else str(v)
            for i, v in enumerate(format_unit(u) for u in self.rows)
        )
