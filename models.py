# Основной класс компьютера. Инициализирую стандартное поведение всех ПК
# и задаю проверку на тип, пока что их 2, иначе принудительно вызываем ошибку
class Computer:
    def __init__(self, computer_id, name, computer_type):
        self.id = computer_id
        self.name = name
        self.type = computer_type
        self.status = "Доступен"

        if computer_type == "Стандарт":
            self.hourly_price = 100
        elif computer_type == "Игровой":
            self.hourly_price = 200
        else:
            raise ValueError("Неизвестный тип компьютера")

# Класс бронирования
class Booking:
    def __init__(self, booking_id, computer_id, customer_name, hours):
        self.id = booking_id
        self.computer_id = computer_id
        self.customer_name = customer_name
        self.hours = hours
        self.status = "Активно"