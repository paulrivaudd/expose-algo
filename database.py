"""Petite base de données indexée par une structure ordonnée
(skip-list ou red-black tree, au choix)."""

from __future__ import annotations

from typing import Callable, Generic, Protocol, TypeVar

from data_loader import Person


K = TypeVar("K")
V = TypeVar("V")


class Index(Protocol, Generic[K, V]):
    """Interface commune à la skip-list et au RB-tree."""
    def insert(self, key: K, value: V) -> None: ...
    def search(self, key: K) -> V | None: ...
    def search_all(self, key: K) -> list[V]: ...
    def range_search(self, low: K, high: K) -> list[V]: ...
    def __len__(self) -> int: ...


class Database:

    def __init__(self,
                 id_index: Index[int, Person],
                 age_index: Index[int, Person]) -> None:
        self.id_index = id_index
        self.age_index = age_index

    @classmethod
    def build(cls,
              people: list[Person],
              index_factory: Callable[[], Index[int, Person]]) -> "Database":
        id_idx = index_factory()
        age_idx = index_factory()
        for p in people:
            id_idx.insert(p.id, p)
            age_idx.insert(p.age, p)
        return cls(id_idx, age_idx)

    def find_by_id(self, person_id: int) -> Person | None:
        return self.id_index.search(person_id)

    def find_by_age(self, age: int) -> list[Person]:
        return self.age_index.search_all(age)

    def find_by_age_range(self, min_age: int, max_age: int) -> list[Person]:
        return self.age_index.range_search(min_age, max_age)

    def count_high_income_in_age_range(self, min_age: int,
                                       max_age: int) -> int:
        return sum(1 for p in self.find_by_age_range(min_age, max_age)
                   if p.income == ">50K")

    def average_hours_in_age_range(self, min_age: int,
                                   max_age: int) -> float:
        people = self.find_by_age_range(min_age, max_age)
        if not people:
            return 0.0
        return sum(p.hours_per_week for p in people) / len(people)
