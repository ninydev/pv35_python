from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from .models import Post
from typing import List, Optional, Tuple

class PostRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_post(self, post_data: dict) -> Post:
        new_post = Post(**post_data)
        self.db.add(new_post)
        await self.db.commit()
        await self.db.refresh(new_post)
        return new_post

    async def get_posts(self, skip: int = 0, limit: int = 10) -> Tuple[List[Post], int]:
        # Отримуємо загальну кількість
        total_query = select(func.count(Post.id))
        total_result = await self.db.execute(total_query)
        total = total_result.scalar() or 0

        # Отримуємо самі пости
        query = (
            select(Post)
            .options(selectinload(Post.author), selectinload(Post.likes))
            .order_by(Post.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(query)
        return result.scalars().all(), total

    async def get_post_by_id(self, post_id: int) -> Optional[Post]:
        query = (
            select(Post)
            .where(Post.id == post_id)
            .options(
                selectinload(Post.author),
                selectinload(Post.comments).selectinload(Comment.author),
                selectinload(Post.likes)
            )
        )
        # Нам потрібен Comment тут для selectinload
        from src.features.comments.models import Comment 
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
        
    async def get_user_posts(self, user_id: int, skip: int = 0, limit: int = 10) -> Tuple[List[Post], int]:
        total_query = select(func.count(Post.id)).where(Post.author_id == user_id)
        total_result = await self.db.execute(total_query)
        total = total_result.scalar() or 0

        query = (
            select(Post)
            .where(Post.author_id == user_id)
            .options(
                selectinload(Post.author),
                selectinload(Post.comments).selectinload(Comment.author),
                selectinload(Post.likes)
            )
            .order_by(Post.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        from src.features.comments.models import Comment
        result = await self.db.execute(query)
        return result.scalars().all(), total
