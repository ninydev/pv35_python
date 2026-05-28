from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from .models import Like

class LikeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def toggle_like(self, post_id: int, user_id: int) -> bool:
        """Повертає True, якщо лайк додано, False якщо видалено."""
        query = select(Like).where(and_(Like.post_id == post_id, Like.user_id == user_id))
        result = await self.db.execute(query)
        existing_like = result.scalar_one_or_none()

        if existing_like:
            await self.db.delete(existing_like)
            await self.db.commit()
            return False
        else:
            new_like = Like(post_id=post_id, user_id=user_id)
            self.db.add(new_like)
            await self.db.commit()
            return True

    async def get_likes_count(self, post_id: int) -> int:
        query = select(func.count(Like.id)).where(Like.post_id == post_id)
        result = await self.db.execute(query)
        return result.scalar() or 0

    async def is_liked_by_user(self, post_id: int, user_id: int) -> bool:
        query = select(Like).where(and_(Like.post_id == post_id, Like.user_id == user_id))
        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None
