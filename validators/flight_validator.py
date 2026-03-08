import re

def validate_flight_number(flight_num):
    """
    Проверка номера рейса: AAA-NNN
    """
    if not flight_num or not isinstance(flight_num, str):
        return False, "Номер рейса не может быть пустым"
    
    flight_num = flight_num.strip().upper()
    
    if not re.match(r'^[A-Z]{3}-\d{3}$', flight_num):
        return False, "Неверный формат. Используйте AAA-NNN (например AFL-123)"
    
    return True, flight_num


def validate_airline(airline):
    """
    Проверка названия авиакомпании
    """
    if not airline or not isinstance(airline, str):
        return False, "Название авиакомпании не может быть пустым"
    
    airline = airline.strip()
    
    if len(airline) < 2:
        return False, "Название авиакомпании должно содержать хотя бы 2 символа"
    
    return True, airline


def validate_airport(airport, field_name="Аэропорт"):
    """
    Проверка названия аэропорта
    Возвращает (True, очищенное_значение) или (False, сообщение_об_ошибке)
    """
    if not airport or not isinstance(airport, str):
        return False, f"{field_name} не может быть пустым"
    
    airport = airport.strip()
    
    if len(airport) < 3:
        return False, f"{field_name} должен содержать хотя бы 3 символа"
    
    return True, airport


def validate_date(date):
    """
    Проверка даты: ДД.ММ.ГГГГ
    """
    if not date or not isinstance(date, str):
        return False, "Дата не может быть пустой"
    
    date = date.strip()
    
    if not re.match(r'^\d{2}\.\d{2}\.\d{4}$', date):
        return False, "Неверный формат. Используйте ДД.ММ.ГГГГ (например 22.02.2026)"
    
    try:
        day, month, year = map(int, date.split('.'))
    except ValueError:
        return False, "Неверный формат даты"
    
    if not (1 <= day <= 31):
        return False, "День должен быть от 1 до 31"
    
    if not (1 <= month <= 12):
        return False, "Месяц должен быть от 1 до 12"
    
    if not (2020 <= year <= 2030):
        return False, "Год должен быть от 2020 до 2030 (актуальные рейсы)"
    
    days_in_month = [31, 29 if year % 4 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    if day > days_in_month[month - 1]:
        return False, f"В месяце {month} нет {day} дней"
    
    return True, date


def validate_time(time):
    """
    Проверка времени: ЧЧ:ММ
    """
    if not time or not isinstance(time, str):
        return False, "Время не может быть пустым"
    
    time = time.strip()
    
    if not re.match(r'^\d{2}:\d{2}$', time):
        return False, "Неверный формат. Используйте ЧЧ:ММ (например 10:30)"
    
    try:
        hours, minutes = map(int, time.split(':'))
    except ValueError:
        return False, "Неверный формат времени"
    
    if not (0 <= hours <= 23):
        return False, "Часы должны быть от 0 до 23"
    
    if not (0 <= minutes <= 59):
        return False, "Минуты должны быть от 0 до 59"
    
    return True, time


def validate_seats(total_seats, free_seats):
    """
    Проверка количества мест
    """
    if not isinstance(total_seats, int) or total_seats <= 0:
        return False, "Количество мест должно быть положительным числом"
    
    if not isinstance(free_seats, int) or free_seats < 0:
        return False, "Количество свободных мест не может быть отрицательным"
    
    if free_seats > total_seats:
        return False, "Свободных мест не может быть больше, чем всего мест"
    
    return True, (total_seats, free_seats)


def validate_flight_data(flight_num, airline, departure, arrival, date, time, total_seats, free_seats):
    """
    Комплексная проверка всех данных рейса
    Возвращает (True, кортеж_данных) или (False, список_ошибок)
    """
    errors = []
    
    valid, result = validate_flight_number(flight_num)
    if not valid:
        errors.append(f"Номер рейса: {result}")
    else:
        flight_num = result
    
    valid, result = validate_airline(airline)
    if not valid:
        errors.append(f"Авиакомпания: {result}")
    else:
        airline = result
    
    valid, result = validate_airport(departure, "Аэропорт отправления")
    if not valid:
        errors.append(result)
    else:
        departure = result
    
    valid, result = validate_airport(arrival, "Аэропорт прибытия")
    if not valid:
        errors.append(result)
    else:
        arrival = result
    
    valid, result = validate_date(date)
    if not valid:
        errors.append(f"Дата: {result}")
    else:
        date = result
    
    valid, result = validate_time(time)
    if not valid:
        errors.append(f"Время: {result}")
    else:
        time = result
    
    valid, result = validate_seats(total_seats, free_seats)
    if not valid:
        errors.append(result)
    else:
        total_seats, free_seats = result
    
    if errors:
        return False, errors
    
    return True, (flight_num, airline, departure, arrival, date, time, total_seats, free_seats)