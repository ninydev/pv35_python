from .repository import CommentRepository
from .schemas import CommentCreate
from .models import Comment
from src.features.sse.connection_manager import sse_manager

class CommentService:
    def __init__(self, repository: CommentRepository):
        self.repository = repository

    async def add_comment(self, post_id: int, comment_in: CommentCreate, author_id: int) -> Comment:
        comment_data = comment_in.model_dump()
        comment_data["post_id"] = post_id
        comment_data["author_id"] = author_id
        comment = await self.repository.create_comment(comment_data)
        
        # Відправка SSE сповіщення автору поста
        if comment.post.author_id != author_id: # Не шлемо самі собі
            await sse_manager.send_personal_message(comment.post.author_id, {
                "type": "new_comment",
                "message": f"Користувач {comment.author.email} прокоментував ваш пост",
                "post_id": post_id,
                "comment_id": comment.id
            })
            
        return comment

    async def get_post_comments(self, post_id: int):
        return await self.repository.get_comments_by_post_id(post_id)
