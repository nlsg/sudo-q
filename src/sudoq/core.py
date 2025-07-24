from typing import Literal, Tuple, TypeVar, get_args, Annotated

T = TypeVar("T")
Nine = Tuple[T, T, T, T, T, T, T, T, T]

Digit = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
Index = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8]

Position = Annotated[Tuple[Index, Index], "row, column"]


DIGITS = set(get_args(Digit)) - {0}
