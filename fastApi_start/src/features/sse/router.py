import asyncio
from fastapi import APIRouter, Request
from sse_starlette.sse import EventSourceResponse
from .connection_manager import sse_manager
from loguru import logger

router = APIRouter(prefix="/sse", tags=["SSE - Notifications"])

@router.get("/subscribe/{user_id}")
async def subscribe(request: Request, user_id: int):
    """
    Підписка на події для конкретного користувача за його ID.
    У реальному проекті тут мала б бути перевірка токена.
    """
    async def event_generator():
        queue = await sse_manager.connect(user_id)
        try:
            while True:
                # Перевірка на відключення клієнта
                if await request.is_disconnected():
                    sse_manager.disconnect(user_id, queue)
                    break

                try:
                    # Очікуємо повідомлення з черги
                    # Використовуємо wait_for, щоб регулярно перевіряти is_disconnected
                    data = await asyncio.wait_for(queue.get(), timeout=20.0)
                    yield {
                        "event": "message",
                        "data": data
                    }
                except asyncio.TimeoutError:
                    # Надсилаємо ping для підтримки з'єднання
                    yield {
                        "event": "ping",
                        "data": "keep-alive"
                    }
        except Exception as e:
            logger.error(f"SSE error for user {user_id}: {e}")
            sse_manager.disconnect(user_id, queue)

    return EventSourceResponse(event_generator())
