def counting_sort_tickets(tickets):
    """Сортировка билетов распределением по ticket_id."""
    if not tickets:
        return []

    # Находим максимальный ID билета
    max_id = max(t.ticket_id for t in tickets)
    
    count = [0] * (max_id + 1)
    output = [None] * len(tickets)
    
    # Подсчитываем вхождения
    for ticket in tickets:
        count[ticket.ticket_id] += 1
        
    # Модифицируем массив count для позиций
    for i in range(1, len(count)):
        count[i] += count[i - 1]
        
    # Строим выходной массив (идем с конца для стабильности)
    for i in range(len(tickets) - 1, -1, -1):
        ticket = tickets[i]
        output[count[ticket.ticket_id] - 1] = ticket
        count[ticket.ticket_id] -= 1
        
    return output