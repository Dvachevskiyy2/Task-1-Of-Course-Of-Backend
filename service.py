from models import COMPUTER_TYPES, Computer, Booking


class NotFoundError(ValueError):
    pass


class ValidationError(ValueError):
    pass


class GameClubService:
    def __init__(self):
        self.computers = {}
        self.bookings = {}
        self.next_computer_id = 1
        self.next_booking_id = 1

    def create_computer(self, name, computer_type):
        if not isinstance(name, str) or not name.strip():
            raise ValidationError("Имя компьютера не может быть пустым")

        if computer_type not in COMPUTER_TYPES:
            raise ValidationError("Неизвестный тип компьютера")

        computer = Computer(self.next_computer_id, name, computer_type)
        self.computers[computer.id] = computer
        self.next_computer_id += 1
        return computer

    def create_booking(self, computer_id, customer_name, hours):
        if computer_id not in self.computers:
            raise NotFoundError("Компьютер не найден")

        computer = self.computers[computer_id]

        if computer.status != "Доступен":
            raise ValidationError("Компьютер уже занят")

        if not isinstance(customer_name, str) or not customer_name.strip():
            raise ValidationError("Имя пользователя не может быть пустым")

        if not isinstance(hours, int) or isinstance(hours, bool) or hours <= 0:
            raise ValidationError("Неверно введено кол-во часов")

        booking = Booking(
            self.next_booking_id,
            computer_id,
            customer_name,
            hours,
            computer.hourly_price * hours
        )
        self.bookings[booking.id] = booking
        self.next_booking_id += 1
        computer.status = "Занят"
        return booking

    def complete_booking(self, booking_id):
        if booking_id not in self.bookings:
            raise NotFoundError("Бронирование не найдено")

        booking = self.bookings[booking_id]

        if booking.status != "Активно":
            raise ValidationError("Бронирование уже не активно")

        computer = self.computers[booking.computer_id]

        booking.status = "Завершено"
        computer.status = "Доступен"
        return booking

    def cancel_booking(self, booking_id):
        if booking_id not in self.bookings:
            raise NotFoundError("Бронирование не найдено")

        booking = self.bookings[booking_id]

        if booking.status != "Активно":
            raise ValidationError("Бронирование неактивно, отменить нельзя")

        computer = self.computers[booking.computer_id]
        booking.status = "Отменено"
        computer.status = "Доступен"
        return booking

    def get_computer(self, computer_id):
        if computer_id not in self.computers:
            raise NotFoundError("Компьютер не найден")

        return self.computers[computer_id]

    def get_computers(self):
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
            raise NotFoundError("Бронирование не найдено")
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
            raise NotFoundError("Компьютер не найден")

        computer = self.computers[computer_id]

        new_name = computer.name
        if name is not None:
            if not isinstance(name, str) or not name.strip():
                raise ValidationError("Имя компьютера не может быть пустым")
            new_name = name

        new_type = computer.type
        new_price = computer.hourly_price
        if computer_type is not None:
            if computer.status == "Занят":
                raise ValidationError("Нельзя менять тип занятого компьютера")

            if computer_type not in COMPUTER_TYPES:
                raise ValidationError("Неизвестный тип компьютера")

            new_type = computer_type
            new_price = COMPUTER_TYPES[computer_type]

        computer.name = new_name
        computer.type = new_type
        computer.hourly_price = new_price
        return computer

    def update_booking(self, booking_id, customer_name=None, hours=None):
        if booking_id not in self.bookings:
            raise NotFoundError("Бронирование не найдено")

        booking = self.bookings[booking_id]

        if booking.status != "Активно":
            raise ValidationError("Можно менять только активное бронирование")

        new_customer_name = booking.customer_name
        if customer_name is not None:
            if not isinstance(customer_name, str) or not customer_name.strip():
                raise ValidationError("Имя пользователя не может быть пустым")
            new_customer_name = customer_name

        new_hours = booking.hours
        if hours is not None:
            if not isinstance(hours, int) or isinstance(hours, bool) or hours <= 0:
                raise ValidationError("Неверно введено кол-во часов")
            new_hours = hours

        computer = self.computers[booking.computer_id]

        booking.customer_name = new_customer_name
        booking.hours = new_hours
        booking.total_price = computer.hourly_price * new_hours
        return booking

    def delete_booking(self, booking_id):
        if booking_id not in self.bookings:
            raise NotFoundError("Бронирование не найдено")

        booking = self.bookings[booking_id]

        if booking.status == "Активно":
            computer = self.computers[booking.computer_id]
            computer.status = "Доступен"

        del self.bookings[booking_id]

    def delete_computer(self, computer_id):
        if computer_id not in self.computers:
            raise NotFoundError("Компьютер не найден")

        computer = self.computers[computer_id]

        if computer.status == "Занят":
            raise ValidationError("Нельзя удалить занятый компьютер")

        for booking in self.bookings.values():
            if booking.computer_id == computer_id:
                raise ValidationError("Сначала удалите связанные бронирования")

        del self.computers[computer_id]
