"""
Структуры данных для бюджетного помощника.

Модуль содержит:
- Stack (Стек) — для отмены последнего расхода
- ExpenseTree (Дерево BST) — для хранения трат по сумме
"""


# ============================================================
# Стек — отмена последнего добавленного расхода
# ============================================================

class Stack:
    """Стек для хранения истории добавленных расходов (undo)."""

    def __init__(self):
        self._data = []

    def push(self, item):
        """Добавить элемент на вершину стека."""
        self._data.append(item)

    def pop(self):
        """Извлечь и вернуть верхний элемент. None если стек пуст."""
        if self.is_empty():
            return None
        return self._data.pop()

    def peek(self):
        """Посмотреть верхний элемент без извлечения."""
        if self.is_empty():
            return None
        return self._data[-1]

    def is_empty(self):
        """Проверить, пуст ли стек."""
        return len(self._data) == 0

    def __len__(self):
        return len(self._data)


# ============================================================
# Дерево BST — хранение расходов, упорядоченных по сумме
# ============================================================

class TreeNode:
    """Узел дерева BST для хранения расхода."""

    def __init__(self, amount, category, day):
        self.amount = amount      # ключ для BST
        self.category = category
        self.day = day
        self.left = None
        self.right = None


class ExpenseTree:
    """
    Бинарное дерево поиска.
    Ключ — сумма расхода. Позволяет быстро найти
    минимальный, максимальный расход и обойти все по порядку.
    """

    def __init__(self):
        self.root = None

    def insert(self, amount, category, day):
        """Вставить новый расход в дерево."""
        new_node = TreeNode(amount, category, day)
        if self.root is None:
            self.root = new_node
            return
        current = self.root
        while True:
            if amount <= current.amount:
                if current.left is None:
                    current.left = new_node
                    break
                current = current.left
            else:
                if current.right is None:
                    current.right = new_node
                    break
                current = current.right

    def inorder(self, node=None, _start=True):
        """
        Симметричный обход — возвращает расходы
        в порядке возрастания суммы.
        """
        if _start:
            node = self.root
        if node is None:
            return []
        result = []
        result += self.inorder(node.left, _start=False)
        result.append((node.amount, node.category, node.day))
        result += self.inorder(node.right, _start=False)
        return result

    def find_max(self):
        """Найти расход с максимальной суммой (крайний правый узел)."""
        if self.root is None:
            return None
        current = self.root
        while current.right is not None:
            current = current.right
        return (current.amount, current.category, current.day)

    def find_min(self):
        """Найти расход с минимальной суммой (крайний левый узел)."""
        if self.root is None:
            return None
        current = self.root
        while current.left is not None:
            current = current.left
        return (current.amount, current.category, current.day)
