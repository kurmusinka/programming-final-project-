"""
budget содержит:
- Префиксные суммы: построение O(n), запрос за период O(1)
- Линейный поиск дня с максимальным расходом: O(n), n=31
- Сортировка вставками категорий по сумме трат: O(k²) (выбрана намеренно для демонстрации алгоритма)
- Стек (LIFO) для отмены последнего расхода: push/pop O(1)
- BST для хранения расходов в отсортированном виде: вставка O(log n)
"""

from __future__ import annotations
from typing import Optional
from data_structures import Stack, ExpenseTree


class BudgetAssistant:
    """
    Бюджетный помощник — хранит расходы за месяц (дни 1–31).
    Такие данные как:
    - daily_expenses: список списков расходов по дням
    - daily_totals: суммы расходов по дням (для префиксных сумм)
    - tree: BST, пересоздаётся при каждом undo для сохранения целостности
    """

    DAYS_IN_MONTH = 31

    def __init__(self) -> None:
        # Храним расходы по дням: список списков [(сумма, категория), ...]
        self.daily_expenses: list[list] = [
            [] for _ in range(self.DAYS_IN_MONTH + 1)
        ]
        # Суммы расходов по дням (индекс = день)
        self.daily_totals: list[float] = [0.0] * (self.DAYS_IN_MONTH + 1)

        # Префиксные суммы; пересчитываются при изменении данных
        self._prefix: list[float] = [0.0] * (self.DAYS_IN_MONTH + 1)
        self._prefix_valid: bool = False

        # Стек для отмены: хранит (day, amount, category)
        self.undo_stack: Stack = Stack()

        # BST (для хранения расходов в отсортированном по сумме виде)
        self.tree: ExpenseTree = ExpenseTree()

    
    # Вспомогательные методы
    def _validate_day(self, day: int) -> None:
        """Проверить корректность дня. Бросает ValueError."""
        if not (1 <= day <= self.DAYS_IN_MONTH):
            raise ValueError(f"День должен быть от 1 до {self.DAYS_IN_MONTH}")

    def _validate_amount(self, amount: float) -> None:
        """Проверить корректность суммы. Бросает ValueError."""
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")

    def _normalize_category(self, category: str) -> str:
        """Нормализовать категорию: убрать пробелы, подставить 'Прочее'."""
        category = category.strip()
        return category if category else "Прочее"

    def _rebuild_tree(self) -> None:
        """
        Пересоздать дерево BST из текущих данных.
        Сложность: O(n log n) в среднем.
        """
        self.tree = ExpenseTree()
        for day in range(1, self.DAYS_IN_MONTH + 1):
            for amount, category in self.daily_expenses[day]:
                self.tree.insert(amount, category, day)

   
    # Добавление расхода
    def add_expense(self, day: int, amount: float, category: str) -> None:
        """
        Добавить расход в указанный день.
        Сложность: O(log n) в среднем (вставка в BST)
        Raises: ValueError - при некорректных входных данных
        """
        self._validate_day(day)
        self._validate_amount(amount)
        category = self._normalize_category(category)

        self.daily_expenses[day].append((amount, category))
        self.daily_totals[day] += amount

        # Кладём в стек для возможности отмены — O(1)
        self.undo_stack.push((day, amount, category))

        # Вставляем в BST — O(log n) в среднем
        self.tree.insert(amount, category, day)
        self._prefix_valid = False


    # Отмена последнего расхода (стек, LIFO)
    def undo(self) -> tuple | None:
        """
        Отменить последний добавленный расход.
        Извлекаем из стека за O(1), удаляем из списка дня за O(k), пересоздаём BST за O(n log n) для сохранения целостности данных.
        Returns: Кортеж (day, amount, category) отменённого расхода или None.
        """
        last = self.undo_stack.pop()  # O(1)
        if last is None:
            return None

        day, amount, category = last

        # Удаляем последнее вхождение из списка дня — O(k)
        expenses = self.daily_expenses[day]
        for i in range(len(expenses) - 1, -1, -1):
            if expenses[i] == (amount, category):
                expenses.pop(i)
                break

        self.daily_totals[day] -= amount

        # Пересоздаём BST
        self._rebuild_tree()

        self._prefix_valid = False
        return last


    # Префиксные суммы
    def _build_prefix(self) -> None:
        """
        Массив префиксных сумм. prefix[i] = сумма расходов с 1-го по i-й день.
        Сложность: O(n), где n = 31.
        """
        self._prefix[0] = 0.0
        for i in range(1, self.DAYS_IN_MONTH + 1):
            self._prefix[i] = self._prefix[i - 1] + self.daily_totals[i]
        self._prefix_valid = True

    def query_period(self, day_a: int, day_b: int) -> tuple[float, int, int]:
        """
        Вернуть сумму расходов за период с day_a по day_b включительно.
        Выполняется за O(1) благодаря массиву префиксных сумм.
        Returns: Кортеж (сумма, day_a, day_b)
        Raises: ValueError: при некорректном периоде
        """
        self._validate_day(day_a)
        self._validate_day(day_b)
        if day_a > day_b:
            raise ValueError("Начало периода не может быть позже конца")

        if not self._prefix_valid:
            self._build_prefix()

        # Формула: prefix[b] - prefix[a-1] — O(1)
        total = self._prefix[day_b] - self._prefix[day_a - 1]
        return (total, day_a, day_b)

   
    # Линейный поиск дня с максимальным расходом
    def find_max_day(self) -> tuple[int, float]:
        """
        Найти день с самыми большими расходами линейным поиском (О(n)).
        Сложность O(n), где n — количество дней.
        Returns: Кортеж (день, сумма) или (0, 0.0) если расходов нет.
        """
        max_day = 0
        max_sum = 0.0

        for day in range(1, self.DAYS_IN_MONTH + 1):
            if self.daily_totals[day] > max_sum:
                max_sum = self.daily_totals[day]
                max_day = day

        return (max_day, max_sum)


    # Сортировка вставками категорий по сумме
    def get_categories_sorted(self) -> list[tuple[str, float]]:
        """
        Сортировка вставками выбрана специально для демонстрации алгоритма O(k²), где k — количество уникальных категорий.
        Returns: Список пар (категория, сумма) в порядке убывания.
        """
        cat_sums: dict[str, float] = {}
        for day in range(1, self.DAYS_IN_MONTH + 1):
            for amount, category in self.daily_expenses[day]:
                cat_sums[category] = cat_sums.get(category, 0.0) + amount

        if not cat_sums:
            return []

        items = list(cat_sums.items())

        # Сортировка вставками по убыванию суммы — O(k²)
        for i in range(1, len(items)):
            key = items[i]
            j = i - 1
            while j >= 0 and items[j][1] < key[1]:
                items[j + 1] = items[j]
                j -= 1
            items[j + 1] = key

        return items


    # Дерево BST
    def get_tree_expenses(self) -> list[tuple]:
        """
        Все расходы из BST в порядке возрастания суммы.
        Сложность: O(n).
        """
        return self.tree.inorder()

    def get_tree_max(self) -> Optional[tuple]:
        """Максимальный расход в BST. Среднее O(log n)."""
        return self.tree.find_max()

    def get_tree_min(self) -> Optional[tuple]:
        """Минимальный расход в BST. Среднее O(log n)."""
        return self.tree.find_min()

   
    # Аналитика
    def total_expenses(self) -> float:
        """Общая сумма всех расходов за месяц."""
        return sum(self.daily_totals)

    def average_daily_expense(self) -> float:
        """Средний расход по дням, в которых есть хоть один расход."""
        active_days = [t for t in self.daily_totals if t > 0]
        if not active_days:
            return 0.0
        return sum(active_days) / len(active_days)

    def average_transaction(self) -> float:
        """Средняя сумма одной транзакции."""
        all_amounts = [
            amount
            for day_list in self.daily_expenses
            for amount, _ in day_list
        ]
        if not all_amounts:
            return 0.0
        return sum(all_amounts) / len(all_amounts)

    def max_category(self) -> tuple[str, float]:
        """Категория с наибольшей суммой расходов."""
        sorted_cats = self.get_categories_sorted()
        if not sorted_cats:
            return ("", 0.0)
        return sorted_cats[0]

    def get_all_expenses(self) -> list[tuple[int, float, str]]:
        """
        Вернуть все расходы в виде списка (день, сумма, категория).
        """
        result = []
        for day in range(1, self.DAYS_IN_MONTH + 1):
            for amount, category in self.daily_expenses[day]:
                result.append((day, amount, category))
        return result
