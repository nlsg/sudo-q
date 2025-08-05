from typing import Literal, Tuple, TypeVar, get_args, Annotated, Iterator
from dataclasses import dataclass
import itertools

T = TypeVar("T")
Nine = Tuple[T, T, T, T, T, T, T, T, T]

Digit = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
Index = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8]

Position = Annotated[Tuple[Index, Index], "row, column"]


DIGITS = set(get_args(Digit)) - {0}


@dataclass(frozen=True)
class Cell:
    position: Position
    value: Digit

    def is_empty(self) -> bool:
        return self.value == 0


def iter_row_positions() -> Iterator[list[Position]]:
    return ([(row, col) for col in range(9)] for row in range(9))


def iter_col_positions() -> Iterator[list[Position]]:
    return ([(row, col) for row in range(9)] for col in range(9))


def iter_box_positions() -> Iterator[list[Position]]:
    return (
        [(r + dr, c + dc) for dr in range(3) for dc in range(3)]
        for r in (0, 3, 6)
        for c in (0, 3, 6)
    )


def iter_unit_positions() -> Iterator[list[Position]]:
    return itertools.chain(
        iter_row_positions(), iter_col_positions(), iter_box_positions()
    )
