"""Arbre rouge-noir (BST auto-équilibré).

Invariants :
1. Chaque nœud est rouge ou noir.
2. La racine est noire.
3. Les feuilles (NIL) sont noires.
4. Un nœud rouge n'a que des enfants noirs.
5. Tout chemin d'un nœud à une feuille a le même nombre de noirs.

Hauteur bornée par 2*log2(n+1) → insertion et recherche en O(log n)
dans le pire cas. Implémentation suivant CLRS avec sentinelle NIL.
"""

from __future__ import annotations

from typing import Generic, Iterator, TypeVar

K = TypeVar("K")
V = TypeVar("V")

RED = True
BLACK = False


class _Node(Generic[K, V]):
    __slots__ = ("key", "value", "color", "left", "right", "parent")

    def __init__(self, key: K, value: V, color: bool = RED) -> None:
        self.key: K = key
        self.value: V = value
        self.color = color
        self.left: _Node[K, V] = None  # type: ignore[assignment]
        self.right: _Node[K, V] = None  # type: ignore[assignment]
        self.parent: _Node[K, V] = None  # type: ignore[assignment]


class RedBlackTree(Generic[K, V]):

    def __init__(self) -> None:
        self.NIL: _Node[K, V] = _Node(
            key=None, value=None, color=BLACK  # type: ignore[arg-type]
        )
        self.NIL.left = self.NIL
        self.NIL.right = self.NIL
        self.NIL.parent = self.NIL
        self.root: _Node[K, V] = self.NIL
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def __contains__(self, key: K) -> bool:
        return self.search(key) is not None

    def __iter__(self) -> Iterator[tuple[K, V]]:
        yield from self._inorder(self.root)

    def _inorder(self, node: _Node[K, V]) -> Iterator[tuple[K, V]]:
        if node is self.NIL:
            return
        yield from self._inorder(node.left)
        yield node.key, node.value
        yield from self._inorder(node.right)

    def search(self, key: K) -> V | None:
        node = self.root
        while node is not self.NIL:
            if key == node.key:
                return node.value
            node = node.left if key < node.key else node.right  # type: ignore[operator]
        return None

    def search_all(self, key: K) -> list[V]:
        result: list[V] = []
        self._collect_equal(self.root, key, result)
        return result

    def _collect_equal(self, node: _Node[K, V], key: K,
                       acc: list[V]) -> None:
        # Les rotations peuvent déplacer des doublons à gauche d'un nœud
        # de même clé, donc on explore les deux côtés en cas d'égalité.
        if node is self.NIL:
            return
        if key < node.key:  # type: ignore[operator]
            self._collect_equal(node.left, key, acc)
        elif key > node.key:  # type: ignore[operator]
            self._collect_equal(node.right, key, acc)
        else:
            acc.append(node.value)
            self._collect_equal(node.left, key, acc)
            self._collect_equal(node.right, key, acc)

    def range_search(self, low: K, high: K) -> list[V]:
        result: list[V] = []
        self._range(self.root, low, high, result)
        return result

    def _range(self, node: _Node[K, V], low: K, high: K,
               acc: list[V]) -> None:
        if node is self.NIL:
            return
        if low <= node.key:  # type: ignore[operator]
            self._range(node.left, low, high, acc)
        if low <= node.key <= high:  # type: ignore[operator]
            acc.append(node.value)
        if node.key <= high:  # type: ignore[operator]
            self._range(node.right, low, high, acc)

    def insert(self, key: K, value: V) -> None:
        z = _Node(key, value, color=RED)
        z.left = self.NIL
        z.right = self.NIL
        z.parent = self.NIL

        y = self.NIL
        x = self.root
        while x is not self.NIL:
            y = x
            x = x.left if z.key < x.key else x.right  # type: ignore[operator]

        z.parent = y
        if y is self.NIL:
            self.root = z
        elif z.key < y.key:  # type: ignore[operator]
            y.left = z
        else:
            y.right = z

        self._insert_fixup(z)
        self._size += 1

    def _insert_fixup(self, z: _Node[K, V]) -> None:
        while z.parent.color == RED:
            if z.parent is z.parent.parent.left:
                y = z.parent.parent.right  # oncle
                if y.color == RED:
                    # cas 1 : oncle rouge → recoloration, on remonte
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z is z.parent.right:
                        # cas 2 → rotation pour ramener à cas 3
                        z = z.parent
                        self._left_rotate(z)
                    # cas 3
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self._right_rotate(z.parent.parent)
            else:
                # cas symétriques (parent à droite)
                y = z.parent.parent.left
                if y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z is z.parent.left:
                        z = z.parent
                        self._right_rotate(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self._left_rotate(z.parent.parent)
        self.root.color = BLACK

    def _left_rotate(self, x: _Node[K, V]) -> None:
        y = x.right
        x.right = y.left
        if y.left is not self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is self.NIL:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, x: _Node[K, V]) -> None:
        y = x.left
        x.left = y.right
        if y.right is not self.NIL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is self.NIL:
            self.root = y
        elif x is x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def black_height(self) -> int:
        h = 0
        node = self.root
        while node is not self.NIL:
            if node.color == BLACK:
                h += 1
            node = node.left
        return h

    def height(self) -> int:
        def _h(node: _Node[K, V]) -> int:
            if node is self.NIL:
                return 0
            return 1 + max(_h(node.left), _h(node.right))
        return _h(self.root)
