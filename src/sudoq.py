from typing import Literal, Tuple, TypeVar
from dataclasses import dataclass

T = TypeVar("T")
Nine = Tuple[T, T, T, T, T, T, T, T, T]

Digit = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
Index = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8]

Position = Tuple[Index, Index]


@dataclass
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

    def is_valid(self):
        return all(u.is_valid() for u in self.rows)
