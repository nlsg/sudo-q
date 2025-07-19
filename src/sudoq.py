from typing import Literal, Tuple, TypeVar, Iterator, get_args, Annotated
from dataclasses import dataclass

T = TypeVar("T")
Nine = Tuple[T, T, T, T, T, T, T, T, T]

Digit = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
Index = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8]

Position = Annotated[Tuple[Index, Index], "row, column"]


@dataclass(frozen=True)
class Unit:
    values: Nine[Digit]

    def is_valid(self):
        return len(self.values) == 9 and all(
            self.values.count(i) <= 1 for i in range(1, 10)
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
