from context import Board
import time


def test_generate_solved():
    start_time = time.perf_counter()
    count = 1
    board = Board.construct_empty().generate_solved()
    assert board.is_valid()
    assert len(list(board.iter_positions(0))) == 0
    assert board.is_solved()
    duration = time.perf_counter() - start_time
    print(
        f"generated {count} solved boards in {duration:.3}s ( {duration / count:.3}s / per borad)"
    )
