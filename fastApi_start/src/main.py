from fastapi import FastAPI, Depends
from src.config.logging import setup_logging
from src.config.settings import settings
from src.infrastructure.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
from src.features.health.router import router as health_router

setup_logging()

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(health_router)


@app.get("/")
async def root(db: AsyncSession = Depends(get_db)):
    logger.info("Root endpoint called")
    return {"message": "Hello World", "project_name": settings.PROJECT_NAME}


@app.get("/hello/{name}")
async def say_hello(name: str):
    logger.info(f"Hello endpoint called with name: {name}")
    return {"message": f"Hello {name}"}
