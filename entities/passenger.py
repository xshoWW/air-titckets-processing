class Passenger:
    """Класс пассажира"""
    def __init__(self, passport, full_name, birth_date, passport_issue):
        self.passport = passport
        self.full_name = full_name
        self.birth_date = birth_date
        self.passport_issue = passport_issue

    def __repr__(self):
        return f"Пассажир: {self.full_name}, паспорт {self.passport}"
    
    def get_info(self):
        return {
            "passport": self.passport,
            "full_name": self.full_name,
            "birth_date": self.birth_date,
            "passport_issue": self.passport_issue
        }