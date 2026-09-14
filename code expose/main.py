"""Point d'entrée. Usage : python main.py adult_train.csv"""

from __future__ import annotations

import sys

from data_loader import load_csv
from skiplist import SkipList
from rbtree import RedBlackTree
from database import Database
from compare_perf import run_all


def demo(db: Database, label: str) -> None:
    print(f"\n--- requêtes [{label}] ---")
    print(f"find_by_id(42)            -> {db.find_by_id(42)}")

    aged_30 = db.find_by_age(30)
    print(f"find_by_age(30)           -> {len(aged_30)} personnes")

    aged_25_30 = db.find_by_age_range(25, 30)
    print(f"find_by_age_range(25,30)  -> {len(aged_25_30)} personnes")

    n_high = db.count_high_income_in_age_range(40, 50)
    avg_h = db.average_hours_in_age_range(40, 50)
    print(f"tranche 40-50 ans :")
    print(f"  - revenus >50K : {n_high}")
    print(f"  - heures hebdo moyennes : {avg_h:.1f}")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage : python main.py adult_train.csv")
        sys.exit(1)

    path = sys.argv[1]
    people = load_csv(path)
    print(f"{len(people)} lignes chargées depuis {path}")

    db_skip = Database.build(people, lambda: SkipList(max_level=20, seed=42))
    db_rb = Database.build(people, RedBlackTree)

    demo(db_skip, "SkipList")
    demo(db_rb, "RedBlackTree")

    a = len(db_skip.find_by_age_range(25, 30))
    b = len(db_rb.find_by_age_range(25, 30))
    assert a == b, f"incohérence : skip-list={a}, rbtree={b}"
    print("\nLes deux structures renvoient les mêmes résultats.")

    print("\n" + "-" * 50)
    print("BENCHMARK")
    print("-" * 50)
    run_all(people)


if __name__ == "__main__":
    main()
