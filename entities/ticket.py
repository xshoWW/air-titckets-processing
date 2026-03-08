class Ticket:
    """Класс билета"""
    
    def __init__(self, ticket_id, passport, flight_number):
        self.ticket_id = ticket_id      # ключ
        self.passport = passport        # паспорт пассажира
        self.flight_number = flight_number  # номер рейса
    
    def __repr__(self):
        return f"Билет №{self.ticket_id}: {self.passport} -> {self.flight_number}"
    
    def get_info(self):
        return {
            "ticket_id": self.ticket_id,
            "passport": self.passport,
            "flight_number": self.flight_number
        }