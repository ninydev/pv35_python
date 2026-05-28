from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database import get_db
from src.features.auth.dependencies import get_current_user
from src.features.auth.models import User
from .schemas import CommentCreate, CommentRead
from .repository import CommentRepository
from .service import CommentService
from src.features.posts.repository import PostRepository

router = APIRouter(prefix="/comments", tags=["Social - Comments"])

async def get_comment_service(db: AsyncSession = Depends(get_db)) -> CommentService:
    repository = CommentRepository(db)
    return CommentService(repository)

@router.post("/{post_id}", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
async def add_comment(
    post_id: int,
    comment_in: CommentCreate,
    current_user: User = Depends(get_current_user),
    service: CommentService = Depends(get_comment_service),
    db: AsyncSession = Depends(get_db)
):
    # Перевіримо чи існує пост
    post_repo = PostRepository(db)
    post = await post_repo.get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        
    return await service.add_comment(post_id, comment_in, current_user.id)
