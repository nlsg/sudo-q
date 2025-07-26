from context import Grid, generators, solvers


def test_generate_complete():
    grid = generators.BasicPuzzleGenerator().fill_grid(grid=Grid.construct_empty())
    assert grid.is_valid()
    assert len(list(grid.iter_positions(0))) == 0
    assert grid.is_complete()


def test_generate_easy_puzzle():
    puzzle = generators.BasicPuzzleGenerator().generate()
    assert puzzle.is_valid()
    assert not puzzle.is_complete()
    assert solvers.BacktrackingSolver().solve(puzzle).is_complete()
