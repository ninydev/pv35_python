import json
import random
import time
from http.server import HTTPServer, BaseHTTPRequestHandler


# 1. Наша синхронная функция-симулятор
def mock_recognize_image(file_size_bytes):
    print(f"[LOG] Отримано файл розміром {file_size_bytes} байт. Аналізуємо...")

    # Имитация работы нейросети
    time.sleep(random.uniform(0.5, 1.5))

    # 20% шанс ошибки
    if random.random() < 0.2:
        return {
            "status": "error",
            "message": "Зображення занадто розмите для розпізнавання."
        }

    # Успешный ответ
    return {
        "status": "success",
        "reading": f"{random.randint(10000, 99999)}",
        "confidence": round(random.uniform(0.70, 0.99), 2),
        "message": "Показання успішно розпізнано"
    }


# 2. Класс, который обрабатывает HTTP-запросы
class MeterAPIHandler(BaseHTTPRequestHandler):

    # Метод, который автоматически вызывается при POST-запросе
    def do_POST(self):
        # Проверяем, что запрос пришел на нужный URL
        if self.path == '/api/recognize':

            # Узнаем размер присланных данных (файла) из заголовков
            content_length = int(self.headers.get('Content-Length', 0))

            # Читаем байты файла прямо из потока (из сокета)
            file_bytes = self.rfile.read(content_length)

            # Передаем данные в нашу функцию
            result_dict = mock_recognize_image(len(file_bytes))

            # Формируем успешный HTTP-ответ (Статус 200 OK)
            self.send_response(200)
            # Говорим клиенту, что возвращаем JSON
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()  # Обязательная пустая строка между заголовками и телом

            # Отправляем сам JSON (превратив его обратно в байты)
            response_json = json.dumps(result_dict, ensure_ascii=False)
            self.wfile.write(response_json.encode('utf-8'))

        else:
            # Если URL неправильный, возвращаем 404 Not Found
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Endpoint not found")


# 3. Запуск сервера
def run_server(port=8000):
    server_address = ('', port)
    # Создаем экземпляр сервера, передавая ему наш обработчик
    httpd = HTTPServer(server_address, MeterAPIHandler)
    print(f"Сервер запущено на http://localhost:{port}")
    print("Чекаю на POST запити за адресою /api/recognize ...")
    print("Для зупинки натисніть Ctrl+C")

    # Запускаем бесконечный цикл прослушивания порта
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()