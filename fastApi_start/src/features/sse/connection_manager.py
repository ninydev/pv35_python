import asyncio
import json
from typing import Dict, List, Any
from loguru import logger

class SSEConnectionManager:
    def __init__(self):
        # Храним очереди для каждого пользователя {user_id: [queue1, queue2, ...]}
        self.active_connections: Dict[int, List[asyncio.Queue]] = {}

    async def connect(self, user_id: int) -> asyncio.Queue:
        """Реєстрація нового підключення для користувача."""
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        
        queue = asyncio.Queue()
        self.active_connections[user_id].append(queue)
        logger.info(f"SSE: User {user_id} connected. Active connections for user: {len(self.active_connections[user_id])}")
        return queue

    def disconnect(self, user_id: int, queue: asyncio.Queue):
        """Видалення підключення."""
        if user_id in self.active_connections:
            if queue in self.active_connections[user_id]:
                self.active_connections[user_id].remove(queue)
            
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        logger.info(f"SSE: User {user_id} disconnected.")

    async def send_personal_message(self, user_id: int, message: Any):
        """Відправка повідомлення конкретному користувачу."""
        if user_id in self.active_connections:
            data = json.dumps(message, ensure_ascii=False)
            for queue in self.active_connections[user_id]:
                await queue.put(data)

    async def broadcast(self, message: Any):
        """Відправка повідомлення всім активним користувачам."""
        data = json.dumps(message, ensure_ascii=False)
        for user_id, queues in self.active_connections.items():
            for queue in queues:
                await queue.put(data)

# Створюємо глобальний екземпляр менеджера
sse_manager = SSEConnectionManager()
