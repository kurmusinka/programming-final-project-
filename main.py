"""
Бюджетный помощник — точка входа.
Запуск: python main.py
"""

from budget import BudgetAssistant


def print_menu():
    print("\n" + "=" * 45)
    print("       БЮДЖЕТНЫЙ ПОМОЩНИК")
    print("=" * 45)
    print("1. Добавить расход")
    print("2. Отменить последний расход (undo)")
    print("3. Сумма расходов за период")
    print("4. День с максимальными расходами")
    print("5. Категории по расходам (сорт. вставками)")
    print("6. Показать дерево расходов (BST)")
    print("7. Показать все расходы по дням")
    print("0. Выход")
    print("=" * 45)


def get_int(prompt, min_val=None, max_val=None):
    """Безопасный ввод целого числа."""
    while True:
        try:
            value = int(input(prompt))
            if min_val is not None and value < min_val:
                print(f"  Введите число >= {min_val}")
                continue
            if max_val is not None and value > max_val:
                print(f"  Введите число <= {max_val}")
                continue
            return value
        except ValueError:
            print("  Ошибка: введите целое число")


def get_float(prompt):
    """Безопасный ввод числа с плавающей точкой."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("  Сумма должна быть больше 0")
                continue
            return value
        except ValueError:
            print("  Ошибка: введите число (например: 250.50)")


def main():
    assistant = BudgetAssistant()

    # Загружаем демонстрационные данные
    demo = [
        (1,  1500.0, "Продукты"),
        (1,   350.0, "Транспорт"),
        (3,  2200.0, "Кафе"),
        (5,   800.0, "Транспорт"),
        (7,  5000.0, "Одежда"),
        (10, 1200.0, "Продукты"),
        (10,  450.0, "Развлечения"),
        (15, 3500.0, "Продукты"),
        (20,  750.0, "Транспорт"),
        (25, 1800.0, "Кафе"),
    ]
    print("\nЗагрузка демонстрационных данных...")
    for day, amount, cat in demo:
        assistant.add_expense(day, amount, cat)
    print("Готово! Добавлено 10 расходов.")

    # Главный цикл
    while True:
        print_menu()
        choice = input("Выберите пункт: ").strip()

        if choice == "1":
            print("\n--- Добавить расход ---")
            day = get_int("День (1-31): ", 1, 31)
            amount = get_float("Сумма (руб.): ")
            category = input("Категория: ").strip()
            if not category:
                category = "Прочее"
            print(assistant.add_expense(day, amount, category))

        elif choice == "2":
            print("\n--- Отмена последнего расхода ---")
            print(assistant.undo())

        elif choice == "3":
            print("\n--- Сумма за период ---")
            day_a = get_int("С какого дня: ", 1, 31)
            day_b = get_int("По какой день: ", day_a, 31)
            print(assistant.query_period(day_a, day_b))

        elif choice == "4":
            print("\n--- День с максимальными расходами ---")
            print(assistant.find_max_day())

        elif choice == "5":
            print("\n--- Категории по расходам ---")
            print(assistant.get_categories_sorted())

        elif choice == "6":
            print("\n--- Дерево расходов (BST) ---")
            print(assistant.show_tree())

        elif choice == "7":
            print("\n--- Все расходы по дням ---")
            print(assistant.show_all())

        elif choice == "0":
            print("\nДо свидания!")
            break

        else:
            print("Неверный выбор, попробуйте снова")


if __name__ == "__main__":
    main()
