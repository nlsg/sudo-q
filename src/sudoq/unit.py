from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import TypeVar, Generic, get_args
from .core import NineDigits


T = TypeVar("T")


@dataclass(frozen=True)
class Unit(Sequence, Generic[T]):
    values: tuple[T, ...]
    digit_type: type[T] = field(default=NineDigits)

    @property
    def digit_set(self) -> frozenset[T]:
        return frozenset(get_args(self.digit_type))

    def is_valid(self):
        N = len(self.digit_set)
        return len(self.values) == N and all(
            self.values.count(d) <= 1 for d in self.digit_set if d != 0
        )

    def is_complete(self) -> bool:
        return 0 not in self.values

    def get_filled_values(self) -> set[T]:
        return set(self.values) - {0}

    def get_candidates(self) -> set[T]:
        return self.digit_set - self.get_filled_values()

    def __eq__(self, other: "Unit"):
        return isinstance(other, Unit) and all(
            s == o for s, o in zip(self.values, other.values)
        )

    def __iter__(self):
        return iter(self.values)

    def __len__(self):
        return len(self.values)

    def __getitem__(self, index):
        return self.values[index]

    def __contains__(self, item):
        return item in self.values
