from collections.abc import Sequence
from dataclasses import dataclass

from .core import Digit, Nine, DIGITS


@dataclass(frozen=True)
class Unit(Sequence):
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

    def __iter__(self):
        return iter(self.values)

    def __len__(self):
        return len(self.values)

    def __getitem__(self, index):
        return self.values[index]

    def __contains__(self, item):
        return item in self.values
