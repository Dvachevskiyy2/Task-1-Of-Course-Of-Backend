
#!/usr/bin/env bash

BASE_URL="http://localhost:8000"

TYPE_GAMING="%D0%98%D0%B3%D1%80%D0%BE%D0%B2%D0%BE%D0%B9"
STATUS_AVAILABLE="%D0%94%D0%BE%D1%81%D1%82%D1%83%D0%BF%D0%B5%D0%BD"
STATUS_ACTIVE="%D0%90%D0%BA%D1%82%D0%B8%D0%B2%D0%BD%D0%BE"

echo
echo "========== 1. СОЗДАНИЕ КОМПЬЮТЕРОВ =========="

curl -sS -i -X POST "$BASE_URL/computers" \
  -H "Content-Type: application/json" \
  --data-binary '{"name":"PC-1","type":"\u0418\u0433\u0440\u043e\u0432\u043e\u0439"}'
echo

curl -sS -i -X POST "$BASE_URL/computers" \
  -H "Content-Type: application/json" \
  --data-binary '{"name":"PC-2","type":"\u0421\u0442\u0430\u043d\u0434\u0430\u0440\u0442"}'
echo

curl -sS -i -X POST "$BASE_URL/computers" \
  -H "Content-Type: application/json" \
  --data-binary '{"name":"PC-3","type":"\u0418\u0433\u0440\u043e\u0432\u043e\u0439"}'
echo

echo
echo "========== 2. ПОЛУЧЕНИЕ И ФИЛЬТРАЦИЯ КОМПЬЮТЕРОВ =========="

curl -sS -i "$BASE_URL/computers"
echo

curl -sS -i "$BASE_URL/computers/1"
echo

curl -sS -i "$BASE_URL/computers?type=$TYPE_GAMING"
echo

curl -sS -i "$BASE_URL/computers?status=$STATUS_AVAILABLE"
echo

curl -sS -i "$BASE_URL/computers/999"
echo

echo
echo "========== 3. СОЗДАНИЕ БРОНИРОВАНИЙ =========="

curl -sS -i -X POST "$BASE_URL/bookings" \
  -H "Content-Type: application/json" \
  --data-binary '{"computer_id":1,"customer_name":"\u0418\u0432\u0430\u043d","hours":3}'
echo

curl -sS -i -X POST "$BASE_URL/bookings" \
  -H "Content-Type: application/json" \
  --data-binary '{"computer_id":3,"customer_name":"\u041f\u0451\u0442\u0440","hours":2}'
echo

echo
echo "========== 4. ПОЛУЧЕНИЕ И ФИЛЬТРАЦИЯ БРОНИРОВАНИЙ =========="

curl -sS -i "$BASE_URL/bookings"
echo

curl -sS -i "$BASE_URL/bookings/1"
echo

curl -sS -i "$BASE_URL/bookings?status=$STATUS_ACTIVE"
echo

curl -sS -i "$BASE_URL/bookings?computer_id=1"
echo

curl -sS -i "$BASE_URL/bookings/999"
echo

echo
echo "========== 5. ПРОВЕРКА ОШИБОК =========="

curl -sS -i -X POST "$BASE_URL/bookings" \
  -H "Content-Type: application/json" \
  --data-binary '{"computer_id":1,"customer_name":"\u0414\u0440\u0443\u0433\u043e\u0439","hours":1}'
echo

curl -sS -i -X POST "$BASE_URL/computers" \
  -H "Content-Type: application/json" \
  --data-binary '{"name":"PC-BAD","type":"\u041d\u0435\u0438\u0437\u0432\u0435\u0441\u0442\u043d\u044b\u0439"}'
echo

curl -sS -i -X POST "$BASE_URL/bookings" \
  -H "Content-Type: application/json" \
  --data-binary '{"computer_id":2,"customer_name":"Test","hours":0}'
echo

echo
echo "========== 6. ИЗМЕНЕНИЕ ДАННЫХ =========="

curl -sS -i -X PATCH "$BASE_URL/computers/2" \
  -H "Content-Type: application/json" \
  --data-binary '{"name":"PC-2-UPDATED","type":"\u0421\u0442\u0430\u043d\u0434\u0430\u0440\u0442"}'
echo

curl -sS -i -X PATCH "$BASE_URL/bookings/1" \
  -H "Content-Type: application/json" \
  --data-binary '{"customer_name":"\u0418\u0432\u0430\u043d \u041f\u0435\u0442\u0440\u043e\u0432","hours":5}'
echo

curl -sS -i "$BASE_URL/computers/2"
echo

curl -sS -i "$BASE_URL/bookings/1"
echo

echo
echo "========== 7. ЗАВЕРШЕНИЕ И ОТМЕНА =========="

curl -sS -i -X POST "$BASE_URL/bookings/1/complete"
echo

curl -sS -i -X PATCH "$BASE_URL/bookings/1" \
  -H "Content-Type: application/json" \
  --data-binary '{"customer_name":"Test","hours":1}'
echo

curl -sS -i -X POST "$BASE_URL/bookings/2/cancel"
echo

curl -sS -i "$BASE_URL/computers"
echo

echo
echo "========== 8. УДАЛЕНИЕ БРОНИРОВАНИЙ =========="

curl -sS -i -X DELETE "$BASE_URL/bookings/1"
echo

curl -sS -i -X DELETE "$BASE_URL/bookings/2"
echo

curl -sS -i "$BASE_URL/bookings"
echo

echo
echo "========== 9. УДАЛЕНИЕ КОМПЬЮТЕРОВ =========="

curl -sS -i -X DELETE "$BASE_URL/computers/1"
echo

curl -sS -i -X DELETE "$BASE_URL/computers/2"
echo

curl -sS -i -X DELETE "$BASE_URL/computers/3"
echo

curl -sS -i "$BASE_URL/computers"
echo

echo
echo "========== 10. НЕСУЩЕСТВУЮЩИЙ МАРШРУТ =========="

curl -sS -i "$BASE_URL/unknown"
echo

echo
echo "========== ТЕСТИРОВАНИЕ ЗАВЕРШЕНО =========="
