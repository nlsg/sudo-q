import time

from sudoq import Grid
from sudoq.core import HexDigits, NineDigits
from sudoq.generators import PuzzleGenerator, DigitReducer, RandomCellReducer

generator = PuzzleGenerator(
    reducers=(
        DigitReducer(digit=4, keep_count=0),  # First reduce digit 4
        DigitReducer(digit=7, keep_count=2),  # Then reduce digit 7
        RandomCellReducer(),  # Finally randomly reduce remaining cells
    ),
    min_clues=17,
)

n = 0
max_empties = 0
start = time.perf_counter()
digit_type = NineDigits
digit_type = HexDigits
try:
    while True:
        t = time.perf_counter()
        puzzle = generator.generate(Grid.construct_empty(digit_type), tries=1)
        print(puzzle)
        max_empties = max(max_empties, puzzle.count_digit(0))
        n += 1
        print(
            f"[{n}] took: {time.perf_counter() - t:.2f}s \n {(time.perf_counter() - start) / n:.2f} s/sudoku\n {max_empties=}\n"
        )
except KeyboardInterrupt:
    end = t - start
    print(f"{n=}, t={end:.2f}s | {end / n:.2f} s/sudoku")
    print(f"{max_empties=}")
