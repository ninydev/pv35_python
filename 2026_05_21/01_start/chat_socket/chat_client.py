import socket
import threading

# Настройки подключения
HOST = '127.0.0.1'
PORT = 5555

nickname = input("Введите ваш никнейм: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive_messages():
    """Фоновый поток для приема сообщений от сервера"""
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                # '\r' и очистка строки, чтобы ввод не мешался с выводом
                print(f"\n{message}\nВаше сообщение: ", end="")
            else:
                break
        except:
            print("[ERROR] Соединение с сервером потеряно.")
            client.close()
            break

def send_messages():
    """Основной поток для отправки сообщений"""
    while True:
        try:
            text = input("Ваше сообщение: ")
            full_message = f"{nickname}: {text}"
            client.send(full_message.encode('utf-8'))
        except:
            break

# Запускаем поток на чтение
receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True # Поток умрет вместе с основной программой
receive_thread.start()

# Запускаем логику отправки в основном потоке
send_messages()