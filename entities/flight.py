class Flight:
    """Класс рейса"""
    def __init__(self, flight_number, airline, departure_airport, arrival_airport,
                 departure_date, departure_time, total_seats, free_seats):
        self.flight_number = flight_number
        self.airline = airline
        self.departure_airport = departure_airport
        self.arrival_airport = arrival_airport
        self.departure_date = departure_date
        self.departure_time = departure_time
        self.total_seats = total_seats
        self.free_seats = free_seats

    def __repr__(self):
        return self.flight_number

    def __str__(self):
        return self.flight_number
    
    def get_info(self):
        return {
            "flight_number": self.flight_number,
            "airline": self.airline,
            "departure_airport": self.departure_airport,
            "arrival_airport": self.arrival_airport,
            "departure_date": self.departure_date,
            "departure_time": self.departure_time,
            "total_seats": self.total_seats,
            "free_seats": self.free_seats
        }