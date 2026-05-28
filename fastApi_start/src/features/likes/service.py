from .repository import LikeRepository
from src.features.sse.connection_manager import sse_manager

class LikeService:
    def __init__(self, repository: LikeRepository):
        self.repository = repository

    async def toggle_like(self, post_id: int, user_id: int) -> bool:
        is_added, author_id = await self.repository.toggle_like(post_id, user_id)
        
        if is_added and author_id and author_id != user_id:
            await sse_manager.send_personal_message(author_id, {
                "type": "new_like",
                "message": f"Користувач (ID: {user_id}) вподобав ваш пост",
                "post_id": post_id
            })
            
        return is_added

    async def get_likes_count(self, post_id: int) -> int:
        return await self.repository.get_likes_count(post_id)
