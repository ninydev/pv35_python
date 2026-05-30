"""
Головний файл конфігурації та точка входу для FastAPI застосунку (src/main.py).

Цей файл виконує роль "клею" для всього проекту. Його основні завдання:
1. Ініціалізація головного об'єкта `app = FastAPI(...)`.
2. Налаштування глобальних підсистем (наприклад, системи логування).
3. Підключення всіх модулів (фіч) через підключення їхніх роутерів (`app.include_router`).
4. Налаштування додаткових точок входу, таких як GraphQL.
5. Монтування статичних файлів (щоб користувачі могли завантажувати картинки).

При запуску сервера (наприклад, через uvicorn) сервер шукає саме об'єкт `app` у цьому файлі.
"""

from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from src.config.logging import setup_logging
from src.config.settings import settings
from src.infrastructure.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
from src.features.health.router import router as health_router
from src.features.auth.router import router as auth_router
from src.features.posts.router import router as posts_router
from src.features.comments.router import router as comments_router
from src.features.likes.router import router as likes_router
from src.features.blog.router import router as blog_router
from src.features.sse.router import router as sse_router
from src.features.websocket.router import router as ws_router
from strawberry.fastapi import GraphQLRouter
from src.features.graphql_api.schema import schema

# Ініціалізація глобального логування на самому старті програми
setup_logging()

# Створення основного екземпляра FastAPI
app = FastAPI(title=settings.PROJECT_NAME)

async def get_context(db: AsyncSession = Depends(get_db)):
    """
    Функція для створення контексту виконання GraphQL запитів.
    Забезпечує передачу сесії бази даних в резолвери GraphQL.
    """
    return {"db": db}

# Налаштування GraphQL точки входу
graphql_app = GraphQLRouter(schema, context_getter=get_context)

# Налаштування роздачі статичних файлів (завантажених користувачами картинок тощо)
# Усі запити, що починаються на settings.STATIC_URL (напр. /static), будуть шукати файли в settings.UPLOAD_DIR
app.mount(settings.STATIC_URL, StaticFiles(directory=settings.UPLOAD_DIR), name="static")

# Реєстрація роутерів з різних частин (фіч) нашого моноліту
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(posts_router)
app.include_router(comments_router)
app.include_router(likes_router)
app.include_router(blog_router)
app.include_router(sse_router)
app.include_router(ws_router)

# Підключення GraphQL під окремим префіксом
app.include_router(graphql_app, prefix="/graphql")
