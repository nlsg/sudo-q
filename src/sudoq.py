from typing import Literal, Tuple, TypeVar, Iterator, get_args
from dataclasses import dataclass

T = TypeVar("T")
Nine = Tuple[T, T, T, T, T, T, T, T, T]

Digit = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
Index = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8]

Position = Tuple[Index, Index]


@dataclass(frozen=True)
class Unit:
    values: Nine[Digit]

    def is_valid(self):
        return len(self.values) == 9 and all(
            self.values.count(i) <= 1 for i in range(1, 10)
        )


@dataclass(frozen=True)
class Board:
    rows: list[Unit]

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

    def iter_rows(self) -> Iterator[Unit]:
        for row in self.rows:
            yield row

    def iter_cols(self) -> Iterator[Unit]:
        for i in get_args(Index):
            yield Unit(values=[self.rows[j].values[i] for j in get_args(Index)])

    def iter_boxes(self) -> Iterator[Unit]:
        for row_offset in 0, 3, 6:
            for col_offset in 0, 3, 6:
                yield Unit(
                    values=list(
                        self.rows[row_offset + i].values[col_offset + r]
                        for i in range(3)
                        for r in range(3)
                    )
                )
    def is_valid(self):
        return all(u.is_valid() for u in self.rows)
