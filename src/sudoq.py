from typing import Literal, Tuple, TypeVar, Iterator, get_args, Annotated
from dataclasses import dataclass

T = TypeVar("T")
Nine = Tuple[T, T, T, T, T, T, T, T, T]

Digit = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
Index = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8]

Position = Annotated[Tuple[Index, Index], "row, column"]


DIGITS = set(get_args(Digit)) - {0}


@dataclass(frozen=True)
class Unit:
    values: Nine[Digit]

    def is_valid(self):
        return len(self.values) == 9 and all(
            self.values.count(i) <= 1 for i in range(1, 10)
        )

    def is_complete(self) -> bool:
        return 0 not in self.values

    def get_filled_values(self) -> set[Digit]:
        return set(self.values) - {0}

    def get_candidates(self) -> set[Digit]:
        return DIGITS - self.get_filled_values()

    def __eq__(self, other: "Unit"):
        return isinstance(other, Unit) and all(
            s == o for s, o in zip(self.values, other.values)
        )


@dataclass(frozen=True)
class Board:
    rows: Nine[Unit]

    @classmethod
    def from_csv_file(cls, path: str, delimiter=",") -> "Board":
        with open(path) as csv:
            return cls(
                rows=tuple(
                    Unit(list(map(int, line)))
                    for raw_line in csv.readlines()
                    if (line := raw_line.strip("\n ").split(delimiter))[0]
                )
            )

    @classmethod
    def construct_empty(cls) -> "Board":
        return cls(rows=[Unit(values=[0] * 9)] * 9)

    def with_placement(self, position: Position, value: Digit) -> "Board":
        row, col = position
        changed_unit = Unit(
            values=[
                value if i == col else v for i, v in enumerate(self.rows[row].values)
            ]
        )
        return Board(
            rows=(list(self.rows[:row]) + [changed_unit] + list(self.rows[row + 1 :]))
        )

    def solve_step(self) -> "Board":
        for position in self.iter_empty_positions():
            candidates = self.get_candidates(position)
            if len(candidates) == 1:
                return self.with_placement(position, next(iter(candidates)))
        return self

    def solve(self) -> "Board":
        board = self
        while not board.is_solved():
            board = board.solve_step()
        return board

    def solve_backtracking(self) -> "Board":
        if not (position := next(self.iter_empty_positions(), None)):
            return self
        for candidate in self.get_candidates(position):
            board = self.with_placement(position, candidate).solve_backtracking()
            if board.is_solved():
                return board
        return self

    def get_candidates(self, position: Position) -> set[Digit]:
        return (
            self.get_row(position).get_candidates()
            & self.get_col(position).get_candidates()
            & self.get_box(position).get_candidates()
        )

    def iter_empty_positions(self) -> Iterator[Position]:
        for row_index, unit in enumerate(self.iter_rows()):
            for col_index, value in enumerate(unit.values):
                if not value:
                    yield row_index, col_index

    def get_cell(self, position: Position) -> Digit:
        row, col = position
        return self.rows[row].values[col]

    def get_row(self, position: Position) -> Unit:
        row, _ = position
        return self.rows[row]

    def get_col(self, position: Position) -> Unit:
        _, col = position
        return Unit(values=[self.rows[i].values[col] for i in get_args(Index)])

    def get_box(self, position: Position) -> Unit:
        row, col = position
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        return Unit(
            values=list(
                self.rows[start_row + r].values[start_col + c]
                for r in range(3)
                for c in range(3)
            )
        )

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

    def __eq__(self, other: "Board"):
        return isinstance(other, Board) and all(
            own_unit == other_unit
            for own_unit, other_unit in zip(self.iter_rows(), other.iter_rows())
        )

    def __str__(self):
        empty_cells = len(list(self.iter_empty_positions()))

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
