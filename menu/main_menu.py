from algorithms.passenger_hash import HashTable
from algorithms.flight_avl import AVLTree
from algorithms.ticket_skiplist import SkipList   
from .passenger_menu import menu_passengers
from .flight_menu import menu_flights
from .ticket_menu import (
    sell_ticket, return_ticket,
    search_passenger_by_name, search_flight_by_arrival,
    display_tickets_sorted
)
from utils.console import clear_screen, print_header, wait_for_enter

def main_menu():
    passengers = HashTable()
    flights = AVLTree()
    tickets = SkipList()

    while True:
        clear_screen()
        print_header("🛫 СИСТЕМА ПРОДАЖИ АВИАБИЛЕТОВ 🛬")
        print("1. 🧑 Пассажиры")
        print("2. ✈️  Рейсы")
        print("3. 💳 Продажа билета")
        print("4. ↩️  Возврат билета")
        print("5. 🔍 Поиск пассажира по ФИО")
        print("6. 🔍 Поиск рейса по аэропорту")
        print("7. 📋 Все рейсы (обход)")
        print("8. 📋 Все билеты")
        print("0. 🚪 Выход")
        print("-" * 60)
        
        choice = input("👉 Выберите (0-8): ").strip()

        if choice == "1":
            menu_passengers(passengers)
        elif choice == "2":
            menu_flights(flights)
        elif choice == "3":
            sell_ticket(passengers, flights, tickets)
        elif choice == "4":
            return_ticket(passengers, flights, tickets)
        elif choice == "5":
            search_passenger_by_name(passengers)
        elif choice == "6":
            search_flight_by_arrival(flights)
        elif choice == "7":
            clear_screen()
            print_header("📋 ВСЕ РЕЙСЫ")
            result = flights.reverse_traversal()
            if result:
                for i, f in enumerate(result, 1):
                    print(f"{i:2}. {f.flight_number}")
            else:
                print("   📭 Нет рейсов")
            wait_for_enter()
        elif choice == "8":
            display_tickets_sorted(tickets)
        elif choice == "0":
            break
        else:
            print("❌ Неверный выбор!")
            wait_for_enter()