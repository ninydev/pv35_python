from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database import get_db
from src.features.posts.repository import PostRepository
from src.features.posts.service import PostService
from src.features.posts.schemas import PostDetailRead
from src.infrastructure.schemas import PaginationParams, PaginatedResponse

router = APIRouter(prefix="/blog", tags=["Blog - Aggregation"])

async def get_post_service(db: AsyncSession = Depends(get_db)) -> PostService:
    repository = PostRepository(db)
    return PostService(repository)

@router.get("/user/{user_id}", response_model=PaginatedResponse[PostDetailRead])
async def get_user_blog(
    user_id: int,
    params: PaginationParams = Depends(),
    service: PostService = Depends(get_post_service)
):
    """
    Отримати всі пости конкретного користувача разом з коментарями та лайками.
    Агрегований маршрут для персональної сторінки/блогу з пагінацією.
    """
    return await service.get_user_posts_paginated(user_id, params)
