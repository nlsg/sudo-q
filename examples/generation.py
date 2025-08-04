from sudoq.generators import PuzzleGenerator, DigitReducer, RandomCellReducer

generator = PuzzleGenerator(
    reducers=(
        DigitReducer(digit=4, keep_count=0),  # First reduce digit 4
        DigitReducer(digit=7, keep_count=2),  # Then reduce digit 7
        RandomCellReducer(),  # Finally randomly reduce remaining cells
    ),
    min_clues=17,
)

puzzle = generator.generate()
print(generator.generate())
pass
