from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database import get_db
from src.features.auth.dependencies import get_current_user
from src.features.auth.models import User
from .repository import LikeRepository
from .service import LikeService
from src.features.posts.repository import PostRepository

router = APIRouter(prefix="/likes", tags=["Social - Likes"])

async def get_like_service(db: AsyncSession = Depends(get_db)) -> LikeService:
    repository = LikeRepository(db)
    return LikeService(repository)

@router.post("/{post_id}")
async def toggle_like(
    post_id: int,
    current_user: User = Depends(get_current_user),
    service: LikeService = Depends(get_like_service),
    db: AsyncSession = Depends(get_db)
):
    # Перевіримо чи існує пост
    post_repo = PostRepository(db)
    post = await post_repo.get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        
    is_liked = await service.toggle_like(post_id, current_user.id)
    return {"is_liked": is_liked}
