"""
data_structures содержит:
- Stack — для отмены последнего расхода
- Дерево BST — для хранения трат по сумме
"""
from typing import Any, Optional



# Стек — отмена последнего добавленного расхода
class Stack:
    """
    Стек для хранения истории добавленных расходов. 
    Используется принцип LIFO (Last In — First Out), поскольку нужно отменять именно последнее действие, а стек даёт доступ к нему за O(1).
    """

    def __init__(self) -> None:
        self._data: list = []

    def push(self, item: Any) -> None:
        """Добавить элемент на вершину стека. Сложность O(1)."""
        self._data.append(item)

    def pop(self) -> Optional[Any]:
        """
        Извлечь и вернуть верхний элемент. Сложность O(1).
        Возвращает None если стек пуст.
        """
        if self.is_empty():
            return None
        return self._data.pop()

    def peek(self) -> Optional[Any]:
        """Посмотреть верхний элемент без извлечения. Сложность O(1)."""
        if self.is_empty():
            return None
        return self._data[-1]

    def is_empty(self) -> bool:
        """Проверить, пуст ли стек. Сложность O(1)."""
        return len(self._data) == 0

    def size(self) -> int:
        """Количество элементов в стеке. Сложность O(1)."""
        return len(self._data)

    def clear(self) -> None:
        """Очистить стек."""
        self._data = []

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"Stack({self._data})"



# Дерево BST — хранение расходов, упорядоченных по сумме
class TreeNode:
    """Узел бинарного дерева поиска."""

    def __init__(self, amount: float, category: str, day: int) -> None:
        # Составной ключ: (amount, day, category) — уникален для каждого расхода
        self.key: tuple = (amount, day, category)
        self.amount = amount
        self.category = category
        self.day = day
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None


class ExpenseTree:
    """
    Бинарное дерево поиска расходов.
    Ключ — составной (amount, day, category), что позволяет корректно хранить расходы с одинаковой суммой.
    Сложности операций: insert: O(log n), inorder: O(n), find_min/find_max: O(log n)
    """

    def __init__(self) -> None:
        self.root: Optional[TreeNode] = None

    def insert(self, amount: float, category: str, day: int) -> None:
        """
        Вставить расход в дерево. Среднее O(log n), худшее O(n).
        """
        new_node = TreeNode(amount, category, day)
        if self.root is None:
            self.root = new_node
            return
        current = self.root
        while True:
            if new_node.key <= current.key:
                if current.left is None:
                    current.left = new_node
                    break
                current = current.left
            else:
                if current.right is None:
                    current.right = new_node
                    break
                current = current.right

    def inorder(self) -> list[tuple]:
        """
        Симметричный обход — возвращает расходы в порядке возрастания суммы. Сложность O(n).
        """
        result: list = []

        def dfs(node: Optional[TreeNode]) -> None:
            if node is None:
                return
            dfs(node.left)
            result.append((node.amount, node.category, node.day))
            dfs(node.right)

        dfs(self.root)
        return result

    def find_max(self) -> Optional[tuple]:
        """
        Найти расход с максимальной суммой (крайний правый узел). Среднее O(log n), худшее O(n).
        """
        if self.root is None:
            return None
        current = self.root
        while current.right is not None:
            current = current.right
        return (current.amount, current.category, current.day)

    def find_min(self) -> Optional[tuple]:
        """
        Найти расход с минимальной суммой (крайний левый узел). Среднее O(log n), худшее O(n).
        """
        if self.root is None:
            return None
        current = self.root
        while current.left is not None:
            current = current.left
        return (current.amount, current.category, current.day)

    def is_empty(self) -> bool:
        """Проверить, пусто ли дерево."""
        return self.root is None
