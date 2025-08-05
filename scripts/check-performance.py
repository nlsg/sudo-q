import timeit
from sudoq import Grid
from sudoq.solvers import BacktrackingSolver


def check_performance():
    time = min(
        timeit.repeat(
            lambda: BacktrackingSolver().solve(Grid.construct_empty()),
            number=1,
            repeat=3,
        )
    )
    if time > 0.01:
        print(f"Performance regression detected: {time:.2f}s")
        return 1
    return 0


if __name__ == "__main__":
    exit(check_performance())
