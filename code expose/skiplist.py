"""Skip-list triée, doublons autorisés.

Une skip-list est une liste chaînée triée à plusieurs niveaux.
Le niveau 0 contient tous les éléments. Chaque niveau supérieur est
une sous-liste tirée aléatoirement (proba p de monter d'un cran),
ce qui donne des "raccourcis" pour la recherche.

Recherche / insertion : O(log n) en moyenne.
"""

from __future__ import annotations

import random
from typing import Generic, Iterator, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class _Node(Generic[K, V]):
    __slots__ = ("key", "value", "forward")

    def __init__(self, key: K, value: V, level: int) -> None:
        self.key: K = key
        self.value: V = value
        self.forward: list[_Node[K, V] | None] = [None] * (level + 1)


class SkipList(Generic[K, V]):

    def __init__(self, max_level: int = 16, p: float = 0.5,
                 seed: int | None = None) -> None:
        self.max_level = max_level
        self.p = p
        self.level = 0
        self._size = 0
        self.head: _Node[K, V] = _Node(
            key=None, value=None, level=max_level  # type: ignore[arg-type]
        )
        self._rng = random.Random(seed)

    def __len__(self) -> int:
        return self._size

    def __contains__(self, key: K) -> bool:
        return self.search(key) is not None

    def __iter__(self) -> Iterator[tuple[K, V]]:
        node = self.head.forward[0]
        while node is not None:
            yield node.key, node.value
            node = node.forward[0]

    def _random_level(self) -> int:
        lvl = 0
        while self._rng.random() < self.p and lvl < self.max_level:
            lvl += 1
        return lvl

    def insert(self, key: K, value: V) -> None:
        update: list[_Node[K, V]] = [self.head] * (self.max_level + 1)
        current = self.head

        for i in range(self.level, -1, -1):
            while (current.forward[i] is not None
                   and current.forward[i].key < key):  # type: ignore[operator]
                current = current.forward[i]  # type: ignore[assignment]
            update[i] = current

        lvl = self._random_level()
        if lvl > self.level:
            for i in range(self.level + 1, lvl + 1):
                update[i] = self.head
            self.level = lvl

        new_node = _Node(key, value, lvl)
        for i in range(lvl + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

        self._size += 1

    def search(self, key: K) -> V | None:
        current = self.head
        for i in range(self.level, -1, -1):
            while (current.forward[i] is not None
                   and current.forward[i].key < key):  # type: ignore[operator]
                current = current.forward[i]  # type: ignore[assignment]
        candidate = current.forward[0]
        if candidate is not None and candidate.key == key:
            return candidate.value
        return None

    def search_all(self, key: K) -> list[V]:
        """Toutes les valeurs ayant cette clé (utile quand il y a des doublons)."""
        result: list[V] = []
        current = self.head
        for i in range(self.level, -1, -1):
            while (current.forward[i] is not None
                   and current.forward[i].key < key):  # type: ignore[operator]
                current = current.forward[i]  # type: ignore[assignment]
        node = current.forward[0]
        while node is not None and node.key == key:
            result.append(node.value)
            node = node.forward[0]
        return result

    def range_search(self, low: K, high: K) -> list[V]:
        """Toutes les valeurs dont la clé est dans [low, high]."""
        result: list[V] = []
        current = self.head
        for i in range(self.level, -1, -1):
            while (current.forward[i] is not None
                   and current.forward[i].key < low):  # type: ignore[operator]
                current = current.forward[i]  # type: ignore[assignment]
        node = current.forward[0]
        while node is not None and node.key <= high:  # type: ignore[operator]
            result.append(node.value)
            node = node.forward[0]
        return result
