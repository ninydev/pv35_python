import json
from typing import Dict, List
from fastapi import WebSocket
from loguru import logger

class WebSocketManager:
    def __init__(self):
        # Храним активные соединения: {user_id: [websocket1, websocket2, ...]}
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        """Прийняти з'єднання та зареєструвати його."""
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
        logger.info(f"WS: User {user_id} connected. Total connections for user: {len(self.active_connections[user_id])}")

    def disconnect(self, websocket: WebSocket, user_id: int):
        """Видалити з'єднання."""
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        logger.info(f"WS: User {user_id} disconnected.")

    async def send_personal_message(self, message: dict, user_id: int):
        """Відправити повідомлення конкретному користувачу."""
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                await connection.send_json(message)

    async def broadcast(self, message: dict):
        """Відправити повідомлення всім підключеним користувачам."""
        for user_id, connections in self.active_connections.items():
            for connection in connections:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Error broadcasting to user {user_id}: {e}")

# Глобальний екземпляр менеджера
ws_manager = WebSocketManager()
