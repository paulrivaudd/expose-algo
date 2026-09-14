"""Mesures comparatives skip-list vs red-black tree."""

from __future__ import annotations

import random
import time
from dataclasses import dataclass
from typing import Callable

from data_loader import Person
from skiplist import SkipList
from rbtree import RedBlackTree


@dataclass
class BenchResult:
    name: str
    n: int
    build_time: float
    search_time: float
    range_time: float
    info: str


def bench(name: str,
          factory: Callable[[], object],
          people: list[Person],
          n_searches: int = 1000,
          seed: int = 42) -> BenchResult:
    rng = random.Random(seed)

    structure = factory()
    t0 = time.perf_counter()
    for p in people:
        structure.insert(p.age, p)  # type: ignore[attr-defined]
    build_time = time.perf_counter() - t0

    keys = [rng.choice(people).age for _ in range(n_searches)]
    t0 = time.perf_counter()
    for k in keys:
        structure.search(k)  # type: ignore[attr-defined]
    search_time = time.perf_counter() - t0

    intervals = [(a := rng.randint(17, 80), a + rng.randint(1, 10))
                 for _ in range(100)]
    t0 = time.perf_counter()
    for a, b in intervals:
        structure.range_search(a, b)  # type: ignore[attr-defined]
    range_time = time.perf_counter() - t0

    if isinstance(structure, SkipList):
        info = f"niveau {structure.level}/{structure.max_level}"
    elif isinstance(structure, RedBlackTree):
        info = f"h={structure.height()}, bh={structure.black_height()}"
    else:
        info = ""

    return BenchResult(name, len(people), build_time,
                       search_time, range_time, info)


def run_all(people: list[Person]) -> list[BenchResult]:
    results: list[BenchResult] = []
    sizes = [s for s in (1_000, 5_000, 10_000, len(people))
             if s <= len(people)]

    for n in sizes:
        subset = people[:n]
        print(f"\nn = {n}")
        r1 = bench(f"SkipList (n={n})",
                   lambda: SkipList(max_level=20, seed=42), subset)
        r2 = bench(f"RedBlackTree (n={n})", RedBlackTree, subset)
        results.extend([r1, r2])
        _print_pair(r1, r2)
    return results


def _print_pair(a: BenchResult, b: BenchResult) -> None:
    print(f"{'':<25}{'build (s)':>12}{'search (ms)':>14}{'range (ms)':>14}   info")
    for r in (a, b):
        print(f"{r.name:<25}{r.build_time:>12.4f}"
              f"{r.search_time*1000:>14.2f}"
              f"{r.range_time*1000:>14.2f}   {r.info}")
