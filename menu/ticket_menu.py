import random
from entities.ticket import Ticket
from algorithms.sorting import counting_sort_tickets
from algorithms.boyer_moore import boyer_moore_search
from utils.console import clear_screen, print_header, wait_for_enter, input_int

def sell_ticket(passengers, flights, tickets):
    clear_screen()
    print_header("💳 ПРОДАЖА БИЛЕТА")
    
    passport = input("Введите паспорт пассажира (формат NNNN-NNNNNN): ").strip()
    passenger = passengers.find(passport)
    if not passenger:
        print("❌ Пассажир не найден в системе!")
        wait_for_enter()
        return

    flight_num = input("Введите номер рейса (например AFL-123): ").strip().upper()
    flight = flights.root
    # Простой поиск в АВЛ по ключу
    target_flight = None
    current = flights.root
    while current:
        if flight_num == current.flight.flight_number:
            target_flight = current.flight
            break
        elif flight_num < current.flight.flight_number:
            current = current.left
        else:
            current = current.right

    if not target_flight:
        print("❌ Рейс не найден!")
        wait_for_enter()
        return

    if target_flight.free_seats <= 0:
        print("❌ На этот рейс нет свободных мест!")
        wait_for_enter()
        return

    # Генерируем уникальный ID для билета
    ticket_id = random.randint(1000, 9999)
    while tickets.find(ticket_id):
        ticket_id = random.randint(1000, 9999)

    # Уменьшаем кол-во свободных мест
    target_flight.free_seats -= 1
    
    # Создаем и добавляем билет
    new_ticket = Ticket(ticket_id, passenger.passport, target_flight.flight_number)
    tickets.insert(new_ticket)
    
    print(f"\n✅ Билет успешно продан! Номер билета: {ticket_id}")
    wait_for_enter()

def return_ticket(passengers, flights, tickets):
    clear_screen()
    print_header("↩️  ВОЗВРАТ БИЛЕТА")
    
    ticket_id = input_int("Введите номер билета для возврата: ")
    ticket = tickets.find(ticket_id)
    
    if not ticket:
        print("❌ Билет с таким номером не найден.")
        wait_for_enter()
        return

    # Находим рейс и увеличиваем кол-во мест
    current = flights.root
    while current:
        if ticket.flight_number == current.flight.flight_number:
            current.flight.free_seats += 1
            break
        elif ticket.flight_number < current.flight.flight_number:
            current = current.left
        else:
            current = current.right

    tickets.delete(ticket_id)
    print("\n✅ Билет успешно возвращен. Место на рейсе освобождено.")
    wait_for_enter()

def search_passenger_by_name(passengers):
    clear_screen()
    print_header("🔍 ПОИСК ПАССАЖИРА ПО ФИО (Бойер-Мур)")
    
    query = input("Введите фрагмент ФИО для поиска: ").strip()
    if not query:
        print("❌ Пустой запрос.")
        wait_for_enter()
        return
        
    found_any = False
    print("\nРезультаты поиска:")
    # Итерация по хеш-таблице напрямую (т.к. метод get_all может быть не реализован)
    for i in range(passengers.size):
        if passengers._states[i] == passengers.OCCUPIED:
            passenger = passengers._table[i]
            # Применяем Бойера-Мура
            if boyer_moore_search(passenger.full_name, query) != -1:
                print(f" - {passenger.full_name} (Паспорт: {passenger.passport})")
                found_any = True
                
    if not found_any:
        print("   📭 Пассажиров не найдено.")
    wait_for_enter()

def search_flight_by_arrival(flights):
    clear_screen()
    print_header("🔍 ПОИСК РЕЙСА ПО АЭРОПОРТУ ПРИБЫТИЯ")
    
    query = input("Введите фрагмент названия аэропорта (например 'Сочи'): ").strip()
    
    # Получаем все рейсы через обратный обход (левый-правый-корень)
    all_flights = flights.reverse_traversal()
    if not all_flights:
        print("❌ В системе нет рейсов.")
        wait_for_enter()
        return

    found_any = False
    print("\nРезультаты поиска:")
    for f in all_flights:
        if boyer_moore_search(f.arrival_airport, query) != -1:
            print(f" - Рейс {f.flight_number}: {f.departure_airport} ✈️  {f.arrival_airport}")
            found_any = True
            
    if not found_any:
        print("   📭 Рейсов не найдено.")
    wait_for_enter()

def display_tickets_sorted(tickets):
    clear_screen()
    print_header("📋 ВСЕ БИЛЕТЫ (Сортировка распределением)")
    
    all_tickets = tickets.get_all()
    if not all_tickets:
        print("   📭 В системе пока нет проданных билетов.")
        wait_for_enter()
        return

    sorted_tickets = counting_sort_tickets(all_tickets)
    
    print(f"{'ID Билета':<12} | {'Рейс':<10} | {'Паспорт пассажира'}")
    print("-" * 50)
    for t in sorted_tickets:
        print(f"{t.ticket_id:<12} | {t.flight_number:<10} | {t.passport}")
        
    print(f"\nВсего билетов: {len(sorted_tickets)}")
    wait_for_enter()