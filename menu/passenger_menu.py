from algorithms.passenger_hash import HashTable
from entities.passenger import Passenger
from validators.passenger_validator import (
    validate_passport,
    validate_full_name,
    validate_birth_date,
    validate_passport_issue
)
from utils.console import clear_screen, print_header, wait_for_enter, input_yes_no


def menu_passengers(passengers):
    """Меню работы с пассажирами"""
    while True:
        clear_screen()
        print_header("🧑 РАБОТА С ПАССАЖИРАМИ")
        print("1. ➕ Добавить пассажира")
        print("2. 🔍 Найти пассажира по паспорту")
        print("3. 🗑️ Удалить пассажира")
        print("4. 📋 Показать всех пассажиров")
        print("5. 📦 Автозаполнение (тестовые данные)")
        print("0. 🔙 Назад в главное меню")
        print("-" * 60)

        choice = input("👉 Выберите действие: ").strip()

        if choice == "1":
            _add_passenger(passengers)
        elif choice == "2":
            _find_passenger(passengers)
        elif choice == "3":
            _delete_passenger(passengers)
        elif choice == "4":
            _list_passengers(passengers)
        elif choice == "5":
            _autofill_passengers(passengers)
        elif choice == "0":
            break
        else:
            print("❌ Неверный выбор. Введите 0-5.")
            wait_for_enter()


def _add_passenger(passengers):
    """Добавление нового пассажира с пошаговой валидацией"""
    clear_screen()
    print_header("➕ ДОБАВЛЕНИЕ ПАССАЖИРА")
    print("📝 Введите данные (ошибки будут показаны сразу):")
    print("-" * 60)

    # Ввод номера паспорта с проверкой
    while True:
        passport = input("   Номер паспорта (NNNN-NNNNNN): ").strip()
        valid, result = validate_passport(passport)
        if valid:
            passport = result
            break
        print(f"   ❌ {result}")

    # Проверка на дубликат
    if passengers.find(passport):
        print(f"\n❌ Паспорт {passport} уже существует!")
        wait_for_enter()
        return

    # Ввод ФИО с проверкой
    while True:
        full_name = input("   ФИО полностью: ").strip()
        valid, result = validate_full_name(full_name)
        if valid:
            full_name = result
            break
        print(f"   ❌ {result}")

    # Ввод даты рождения с проверкой
    while True:
        birth_date = input("   Дата рождения (ДД.ММ.ГГГГ): ").strip()
        valid, result = validate_birth_date(birth_date)
        if valid:
            birth_date = result
            break
        print(f"   ❌ {result}")

    # Ввод места выдачи с проверкой
    while True:
        passport_issue = input("   Место выдачи паспорта: ").strip()
        valid, result = validate_passport_issue(passport_issue)
        if valid:
            passport_issue = result
            break
        print(f"   ❌ {result}")

    # Создание и добавление пассажира
    p = Passenger(passport, full_name, birth_date, passport_issue)
    passengers.insert(p)
    print(f"\n✅ Пассажир {full_name} успешно добавлен!")
    print(f"   Паспорт: {passport}")
    wait_for_enter()


def _find_passenger(passengers):
    """Поиск пассажира по номеру паспорта"""
    clear_screen()
    print_header("🔍 ПОИСК ПАССАЖИРА")

    # Ввод паспорта с проверкой формата
    while True:
        passport = input("   Введите номер паспорта (NNNN-NNNNNN): ").strip()
        valid, result = validate_passport(passport)
        if valid:
            passport = result
            break
        print(f"   ❌ {result}")

    found = passengers.find(passport)
    if found:
        info = found.get_info()
        print(f"\n✅ ПАССАЖИР НАЙДЕН:")
        print("=" * 50)
        print(f"   Паспорт:    {info['passport']}")
        print(f"   ФИО:        {info['full_name']}")
        print(f"   Дата рожд.: {info['birth_date']}")
        print(f"   Место выд.: {info['passport_issue']}")
        print("=" * 50)
    else:
        print(f"\n❌ Пассажир с паспортом {passport} не найден!")

    wait_for_enter()


def _delete_passenger(passengers):
    """Удаление пассажира по номеру паспорта"""
    clear_screen()
    print_header("🗑️ УДАЛЕНИЕ ПАССАЖИРА")
    print("⚠️ Внимание! Удаление нельзя отменить.")

    # Ввод паспорта с проверкой формата
    while True:
        passport = input("   Введите номер паспорта (NNNN-NNNNNN): ").strip()
        valid, result = validate_passport(passport)
        if valid:
            passport = result
            break
        print(f"   ❌ {result}")

    found = passengers.find(passport)
    if found:
        print(f"\n📋 Найден пассажир: {found.full_name}")
        if input_yes_no("   Удалить? (д/н): "):
            if passengers.delete(passport):
                print(f"\n✅ Пассажир успешно удалён!")
            else:
                print(f"\n❌ Ошибка при удалении!")
        else:
            print(f"\n🚫 Удаление отменено.")
    else:
        print(f"\n❌ Пассажир с паспортом {passport} не найден!")

    wait_for_enter()


def _list_passengers(passengers):
    """Вывод списка всех пассажиров"""
    clear_screen()
    print_header("📋 ВСЕ ПАССАЖИРЫ")
    all_pass = passengers.get_all_passengers()

    if all_pass:
        print(f"   Всего пассажиров: {len(all_pass)}")
        print("-" * 60)
        for i, p in enumerate(all_pass, 1):
            info = p.get_info()
            print(f"{i:2}. {info['full_name']}")
            print(f"     Паспорт: {info['passport']}")
            print(f"     Дата рожд.: {info['birth_date']}")
            print(f"     Место выд.: {info['passport_issue']}")
            print("-" * 40)
    else:
        print("   📭 Нет зарегистрированных пассажиров")

    wait_for_enter()


def _autofill_passengers(passengers):
    """Автозаполнение тестовыми пассажирами"""
    clear_screen()
    print_header("📦 АВТОЗАПОЛНЕНИЕ ПАССАЖИРОВ")
    print("   Добавление тестовых данных...")
    print("-" * 60)

    test_passengers = [
        ("1234-567890", "Иванов Иван Иванович", "15.05.1985", "Паспортный стол №1 г. Москва"),
        ("2345-678901", "Петров Петр Петрович", "23.08.1990", "УФМС г. Москва"),
        ("3456-789012", "Сидорова Анна Сергеевна", "07.11.1988", "МФЦ г. Санкт-Петербург"),
        ("4567-890123", "Козлов Дмитрий Александрович", "30.01.1979", "ОВД г. Казань"),
        ("5678-901234", "Смирнова Елена Владимировна", "12.03.1995", "Паспортный стол №3 г. Новосибирск"),
        ("6789-012345", "Морозов Алексей Игоревич", "19.09.1982", "УФМС г. Екатеринбург"),
        ("7890-123456", "Волкова Татьяна Николаевна", "25.12.1993", "МФЦ г. Нижний Новгород"),
        ("8901-234567", "Соколов Андрей Павлович", "03.07.1987", "ОВД г. Самара"),
        ("9012-345678", "Михайлова Ольга Викторовна", "14.04.1991", "Паспортный стол №5 г. Ростов"),
        ("0123-456789", "Федоров Сергей Валерьевич", "21.10.1984", "УФМС г. Краснодар"),
    ]

    added = 0
    skipped = 0

    for passport, name, birth, issue in test_passengers:
        if passengers.find(passport):
            print(f"   ⏭️  Пропущен (уже есть): {name} ({passport})")
            skipped += 1
        else:
            p = Passenger(passport, name, birth, issue)
            passengers.insert(p)
            print(f"   ✅ Добавлен: {name} ({passport})")
            added += 1

    print("-" * 60)
    print(f"   📊 Итог: добавлено {added}, пропущено {skipped}")
    wait_for_enter()