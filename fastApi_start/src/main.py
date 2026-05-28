from fastapi import FastAPI, Depends
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

setup_logging()

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(posts_router)
app.include_router(comments_router)
app.include_router(likes_router)
app.include_router(blog_router)


@app.get("/")
async def root(db: AsyncSession = Depends(get_db)):
    logger.info("Root endpoint called")
    return {"message": "Hello World", "project_name": settings.PROJECT_NAME}


@app.get("/hello/{name}")
async def say_hello(name: str):
    logger.info(f"Hello endpoint called with name: {name}")
    return {"message": f"Hello {name}"}
