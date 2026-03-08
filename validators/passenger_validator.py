import re

def validate_passport(passport):
    """
    Проверка номера паспорта: NNNN-NNNNNN
    """
    if not passport or not isinstance(passport, str):
        return False, "Номер паспорта не может быть пустым"
    
    passport = passport.strip()
    
    if not re.match(r'^\d{4}-\d{6}$', passport):
        return False, "Неверный формат. Используйте NNNN-NNNNNN (например 1234-567890)"
    
    return True, passport


def validate_full_name(name):
    """
    Проверка ФИО (не пустое, минимальная длина)
    """
    if not name or not isinstance(name, str):
        return False, "ФИО не может быть пустым"
    
    name = name.strip()
    
    if len(name) < 3:
        return False, "ФИО должно содержать хотя бы 3 символа"
    
    if len(name) > 100:
        return False, "ФИО слишком длинное (максимум 100 символов)"
    
    return True, name


def validate_birth_date(date):
    """
    Проверка даты рождения: ДД.ММ.ГГГГ
    """
    if not date or not isinstance(date, str):
        return False, "Дата рождения не может быть пустой"
    
    date = date.strip()
    
    # Проверка формата
    if not re.match(r'^\d{2}\.\d{2}\.\d{4}$', date):
        return False, "Неверный формат. Используйте ДД.ММ.ГГГГ (например 22.02.2026)"
    
    # Разбираем дату
    try:
        day, month, year = map(int, date.split('.'))
    except ValueError:
        return False, "Неверный формат даты"
    
    # Проверка диапазонов
    if not (1 <= day <= 31):
        return False, "День должен быть от 1 до 31"
    
    if not (1 <= month <= 12):
        return False, "Месяц должен быть от 1 до 12"
    
    if not (1900 <= year <= 2100):
        return False, "Год должен быть от 1900 до 2100"
    
    # Проверка количества дней в месяце
    days_in_month = [31, 29 if year % 4 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    if day > days_in_month[month - 1]:
        return False, f"В месяце {month} нет {day} дней"
    
    return True, date


def validate_passport_issue(issue):
    """
    Проверка места выдачи паспорта (не пустое)
    """
    if not issue or not isinstance(issue, str):
        return False, "Место выдачи паспорта не может быть пустым"
    
    issue = issue.strip()
    
    if len(issue) < 3:
        return False, "Место выдачи должно содержать хотя бы 3 символа"
    
    return True, issue


# Для обратной совместимости оставляем старую функцию
def validate_passenger_data(passport, full_name, birth_date, passport_issue):
    """
    Комплексная проверка всех данных (возвращает список ошибок)
    """
    errors = []
    
    # Проверяем каждое поле
    valid, result = validate_passport(passport)
    if not valid:
        errors.append(f"Паспорт: {result}")
    
    valid, result = validate_full_name(full_name)
    if not valid:
        errors.append(f"ФИО: {result}")
    
    valid, result = validate_birth_date(birth_date)
    if not valid:
        errors.append(f"Дата рождения: {result}")
    
    valid, result = validate_passport_issue(passport_issue)
    if not valid:
        errors.append(f"Место выдачи: {result}")
    
    if errors:
        return False, errors
    
    return True, (passport, full_name, birth_date, passport_issue)