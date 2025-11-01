from multiprocessing import Process, Queue
import time
import random
import itertools
from typing import TypedDict, Literal, get_args
import string
import unicodedata
from sudoq import Grid, HexDigits, protocols, Cell
from sudoq.solvers import BacktrackingSolver

empty_grid = Grid.construct_empty(digit_type=HexDigits)


queue = Queue()


class Msg(TypedDict):
    grid: Grid
    duration: float
    name: str


def run_solver(name, solver: protocols.Solver, queue: Queue, grid: Grid):
    start = time.perf_counter()
    g = solver.solve(grid)
    msg: Msg = {
        "grid": g,
        "duration": time.perf_counter() - start,
        "name": name,
    }
    queue.put(msg)
    return msg


def apply_random_reduction(grid: Grid) -> Grid:
    if random.random() > 0.33:
        return grid
    return grid.with_placement(
        Cell(
            (
                random.randint(0, grid.N),
                random.randint(0, grid.N),
            ),
            value=0,
        )
    )


solvers = {
    "plain": BacktrackingSolver(),
    "random-candidate": BacktrackingSolver(
        candidate_hook=lambda s: random.sample(tuple(s), len(s))
    ),
    "random-position": BacktrackingSolver(
        position_chooser=lambda p, *_: random.choice(list(p)),
    ),
    "rotation": BacktrackingSolver(solve_step_hook=Grid.rotate),
    "random-position-candidate": BacktrackingSolver(
        position_chooser=lambda p, *_: random.choice(list(p)),
        candidate_hook=lambda s: random.sample(tuple(s), len(s)),
    ),
    "random-reduction": BacktrackingSolver(solve_step_hook=apply_random_reduction),
}


def unique_char_iterator():
    yield from string.digits
    yield from string.ascii_lowercase
    yield from (
        chr(i)
        for i in range(32, 0x10000)
        if chr(i).isprintable()
        and not chr(i).isalnum()
        and unicodedata.category(chr(i)).startswith(("S", "P"))
    )


def yield_sets():
    unique_gen = unique_char_iterator()
    for i in range(2, 10):
        n = i**2
        yield Literal[tuple(itertools.islice(unique_gen, n))]


def print_queue(queue: Queue, i: int):
    msg: Msg = queue.get()
    print(f"{i} | {msg['duration']:.2f}s | {msg['name']}")
    print(msg["grid"])
    print()
    print()


def run_parallel(grid: Grid):
    processes = [
        Process(target=run_solver, args=(name, solver, queue, grid))
        for name, solver in solvers.items()
    ]
    for p in processes:
        p.start()

    for i in range(len(processes)):
        print_queue(queue, i)
    for p in processes:
        p.join()


def run_sequential(grid: Grid):
    for name, solver in solvers.items():
        run_solver(name, solver, queue, grid)
        print_queue(queue, 0)


for i, typ in enumerate(yield_sets()):
    print(f"T{i} | ... | ( {len(get_args(typ))} ) {typ}")
    t1 = time.perf_counter()
    run_parallel(Grid.construct_empty(typ))
    # run_sequential(Grid.construct_empty(typ))
    print(f"T{i} | {time.perf_counter() - t1:.2f}s | ( {len(get_args(typ))} ) {typ}")
    print()
    print()
