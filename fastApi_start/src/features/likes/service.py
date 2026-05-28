from .repository import LikeRepository

class LikeService:
    def __init__(self, repository: LikeRepository):
        self.repository = repository

    async def toggle_like(self, post_id: int, user_id: int) -> bool:
        return await self.repository.toggle_like(post_id, user_id)

    async def get_likes_count(self, post_id: int) -> int:
        return await self.repository.get_likes_count(post_id)
