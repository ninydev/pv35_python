import socket
import time
import json
from datetime import datetime

# Настройки
HOST = '127.0.0.1'  # Localhost
PORT = 3321  # Наш кастомный порт
DELAY = 10  # Задержка в секундах


def start_server():
    # 1. Создаем сокет (AF_INET = IPv4, SOCK_STREAM = TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2. Привязываем сокет к адресу и порту
    # Позволяет повторно использовать порт сразу после закрытия
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))

    # 3. Слушаем входящие соединения
    server_socket.listen(5)
    print(f"Сервер запущен на http://{HOST}:{PORT}")
    print(f"Задержка ответа: {DELAY} сек. Ожидание подключения...")

    try:
        while True:
            # 4. Принимаем входящий звонок
            client_socket, address = server_socket.accept()
            print(f"Получен запрос от {address}")

            # 5. Читаем данные запроса (даже если они нам не нужны)
            request = client_socket.recv(1024).decode('utf-8')
            # print(f"Содержимое запроса:\n{request}")

            # Имитируем тяжелую работу (как в финтехе)
            time.sleep(DELAY)

            # 6. Формируем данные (JSON)
            now = datetime.now()
            response_data = {
                "status": "success",
                "server_time": now.strftime("%H:%M:%S"),
                "server_date": now.strftime("%Y-%m-%d"),
                "message": f"Wait for {DELAY} seconds"
            }
            payload = json.dumps(response_data)

            # 7. Формируем HTTP-ответ (минимальный заголовок)
            # Без этого браузер не поймет, что это HTTP
            http_response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: application/json\r\n"
                f"Content-Length: {len(payload)}\r\n"
                "Connection: close\r\n"
                "\r\n"
                f"{payload}"
            )

            # 8. Отправляем и закрываем
            client_socket.sendall(http_response.encode('utf-8'))
            client_socket.close()
            print(f"Ответ отправлен. Сокет закрыт.\n")

    except KeyboardInterrupt:
        print("\nСервер остановлен пользователем.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()