import pytest
from context import Grid, generators, reducers, solvers, Cell


def test_generate_complete():
    grid = generators.PuzzleGenerator(
        reducers=[reducers.RandomCellReducer()]
    ).fill_grid(grid=Grid.construct_empty())
    assert grid.is_valid()
    assert grid.count_digit(0) == 0
    assert grid.is_complete()


def test_unique_filling():
    amount = 3
    assert (
        len(
            {
                hash(
                    generators.PuzzleGenerator(
                        reducers=[reducers.RandomCellReducer()]
                    ).fill_grid(grid=Grid.construct_empty())
                )
                for _ in range(amount)
            }
        )
        == amount
    )


def test_random_cell_reducer():
    reducer = reducers.RandomCellReducer()
    grid = Grid.construct_empty().with_placement(Cell(position=(0, 0), value=5))

    # Should select the only filled position
    assert reducer.select_position(grid) == (0, 0)

    assert reducer.select_position(Grid.construct_empty()) is None


def test_digit_reducer():
    reducer = reducers.DigitReducer(digit=4, keep_count=2)

    grid = Grid.construct_empty()
    positions = [(0, 0), (1, 1), (2, 2)]
    for pos in positions:
        grid = grid.with_placement((Cell(position=pos, value=4)))

    pos = reducer.select_position(grid)
    assert pos in positions

    grid = grid.with_placement(Cell(position=pos, value=0))

    # Should not reduce further as we want to keep 2
    assert reducer.select_position(grid) is None


def test_composite_reducer():
    reducer1 = reducers.DigitReducer(digit=4, keep_count=1)
    reducer2 = reducers.RandomCellReducer()
    composite = reducers.CompositeReducer([reducer1, reducer2])

    grid = Grid.construct_empty()
    grid = grid.with_placement(Cell(position=(0, 0), value=4))
    grid = grid.with_placement(Cell(position=(1, 1), value=5))

    # First reducer should not select anything (keep_count=1)
    # Second reducer should select a random filled cell
    assert composite.select_position(grid) in [(0, 0), (1, 1)]


def test_puzzle_generator():
    generator = generators.PuzzleGenerator(
        reducers=[reducers.RandomCellReducer()],
        solver=solvers.StrategicSolver(),
        min_clues=17,
    )

    puzzle = generator.generate()

    assert puzzle.is_valid()
    assert puzzle.count_filled() >= 17
    assert solvers.StrategicSolver().solve(puzzle).is_complete()


def test_puzzle_generator_with_digit_reducer():
    generator = generators.PuzzleGenerator(
        reducers=[
            reducers.DigitReducer(digit=4, keep_count=1),
            reducers.RandomCellReducer(),
        ],
        min_clues=17,
    )

    puzzle = generator.generate()

    assert puzzle.is_valid()
    assert puzzle.count_filled() >= 17
    assert sum(1 for _ in puzzle.iter_positions(4)) == 1
    assert solvers.StrategicSolver().solve(puzzle).is_complete()


@pytest.mark.parametrize("min_clues", [17, 20, 80])
def test_puzzle_generator_respects_min_clues(min_clues):
    generator = generators.PuzzleGenerator(
        reducers=[reducers.RandomCellReducer()], min_clues=min_clues
    )

    puzzle = generator.generate()
    assert puzzle.count_filled() >= min_clues


def test_puzzle_generator_with_input_grid():
    input_grid = Grid.construct_empty().with_placement(Cell(position=(0, 0), value=5))
    generator = generators.PuzzleGenerator(reducers=[reducers.RandomCellReducer()])

    puzzle = generator.generate(input_grid)
    assert puzzle.is_valid()
    assert puzzle.get_cell((0, 0)) in (5, 0)  # Either kept or reduced
