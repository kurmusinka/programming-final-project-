"""
Тесты для бюджетного помощника.
Запуск: pytest tests.py -v
"""

import pytest
from budget import BudgetAssistant


# Фикстура - помощник для каждого теста

@pytest.fixture
def assistant():
    return BudgetAssistant()



# Тесты add_expense
def test_add_expense_basic(assistant):
    """Расход добавляется корректно."""
    assistant.add_expense(1, 500.0, "Еда")
    assert assistant.daily_totals[1] == 500.0
    assert assistant.daily_expenses[1] == [(500.0, "Еда")]


def test_add_expense_empty_category_becomes_prochee(assistant):
    """Пустая категория заменяется на 'Прочее'."""
    assistant.add_expense(1, 100.0, "")
    assert assistant.daily_expenses[1][0][1] == "Прочее"


def test_add_expense_invalid_day(assistant):
    """Некорректный день бросает ValueError."""
    with pytest.raises(ValueError):
        assistant.add_expense(0, 100.0, "Еда")
    with pytest.raises(ValueError):
        assistant.add_expense(32, 100.0, "Еда")


def test_add_expense_invalid_amount(assistant):
    """Некорректная сумма бросает ValueError."""
    with pytest.raises(ValueError):
        assistant.add_expense(1, -100.0, "Еда")
    with pytest.raises(ValueError):
        assistant.add_expense(1, 0.0, "Еда")


def test_add_multiple_expenses_same_day(assistant):
    """Несколько расходов в один день суммируются."""
    assistant.add_expense(5, 300.0, "Кафе")
    assistant.add_expense(5, 200.0, "Транспорт")
    assert assistant.daily_totals[5] == 500.0
    assert len(assistant.daily_expenses[5]) == 2



# Тесты undo
def test_undo_removes_last_expense(assistant):
    """Undo удаляет последний добавленный расход."""
    assistant.add_expense(1, 500.0, "Еда")
    assistant.add_expense(1, 300.0, "Транспорт")
    result = assistant.undo()
    assert result == (1, 300.0, "Транспорт")
    assert assistant.daily_totals[1] == 500.0
    assert len(assistant.daily_expenses[1]) == 1


def test_undo_empty_stack_returns_none(assistant):
    """Undo на пустом стеке возвращает None."""
    assert assistant.undo() is None


def test_undo_updates_bst(assistant):
    """После undo дерево BST не содержит отменённый расход."""
    assistant.add_expense(1, 1000.0, "Еда")
    assistant.undo()
    assert assistant.tree.is_empty()


def test_undo_twice(assistant):
    """Два последовательных undo работают корректно."""
    assistant.add_expense(1, 100.0, "A")
    assistant.add_expense(2, 200.0, "B")
    assistant.undo()
    assistant.undo()
    assert assistant.total_expenses() == 0.0



# Тесты query_period (префиксные суммы)
def test_query_period_basic(assistant):
    """Сумма за период считается верно."""
    assistant.add_expense(1, 100.0, "A")
    assistant.add_expense(3, 200.0, "B")
    assistant.add_expense(5, 300.0, "C")
    total, a, b = assistant.query_period(1, 5)
    assert total == 600.0

def test_query_period_single_day(assistant):
    """Запрос суммы за один день."""
    assistant.add_expense(7, 777.0, "X")
    total, _, _ = assistant.query_period(7, 7)
    assert total == 777.0


def test_query_period_empty(assistant):
    """Сумма за период без расходов равна 0."""
    total, _, _ = assistant.query_period(1, 10)
    assert total == 0.0


def test_query_period_invalid(assistant):
    """Некорректный период бросает ValueError."""
    with pytest.raises(ValueError):
        assistant.query_period(10, 5)  # начало > конец



# Тесты find_max_day
def test_find_max_day_basic(assistant):
    """День с максимальными расходами определяется верно."""
    assistant.add_expense(3, 100.0, "A")
    assistant.add_expense(7, 500.0, "B")
    assistant.add_expense(15, 300.0, "C")
    day, total = assistant.find_max_day()
    assert day == 7
    assert total == 500.0


def test_find_max_day_empty(assistant):
    """При отсутствии расходов возвращает (0, 0.0)."""
    day, total = assistant.find_max_day()
    assert day == 0
    assert total == 0.0



# Тесты get_categories_sorted (сортировка вставками)
def test_categories_sorted_order(assistant):
    """Категории отсортированы по убыванию суммы."""
    assistant.add_expense(1, 100.0, "Кафе")
    assistant.add_expense(2, 500.0, "Одежда")
    assistant.add_expense(3, 300.0, "Продукты")
    items = assistant.get_categories_sorted()
    totals = [t for _, t in items]
    assert totals == sorted(totals, reverse=True)


def test_categories_sorted_empty(assistant):
    """При отсутствии расходов возвращает пустой список."""
    assert assistant.get_categories_sorted() == []



# Тесты BST
def test_tree_inorder_sorted(assistant):
    """BST возвращает расходы в порядке возрастания суммы."""
    assistant.add_expense(1, 300.0, "A")
    assistant.add_expense(2, 100.0, "B")
    assistant.add_expense(3, 200.0, "C")
    nodes = assistant.get_tree_expenses()
    amounts = [n[0] for n in nodes]
    assert amounts == sorted(amounts)


def test_tree_max(assistant):
    """BST находит максимальный расход."""
    assistant.add_expense(1, 300.0, "A")
    assistant.add_expense(2, 100.0, "B")
    assistant.add_expense(3, 500.0, "C")
    max_node = assistant.get_tree_max()
    assert max_node[0] == 500.0



# Тесты аналитики
def test_total_expenses(assistant):
    """Общая сумма расходов считается верно."""
    assistant.add_expense(1, 100.0, "A")
    assistant.add_expense(2, 200.0, "B")
    assert assistant.total_expenses() == 300.0


def test_average_transaction(assistant):
    """Средняя транзакция считается верно."""
    assistant.add_expense(1, 100.0, "A")
    assistant.add_expense(1, 300.0, "B")
    assert assistant.average_transaction() == 200.0


def test_max_category(assistant):
    """Топ категория определяется верно."""
    assistant.add_expense(1, 100.0, "Кафе")
    assistant.add_expense(2, 500.0, "Одежда")
    cat, _ = assistant.max_category()
    assert cat == "Одежда"
