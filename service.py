from models import Computer, Booking

class GameClubService:
    def __init__(self):
        self.computers = {} # Словарь компьютеров
        self.bookings = {} # Словарь бронирования
        self.next_computer_id = 1
        self.next_booking_id = 1

    def create_computer(self, name, computer_type):
        if not name.strip():
            raise ValueError("Имя компьютера не может быть пустым")

        computer = Computer(self.next_computer_id, name, computer_type)
        self.computers[computer.id] = computer
        self.next_computer_id += 1
        return computer

    def create_booking(self, computer_id, customer_name, hours):
        if computer_id not in self.computers:
            raise ValueError("Компьютер не найден")

        computer = self.computers[computer_id]

        if computer.status != "Доступен":
            raise ValueError("Компьютер уже занят")

        if not customer_name.strip():
            raise ValueError("Имя пользователя не может быть пустым")

        if not isinstance(hours, int) or hours <= 0:
            raise ValueError("Неверно введено кол-во часов")

        booking = Booking(self.next_booking_id, computer_id, customer_name, hours)
        self.bookings[booking.id] = booking
        self.next_booking_id += 1
        computer.status = "Занят"
        return booking

    def complete_booking(self, booking_id):
        if booking_id not in self.bookings:
            raise ValueError("Бронирование не найдено")

        booking = self.bookings[booking_id]

        if booking.status != "Активно":
            raise ValueError("Бронирование уже не активно")

        computer = self.computers[booking.computer_id]

        booking.status = "Завершено"
        computer.status = "Доступен"
        return booking

    def cancel_booking(self, booking_id):
        if booking_id not in self.bookings:
            raise ValueError("Бронирование не найдено")

        booking = self.bookings[booking_id]

        if booking.status != "Активно":
            raise ValueError("Бронирование неактивно, отменить нельзя")

        computer = self.computers[booking.computer_id]
        booking.status = "Отменено"
        computer.status = "Досутпен"
        return booking

    def get_computer(self, computer_id): # получаем компьютер по отдельности
        if computer_id not in self.computers:
            raise ValueError("Компьютер не найден")

        return self.computers[computer_id]

    def get_computers(self): # получаем все компьютеры
        return list(self.computers.values())

    def filter_computers(self, computer_type=None, status=None):
        result = []

        for computer in self.computers.values():
            if computer_type is not None and computer.type != computer_type:
                continue
            if status is not None and computer.status != status:
                continue

            result.append(computer)
        return result

    def get_booking(self, booking_id):
        if booking_id not in self.bookings:
            raise ValueError("Бронирование не найдено")
        return self.bookings[booking_id]

    def get_bookings(self):
        return list(self.bookings.values())

    def filter_bookings(self, status=None, computer_id=None):
        result = []
        for booking in self.bookings.values():
            if status is not None and booking.status != status:
                continue

            if computer_id is not None and booking.computer_id != computer_id:
                continue
            result.append(booking)
        return result

    def update_computer(self, computer_id, name=None, computer_type=None):
        if computer_id not in self.computers:
            raise ValueError("Компьютер не найден")

        computer = self.computers[computer_id]

        if name is not None:
            if not name.strip():
                raise ValueError("Имя компьютера не может быть пустым")
            computer.name = name

        if computer_type is not None:
            if computer.status == "Занят":
                raise ValueError("Нельзя менять тип занятого компьютера")

            if computer_type == "Стандарт":
                computer.hourly_price = 100
            elif computer_type == "Игровой":
                computer.hourly_price = 200
            else:
                raise ValueError("Неизвестный тип компьютера")

            computer.type = computer_type

        return computer

    def update_booking(self, booking_id, customer_name=None, hours=None):
        if booking_id not in self.bookings:
            raise ValueError("Бронирование не найдено")

        booking = self.bookings[booking_id]

        if booking.status != "Активно":
            raise ValueError("Можно менять только активное бронирование")

        if customer_name is not None:
            if not customer_name.strip():
                raise ValueError("Имя пользователя не может быть пустым")
            booking.customer_name = customer_name

        if hours is not None:
            if type(hours) is not int or hours <= 0:
                raise ValueError("Неверно введено кол-во часов")
            booking.hours = hours

        return booking

    def delete_booking(self, booking_id):
        if booking_id not in self.bookings:
            raise ValueError("Бронирование не найдено")

        booking = self.bookings[booking_id]

        if booking.status == "Активно":
            computer = self.computers[booking.computer_id]
            computer.status = "Доступен"

        del self.bookings[booking_id]

    def delete_computer(self, computer_id):
        if computer_id not in self.computers:
            raise ValueError("Компьютер не найден")

        computer = self.computers[computer_id]

        if computer.status == "Занят":
            raise ValueError("Нельзя удалить занятый компьютер")

        for booking in self.bookings.values():
            if booking.computer_id == computer_id:
                raise ValueError("Сначала удалите связанные бронирования")

        del self.computers[computer_id]
