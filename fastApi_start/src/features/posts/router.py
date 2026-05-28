from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database import get_db
from src.features.auth.dependencies import get_current_user, get_optional_current_user
from src.features.auth.models import User
from .schemas import PostCreate, PostRead, PostDetailRead
from .repository import PostRepository
from .service import PostService
from src.infrastructure.storage.base import StorageService
from src.infrastructure.storage.dependencies import get_storage_service
from src.infrastructure.schemas import PaginationParams, PaginatedResponse
from typing import Optional

router = APIRouter(prefix="/posts", tags=["Social - Posts"])

async def get_post_service(
    db: AsyncSession = Depends(get_db),
    storage: StorageService = Depends(get_storage_service)
) -> PostService:
    repository = PostRepository(db)
    return PostService(repository, storage)

@router.post("/", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create_post(
    content: str = Form(...),
    image: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    service: PostService = Depends(get_post_service)
):
    return await service.create_post(content, current_user.id, image)

@router.get("/", response_model=PaginatedResponse[PostRead])
async def get_posts(
    params: PaginationParams = Depends(),
    current_user: Optional[User] = Depends(get_optional_current_user),
    service: PostService = Depends(get_post_service)
):
    return await service.get_posts_paginated(params, current_user.id if current_user else None)

@router.get("/{post_id}", response_model=PostDetailRead)
async def get_post(
    post_id: int,
    current_user: Optional[User] = Depends(get_optional_current_user),
    service: PostService = Depends(get_post_service)
):
    post = await service.get_post_detail(post_id, current_user.id if current_user else None)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post
