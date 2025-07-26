from context import Grid, generators, solvers
import time


def test_generate_solved():
    start_time = time.perf_counter()
    count = 1
    board = Grid.construct_empty().generate_solved()
    assert board.is_valid()
    assert len(list(board.iter_positions(0))) == 0
    assert board.is_complete()
    duration = time.perf_counter() - start_time
    print(
        f"generated {count} solved boards in {duration:.3}s ( {duration / count:.3}s / per borad)"
    )


def test_generate_easy_puzzle():
    puzzle = generators.BasicPuzzleGenerator().generate()
    assert puzzle.is_valid()
    assert not puzzle.is_complete()
    assert solvers.BacktrackingSolver().solve(puzzle).is_complete()
    print(puzzle)
