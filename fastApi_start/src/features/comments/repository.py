from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from .models import Comment
from typing import List

class CommentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_comment(self, comment_data: dict) -> Comment:
        new_comment = Comment(**comment_data)
        self.db.add(new_comment)
        await self.db.commit()
        await self.db.refresh(new_comment)
        
        # Завантажимо автора та інформацію про пост для сповіщень
        from src.features.posts.models import Post
        query = (
            select(Comment)
            .where(Comment.id == new_comment.id)
            .options(
                selectinload(Comment.author),
                selectinload(Comment.post)
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one()

    async def get_comments_by_post_id(self, post_id: int) -> List[Comment]:
        query = (
            select(Comment)
            .where(Comment.post_id == post_id)
            .options(selectinload(Comment.author))
            .order_by(Comment.created_at.asc())
        )
        result = await self.db.execute(query)
        return result.scalars().all()
