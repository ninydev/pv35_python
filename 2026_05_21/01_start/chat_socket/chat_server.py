import socket
import threading

# Настройки
HOST = '127.0.0.1'
PORT = 5555

# Список всех подключенных клиентов
clients = []


def broadcast(message, sender_client):
    """Рассылка сообщения всем, кроме отправителя"""
    for client in clients:
        if client != sender_client:
            try:
                client.send(message)
            except:
                # Если отправить не удалось (клиент отвалился)
                remove_client(client)


def handle_client(client):
    """Функция для работы с каждым конкретным клиентом в отдельном потоке"""
    while True:
        try:
            # Ждем сообщение от клиента
            message = client.recv(1024)
            if not message:
                break
            broadcast(message, client)
            print(f"[SERVER] Сообщение получено от: {message.decode('utf-8')}")
        except:
            break

    remove_client(client)


def remove_client(client):
    """Удаление клиента из списка при отключении"""
    if client in clients:
        clients.remove(client)
        client.close()
        print(f"[SERVER] Клиент отключен. Всего в чате: {len(clients)}")


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[SERVER] Чат-сервер запущен на {HOST}:{PORT}")

    while True:
        # Принимаем новое соединение
        client, address = server.accept()
        print(f"[SERVER] Новое подключение: {str(address)}")

        # Добавляем в список и запускаем поток обслуживания
        clients.append(client)

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()
        print(f"[SERVER] Активных соединений: {len(clients)}")


if __name__ == "__main__":
    start_server()