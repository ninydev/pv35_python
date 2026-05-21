import asyncio
import websockets
import json

HOST = '127.0.0.1'
PORT = 5555

# Список всех подключенных браузеров
connected_clients = set()


async def handle_client(websocket):
    # Регистрируем нового клиента
    connected_clients.add(websocket)
    print(f"[SERVER] Новый клиент подключен. Всего: {len(connected_clients)}")

    try:
        async for message in websocket:
            # Когда пришло сообщение от одного — рассылаем всем
            print(f"[SERVER] Получено: {message}")

            # Создаем задачу на рассылку всем
            if connected_clients:
                # Рассылаем сообщение всем подключенным
                await asyncio.gather(*(client.send(message) for client in connected_clients))

    except websockets.exceptions.ConnectionClosed:
        print("[SERVER] Клиент отключился")
    finally:
        # Убираем клиента из списка при закрытии
        connected_clients.remove(websocket)


async def main():
    async with websockets.serve(handle_client, HOST, PORT):
        print(f"[SERVER] WebSocket сервер запущен на ws://{HOST}:{PORT}")
        await asyncio.Future()  # Работаем вечно


if __name__ == "__main__":
    asyncio.run(main())