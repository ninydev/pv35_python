from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from .connection_manager import ws_manager
from loguru import logger

router = APIRouter(tags=["WebSocket - Chat"])

@router.websocket("/ws/chat/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    """
    Ендпоінт для WebSocket чату.
    Клієнт підключається за ID користувача.
    """
    await ws_manager.connect(websocket, user_id)
    
    # Повідомляємо всіх про приєднання нового користувача
    await ws_manager.broadcast({
        "sender": "System",
        "message": f"Користувач {user_id} приєднався до чату",
        "type": "system"
    })
    
    try:
        while True:
            # Очікуємо повідомлення від клієнта
            data = await websocket.receive_text()
            
            # Розсилаємо отримане повідомлення всім учасникам
            await ws_manager.broadcast({
                "sender": f"User {user_id}",
                "message": data,
                "type": "user_message"
            })
            
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, user_id)
        # Повідомляємо всіх про вихід користувача
        await ws_manager.broadcast({
            "sender": "System",
            "message": f"Користувач {user_id} покинув чат",
            "type": "system"
        })
    except Exception as e:
        logger.error(f"WebSocket error for user {user_id}: {e}")
        ws_manager.disconnect(websocket, user_id)
