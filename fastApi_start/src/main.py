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

setup_logging()

app = FastAPI(title=settings.PROJECT_NAME)

async def get_context(db: AsyncSession = Depends(get_db)):
    return {"db": db}

graphql_app = GraphQLRouter(schema, context_getter=get_context)

# Налаштування статичних файлів
app.mount(settings.STATIC_URL, StaticFiles(directory=settings.UPLOAD_DIR), name="static")

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(posts_router)
app.include_router(comments_router)
app.include_router(likes_router)
app.include_router(blog_router)
app.include_router(sse_router)
app.include_router(ws_router)
app.include_router(graphql_app, prefix="/graphql")