from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs

from service import GameClubService

service = GameClubService()

class GameClubHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        params = parse_qs(parsed_url.query)

        try:
            # Получение и фильтрация компьютеров
            if path == "/computers":
                computer_type = params.get("type", [None])[0]
                status = params.get("status", [None])[0]

                computers = service.filter_computers(
                    computer_type,
                    status
                )
                self.send_json(computers)

            # Получение одного компьютера
            elif path.startswith("/computers/"):
                computer_id = int(path.split("/")[-1])
                computer = service.get_computer(computer_id)
                self.send_json(computer)

            # Получение и фильтрация бронирований
            elif path == "/bookings":
                status = params.get("status", [None])[0]
                computer_id = params.get("computer_id", [None])[0]

                if computer_id is not None:
                    computer_id = int(computer_id)

                bookings = service.filter_bookings(
                    status,
                    computer_id
                )
                self.send_json(bookings)

            # Получение одного бронирования
            elif path.startswith("/bookings/"):
                booking_id = int(path.split("/")[-1])
                booking = service.get_booking(booking_id)
                self.send_json(booking)

            else:
                self.send_json({"error": "Маршрут не найден"}, 404)

        except ValueError as error:
            message = str(error)

            if "не найден" in message.lower():
                self.send_json({"error": message}, 404)
            else:
                self.send_json({"error": message}, 400)

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()

        if isinstance(data, list):
            result = []

            for item in data:
                result.append(item.__dict__)

            data = result

        elif not isinstance(data, dict):
            data = data.__dict__

        response = json.dumps(data, ensure_ascii=False)
        self.wfile.write(response.encode("utf-8"))

    def read_json(self):
        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length)
        data = json.loads(body.decode("utf-8")) # декодируем байты в строку, а loads
        # превращает json строку в словарь
        return data

    def do_POST(self):
        path = urlparse(self.path).path

        try:
            # Создание компьютера
            if path == "/computers":
                data = self.read_json()

                computer = service.create_computer(
                    data["name"],
                    data["type"]
                )

                self.send_json(computer, 201)

            # Создание бронирования
            elif path == "/bookings":
                data = self.read_json()

                booking = service.create_booking(
                    data["computer_id"],
                    data["customer_name"],
                    data["hours"]
                )

                self.send_json(booking, 201)

            # Завершение бронирования
            elif path.startswith("/bookings/") and path.endswith("/complete"):
                booking_id = int(path.split("/")[-2])

                booking = service.complete_booking(booking_id)

                self.send_json(booking)

            # Отмена бронирования
            elif path.startswith("/bookings/") and path.endswith("/cancel"):
                booking_id = int(path.split("/")[-2])

                booking = service.cancel_booking(booking_id)

                self.send_json(booking)

            else:
                self.send_json({"error": "Маршрут не найден"}, 404)

        except ValueError as error:
            message = str(error)

            if "не найден" in message.lower():
                self.send_json({"error": message}, 404)
            else:
                self.send_json({"error": message}, 400)

    def do_PATCH(self):
        path = urlparse(self.path).path

        try:
            data = self.read_json()

            # Изменение компьютера
            if path.startswith("/computers/"):
                computer_id = int(path.split("/")[-1])

                computer = service.update_computer(
                    computer_id,
                    data.get("name"),
                    data.get("type")
                )

                self.send_json(computer)

            # Изменение бронирования
            elif path.startswith("/bookings/"):
                booking_id = int(path.split("/")[-1])

                booking = service.update_booking(
                    booking_id,
                    data.get("customer_name"),
                    data.get("hours")
                )

                self.send_json(booking)

            else:
                self.send_json({"error": "Маршрут не найден"}, 404)

        except ValueError as error:
            message = str(error)

            if "не найден" in message.lower():
                self.send_json({"error": message}, 404)
            else:
                self.send_json({"error": message}, 400)

    def do_DELETE(self):
        path = urlparse(self.path).path

        try:
            # Удаление компьютера
            if path.startswith("/computers/"):
                computer_id = int(path.split("/")[-1])
                service.delete_computer(computer_id)

                self.send_json({"message": "Компьютер удален"})

            # Удаление бронирования
            elif path.startswith("/bookings/"):
                booking_id = int(path.split("/")[-1])
                service.delete_booking(booking_id)

                self.send_json({"message": "Бронирование удалено"})

            else:
                self.send_json({"error": "Маршрут не найден"}, 404)

        except ValueError as error:
            message = str(error)

            if "не найден" in message.lower():
                self.send_json({"error": message}, 404)
            else:
                self.send_json({"error": message}, 400)


server = HTTPServer(("localhost", 8000), GameClubHandler)
print("Сервер запущен на http://localhost:8000")
server.serve_forever()

