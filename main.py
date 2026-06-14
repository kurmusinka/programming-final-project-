"""
Бюджетный помощник — точка входа.
Запуск: python main.py
"""
from budget import BudgetAssistant

def print_menu() -> None:
    print("\n" + "=" * 48)
    print("          БЮДЖЕТНЫЙ ПОМОЩНИК")
    print("=" * 48)
    print("1. Добавить расход")
    print("2. Отменить последний расход (undo)")
    print("3. Сумма расходов за период")
    print("4. День с максимальными расходами")
    print("5. Категории по расходам (сортировка вставками)")
    print("6. Дерево расходов (BST, inorder)")
    print("7. Все расходы по дням")
    print("8. Аналитика (итого, среднее, топ категория)")
    print("0. Выход")
    print("=" * 48)


def get_int(prompt: str, min_val: int = None, max_val: int = None) -> int:
    """Безопасный ввод целого числа с проверкой диапазона."""
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


def get_float(prompt: str) -> float:
    """Безопасный ввод суммы."""
    while True:
        try:
            value = float(input(prompt).replace(",", "."))
            if value <= 0:
                print("  Сумма должна быть больше 0")
                continue
            return value
        except ValueError:
            print("  Ошибка: введите число (например: 250.50)")


def main() -> None:
    assistant = BudgetAssistant()

    # Демонстрационные данные
    demo = [
        (1, 1500.0, "Продукты"),
        (1,  350.0, "Транспорт"),
        (3, 2200.0, "Кафе"),
        (5,  800.0, "Транспорт"),
        (7, 5000.0, "Одежда"),
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

    while True:
        print_menu()
        choice = input("Выберите пункт: ").strip()

        if choice == "1":
            print("\n--- Добавить расход ---")
            try:
                day = get_int("День (1-31): ", 1, 31)
                amount = get_float("Сумма (руб.): ")
                category = input("Категория: ").strip()
                assistant.add_expense(day, amount, category)
                print(f"✓ Добавлено: день {day}, {amount:.2f} руб., '{category or 'Прочее'}'")
            except ValueError as e:
                print(f"Ошибка: {e}")

        elif choice == "2":
            print("\n--- Отмена последнего расхода ---")
            result = assistant.undo()
            if result:
                day, amount, cat = result
                print(f"↩ Отменено: день {day}, {amount:.2f} руб., '{cat}'")
            else:
                print("Нет расходов для отмены")

        elif choice == "3":
            print("\n--- Сумма за период ---")
            try:
                day_a = get_int("С какого дня: ", 1, 31)
                day_b = get_int("По какой день: ", day_a, 31)
                total, a, b = assistant.query_period(day_a, day_b)
                print(f"Расходы с {a} по {b} день: {total:.2f} руб.")
            except ValueError as e:
                print(f"Ошибка: {e}")

        elif choice == "4":
            print("\n--- День с максимальными расходами ---")
            day, total = assistant.find_max_day()
            if day == 0:
                print("Расходы ещё не добавлены")
            else:
                print(f"День {day}: {total:.2f} руб.")

        elif choice == "5":
            print("\n--- Категории по расходам ---")
            items = assistant.get_categories_sorted()
            if not items:
                print("Категории отсутствуют")
            else:
                print("(Сортировка вставками, O(k²))")
                for rank, (cat, total) in enumerate(items, 1):
                    print(f"  {rank}. {cat}: {total:.2f} руб.")

        elif choice == "6":
            print("\n--- Дерево расходов (BST, inorder) ---")
            nodes = assistant.get_tree_expenses()
            if not nodes:
                print("Дерево пусто")
            else:
                print("Расходы в порядке возрастания суммы:")
                for amount, cat, day in nodes:
                    print(f"  День {day:2d} | {amount:8.2f} руб. | {cat}")
                max_node = assistant.get_tree_max()
                if max_node:
                    print(f"\nМакс: {max_node[0]:.2f} руб. ({max_node[1]}, день {max_node[2]})")

        elif choice == "7":
            print("\n--- Все расходы по дням ---")
            all_exp = assistant.get_all_expenses()
            if not all_exp:
                print("Расходы не добавлены")
            else:
                current_day = None
                for day, amount, cat in sorted(all_exp):
                    if day != current_day:
                        current_day = day
                        print(f"\nДень {day}:")
                    print(f"  {amount:.2f} руб. — {cat}")

        elif choice == "8":
            print("\n--- Аналитика ---")
            print(f"Итого за месяц:          {assistant.total_expenses():.2f} руб.")
            print(f"Среднее по активным дням: {assistant.average_daily_expense():.2f} руб.")
            print(f"Средняя транзакция:       {assistant.average_transaction():.2f} руб.")
            cat, total = assistant.max_category()
            if cat:
                print(f"Топ категория:           {cat} ({total:.2f} руб.)")

        elif choice == "0":
            print("\nДо свидания!")
            break
        else:
            print("Неверный выбор, попробуйте снова")


if __name__ == "__main__":
    main()
