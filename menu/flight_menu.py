from algorithms.flight_avl import AVLTree
from entities.flight import Flight
from validators.flight_validator import (
    validate_flight_number,
    validate_airline,
    validate_airport,
    validate_date,
    validate_time,
    validate_seats
)
from utils.console import clear_screen, print_header, wait_for_enter, input_yes_no, input_int


def menu_flights(flights):
    """Меню работы с рейсами"""
    while True:
        clear_screen()
        print_header("✈️  РАБОТА С РЕЙСАМИ")
        print("1. ➕ Добавить рейс")
        print("2. 🔍 Найти рейс по номеру")
        print("3. 🗑️ Удалить рейс")
        print("4. 📋 Показать все рейсы (обратный обход)")
        print("5. 🌳 Показать структуру АВЛ-дерева")
        print("6. 📦 Автозаполнение (тестовые данные)")
        print("0. 🔙 Назад в главное меню")
        print("-" * 60)

        choice = input("👉 Выберите действие: ").strip()

        if choice == "1":
            _add_flight(flights)
        elif choice == "2":
            _find_flight(flights)
        elif choice == "3":
            _delete_flight(flights)
        elif choice == "4":
            _list_flights(flights)
        elif choice == "5":
            _show_tree(flights)
        elif choice == "6":
            _autofill_flights(flights)
        elif choice == "0":
            break
        else:
            print("❌ Неверный выбор. Введите 0-6.")
            wait_for_enter()


def _add_flight(flights):
    """Добавление нового рейса с пошаговой валидацией"""
    clear_screen()
    print_header("➕ ДОБАВЛЕНИЕ РЕЙСА")
    print("📝 Введите данные (ошибки будут показаны сразу):")
    print("-" * 60)

    # Ввод номера рейса с проверкой
    while True:
        flight_num = input("   Номер рейса (AAA-NNN, например AFL-123): ").strip()
        valid, result = validate_flight_number(flight_num)
        if valid:
            flight_num = result
            break
        print(f"   ❌ {result}")

    # Проверка на дубликат
    if flights.find(flight_num):
        print(f"\n❌ Рейс {flight_num} уже существует!")
        wait_for_enter()
        return

    # Ввод авиакомпании
    while True:
        airline = input("   Авиакомпания: ").strip()
        valid, result = validate_airline(airline)
        if valid:
            airline = result
            break
        print(f"   ❌ {result}")

    # Ввод аэропорта отправления
    while True:
        departure = input("   Аэропорт отправления: ").strip()
        valid, result = validate_airport(departure, "Аэропорт отправления")
        if valid:
            departure = result
            break
        print(f"   ❌ {result}")

    # Ввод аэропорта прибытия
    while True:
        arrival = input("   Аэропорт прибытия: ").strip()
        valid, result = validate_airport(arrival, "Аэропорт прибытия")
        if valid:
            arrival = result
            break
        print(f"   ❌ {result}")

    # Ввод даты
    while True:
        date = input("   Дата отправления (ДД.ММ.ГГГГ): ").strip()
        valid, result = validate_date(date)
        if valid:
            date = result
            break
        print(f"   ❌ {result}")

    # Ввод времени
    while True:
        time = input("   Время отправления (ЧЧ:ММ): ").strip()
        valid, result = validate_time(time)
        if valid:
            time = result
            break
        print(f"   ❌ {result}")

    # Ввод количества мест
    total_seats = input_int("   Всего мест: ", min_val=1)
    free_seats = input_int(f"   Свободных мест (0-{total_seats}): ", min_val=0, max_val=total_seats)

    # Создание и добавление рейса
    f = Flight(flight_num, airline, departure, arrival, date, time, total_seats, free_seats)
    flights.insert(f)
    print(f"\n✅ Рейс {flight_num} успешно добавлен!")
    wait_for_enter()


def _find_flight(flights):
    """Поиск рейса по номеру"""
    clear_screen()
    print_header("🔍 ПОИСК РЕЙСА")

    # Ввод номера рейса с проверкой
    while True:
        flight_num = input("   Введите номер рейса (AAA-NNN): ").strip()
        valid, result = validate_flight_number(flight_num)
        if valid:
            flight_num = result
            break
        print(f"   ❌ {result}")

    found = flights.find(flight_num)
    if found:
        info = found.get_info()
        print(f"\n✅ РЕЙС НАЙДЕН:")
        print("=" * 60)
        print(f"   Номер:        {info['flight_number']}")
        print(f"   Авиакомпания: {info['airline']}")
        print(f"   Маршрут:      {info['departure_airport']} → {info['arrival_airport']}")
        print(f"   Отправление:  {info['departure_date']} {info['departure_time']}")
        print(f"   Места:        {info['free_seats']}/{info['total_seats']} свободно")
        print("=" * 60)
    else:
        print(f"\n❌ Рейс {flight_num} не найден!")

    wait_for_enter()


def _delete_flight(flights):
    """Удаление рейса по номеру"""
    clear_screen()
    print_header("🗑️ УДАЛЕНИЕ РЕЙСА")
    print("⚠️ Внимание! Удаление нельзя отменить.")

    # Ввод номера рейса с проверкой
    while True:
        flight_num = input("   Введите номер рейса (AAA-NNN): ").strip()
        valid, result = validate_flight_number(flight_num)
        if valid:
            flight_num = result
            break
        print(f"   ❌ {result}")

    found = flights.find(flight_num)
    if found:
        print(f"\n📋 Найден рейс: {found.flight_number} ({found.departure_airport} → {found.arrival_airport})")
        if input_yes_no("   Удалить? (д/н): "):
            flights.delete(flight_num)
            print(f"\n✅ Рейс {flight_num} удалён!")
        else:
            print(f"\n🚫 Удаление отменено.")
    else:
        print(f"\n❌ Рейс {flight_num} не найден!")

    wait_for_enter()


def _list_flights(flights):
    """Вывод всех рейсов в порядке обратного обхода"""
    clear_screen()
    print_header("📋 ВСЕ РЕЙСЫ (обратный обход)")
    result = flights.reverse_traversal()

    if result:
        print(f"   Всего рейсов: {len(result)}")
        print("-" * 80)
        for i, f in enumerate(result, 1):
            info = f.get_info()
            print(f"{i:2}. {info['flight_number']} | {info['airline']}")
            print(f"     {info['departure_airport']} → {info['arrival_airport']}")
            print(f"     {info['departure_date']} {info['departure_time']} | {info['free_seats']}/{info['total_seats']} мест")
            print("-" * 40)
        print("\n   🔄 Порядок вывода: левое → правое → корень (обратный обход)")
    else:
        print("   📭 Нет добавленных рейсов")

    wait_for_enter()


def _show_tree(flights):
    """Показать структуру АВЛ-дерева"""
    clear_screen()
    print_header("🌳 СТРУКТУРА АВЛ-ДЕРЕВА")
    flights.print_tree_text()
    wait_for_enter()


def _autofill_flights(flights):
    """Автозаполнение тестовыми рейсами"""
    clear_screen()
    print_header("📦 АВТОЗАПОЛНЕНИЕ РЕЙСОВ")
    print("   Добавление тестовых данных...")
    print("-" * 80)

    test_flights = [
        ("AFL-123", "Аэрофлот", "Москва (SVO)", "Санкт-Петербург (LED)", "22.02.2026", "10:30", 150, 150),
        ("S7-456", "S7 Airlines", "Москва (DME)", "Казань (KZN)", "22.02.2026", "12:45", 120, 120),
        ("AFL-789", "Аэрофлот", "Санкт-Петербург (LED)", "Сочи (AER)", "23.02.2026", "08:15", 180, 180),
        ("UT-321", "ЮТэйр", "Москва (VKO)", "Тюмень (TJM)", "22.02.2026", "15:20", 100, 100),
        ("AFL-555", "Аэрофлот", "Москва (SVO)", "Владивосток (VVO)", "24.02.2026", "23:55", 250, 250),
        ("POB-789", "Победа", "Москва (VKO)", "Калининград (KGD)", "23.02.2026", "09:30", 180, 180),
        ("UIA-234", "Уральские авиалинии", "Екатеринбург (SVX)", "Симферополь (SIP)", "25.02.2026", "14:20", 200, 200),
        ("RUS-777", "Россия", "Москва (SVO)", "Сочи (AER)", "22.02.2026", "07:10", 220, 220),
        ("S7-888", "S7 Airlines", "Новосибирск (OVB)", "Москва (DME)", "26.02.2026", "18:45", 160, 160),
        ("AFL-111", "Аэрофлот", "Москва (SVO)", "Нью-Йорк (JFK)", "27.02.2026", "19:30", 300, 300),
    ]

    added = 0
    skipped = 0

    for flight_num, airline, dep, arr, date, time, total, free in test_flights:
        if flights.find(flight_num):
            print(f"   ⏭️  Пропущен (уже есть): {flight_num} ({dep} → {arr})")
            skipped += 1
        else:
            f = Flight(flight_num, airline, dep, arr, date, time, total, free)
            flights.insert(f)
            print(f"   ✅ Добавлен: {flight_num} ({dep} → {arr})")
            added += 1

    print("-" * 80)
    print(f"   📊 Итог: добавлено {added}, пропущено {skipped}")
    wait_for_enter()