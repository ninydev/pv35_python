import os
from aiohttp import web

# Список активных соединений
clients = set()

async def index(request):
    """Отдает файл index.html"""
    return web.FileResponse('./chat_client.html')

async def websocket_handler(request):
    """Обрабатывает WebSocket соединения"""
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    clients.add(ws)
    print(f"Новое подключение. Всего: {len(clients)}")

    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                # Рассылаем сообщение всем
                for client in clients:
                    await client.send_str(msg.data)
    finally:
        clients.remove(ws)
        print(f"Клиент ушел. Всего: {len(clients)}")

    return ws

app = web.Application()
app.add_routes([
    web.get('/', index),                # Главная страница
    web.get('/ws', websocket_handler),  # Путь для сокетов
])

if __name__ == '__main__':
    # Порт берем из переменной окружения (важно для облаков) или 8080 по дефолту
    port = int(os.environ.get("PORT", 5555))
    web.run_app(app, port=port)