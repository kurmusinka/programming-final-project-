"""
Основная логика бюджетного помощника.

Модуль содержит класс BudgetAssistant со всеми алгоритмами:
- Префиксные суммы для запросов за период O(1)
- Линейный поиск дня с максимальным расходом
- Сортировка вставками категорий по сумме трат
- Стек для отмены последнего расхода
- Дерево BST для хранения расходов
"""

from data_structures import Stack, ExpenseTree


class BudgetAssistant:
    """
    Бюджетный помощник.
    Хранит расходы за месяц (дни 1–31).
    """

    DAYS_IN_MONTH = 31

    def __init__(self):
        # Расходы по дням: список списков [(сумма, категория), ...]
        self.daily_expenses = [[] for _ in range(self.DAYS_IN_MONTH + 1)]

        # Сумма расходов по дням (для префиксных сумм)
        self.daily_totals = [0] * (self.DAYS_IN_MONTH + 1)

        # Префиксные суммы (строятся при запросе)
        self.prefix = [0] * (self.DAYS_IN_MONTH + 1)
        self._prefix_valid = False  # флаг: нужно ли пересчитать

        # Стек для отмены
        self.undo_stack = Stack()

        # Дерево BST
        self.tree = ExpenseTree()

    # ----------------------------------------------------------
    # Добавление расхода
    # ----------------------------------------------------------

    def add_expense(self, day: int, amount: float, category: str) -> str:
        """
        Добавить расход.

        Args:
            day: день месяца (1–31)
            amount: сумма расхода (> 0)
            category: категория (например, 'Еда', 'Транспорт')

        Returns:
            Строка с результатом.
        """
        if not (1 <= day <= self.DAYS_IN_MONTH):
            return f"Ошибка: день должен быть от 1 до {self.DAYS_IN_MONTH}"
        if amount <= 0:
            return "Ошибка: сумма должна быть положительной"

        # Сохраняем в список дня
        self.daily_expenses[day].append((amount, category))
        self.daily_totals[day] += amount

        # Добавляем в стек для undo
        self.undo_stack.push((day, amount, category))

        # Добавляем в BST
        self.tree.insert(amount, category, day)

        # Сбрасываем флаг — нужно пересчитать префиксы
        self._prefix_valid = False

        return f"✓ Добавлено: день {day}, {amount:.2f} руб., категория '{category}'"

    # ----------------------------------------------------------
    # Отмена последнего расхода (стек)
    # ----------------------------------------------------------

    def undo(self) -> str:
        """Отменить последний добавленный расход."""
        last = self.undo_stack.pop()
        if last is None:
            return "Нет расходов для отмены"

        day, amount, category = last

        # Убираем из списка дня (последнее вхождение)
        expenses = self.daily_expenses[day]
        for i in range(len(expenses) - 1, -1, -1):
            if expenses[i] == (amount, category):
                expenses.pop(i)
                break

        self.daily_totals[day] -= amount
        self._prefix_valid = False

        return f"↩ Отменено: день {day}, {amount:.2f} руб., '{category}'"

    # ----------------------------------------------------------
    # Префиксные суммы — запрос за O(1)
    # ----------------------------------------------------------

    def _build_prefix(self):
        """Построить массив префиксных сумм."""
        self.prefix[0] = 0
        for i in range(1, self.DAYS_IN_MONTH + 1):
            self.prefix[i] = self.prefix[i - 1] + self.daily_totals[i]
        self._prefix_valid = True

    def query_period(self, day_a: int, day_b: int) -> str:
        """
        Сумма расходов за период с day_a по day_b включительно.
        Ответ за O(1) благодаря префиксным суммам.
        """
        if not (1 <= day_a <= day_b <= self.DAYS_IN_MONTH):
            return "Ошибка: некорректный период"

        if not self._prefix_valid:
            self._build_prefix()

        # prefix[b] - prefix[a-1] — классическая формула
        total = self.prefix[day_b] - self.prefix[day_a - 1]
        return (f"Расходы с {day_a} по {day_b} день: "
                f"{total:.2f} руб.")

    # ----------------------------------------------------------
    # Линейный поиск дня с максимальным расходом
    # ----------------------------------------------------------

    def find_max_day(self) -> str:
        """
        Линейный поиск дня с наибольшей суммой расходов.
        Сложность: O(n), где n — количество дней.
        """
        max_day = 1
        max_sum = self.daily_totals[1]

        for day in range(2, self.DAYS_IN_MONTH + 1):
            if self.daily_totals[day] > max_sum:
                max_sum = self.daily_totals[day]
                max_day = day

        if max_sum == 0:
            return "Расходы ещё не добавлены"
        return f"День с максимальными расходами: {max_day} ({max_sum:.2f} руб.)"

    # ----------------------------------------------------------
    # Сортировка вставками категорий по сумме трат
    # ----------------------------------------------------------

    def get_categories_sorted(self) -> str:
        """
        Собрать суммы по категориям и отсортировать
        сортировкой вставками (по убыванию).
        """
        # Собираем суммы по категориям в словарь
        cat_sums = {}
        for day in range(1, self.DAYS_IN_MONTH + 1):
            for amount, category in self.daily_expenses[day]:
                if category not in cat_sums:
                    cat_sums[category] = 0
                cat_sums[category] += amount

        if not cat_sums:
            return "Категории отсутствуют"

        # Преобразуем в список пар для сортировки
        items = list(cat_sums.items())  # [(категория, сумма), ...]

        # --- Сортировка вставками (по убыванию суммы) ---
        for i in range(1, len(items)):
            key = items[i]
            j = i - 1
            while j >= 0 and items[j][1] < key[1]:
                items[j + 1] = items[j]
                j -= 1
            items[j + 1] = key

        lines = ["Категории по расходам:"]
        for rank, (cat, total) in enumerate(items, start=1):
            lines.append(f"  {rank}. {cat}: {total:.2f} руб.")
        return "\n".join(lines)

    # ----------------------------------------------------------
    # Вывод дерева (все расходы, упорядоченные по сумме)
    # ----------------------------------------------------------

    def show_tree(self) -> str:
        """Показать все расходы из BST в порядке возрастания суммы."""
        nodes = self.tree.inorder()
        if not nodes:
            return "Дерево расходов пусто"
        lines = ["Все расходы (по возрастанию суммы):"]
        for amount, category, day in nodes:
            lines.append(f"  День {day:2d} | {amount:8.2f} руб. | {category}")
        max_node = self.tree.find_max()
        if max_node:
            lines.append(f"\nМаксимальный расход в дереве: "
                         f"{max_node[0]:.2f} руб. ({max_node[1]}, день {max_node[2]})")
        return "\n".join(lines)

    # ----------------------------------------------------------
    # Показать все расходы по дням
    # ----------------------------------------------------------

    def show_all(self) -> str:
        """Вывести все дни, в которых есть расходы."""
        lines = ["=== Все расходы по дням ==="]
        has_any = False
        for day in range(1, self.DAYS_IN_MONTH + 1):
            if self.daily_expenses[day]:
                has_any = True
                lines.append(f"День {day}:")
                for amount, cat in self.daily_expenses[day]:
                    lines.append(f"  {amount:.2f} руб. — {cat}")
                lines.append(f"  Итого за день: {self.daily_totals[day]:.2f} руб.")
        if not has_any:
            return "Расходы ещё не добавлены"
        return "\n".join(lines)
