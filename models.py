COMPUTER_TYPES = {
    "Стандарт": 100,
    "Игровой": 200
}


class Computer:
    def __init__(self, computer_id, name, computer_type):
        if computer_type not in COMPUTER_TYPES:
            raise ValueError("Неизвестный тип компьютера")

        self.id = computer_id
        self.name = name
        self.type = computer_type
        self.status = "Доступен"
        self.hourly_price = COMPUTER_TYPES[computer_type]


class Booking:
    def __init__(self, booking_id, computer_id, customer_name, hours, total_price=0):
        self.id = booking_id
        self.computer_id = computer_id
        self.customer_name = customer_name
        self.hours = hours
        self.total_price = total_price
        self.status = "Активно"
