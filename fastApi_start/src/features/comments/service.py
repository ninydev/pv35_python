from .repository import CommentRepository
from .schemas import CommentCreate
from .models import Comment

class CommentService:
    def __init__(self, repository: CommentRepository):
        self.repository = repository

    async def add_comment(self, post_id: int, comment_in: CommentCreate, author_id: int) -> Comment:
        comment_data = comment_in.model_dump()
        comment_data["post_id"] = post_id
        comment_data["author_id"] = author_id
        return await self.repository.create_comment(comment_data)

    async def get_post_comments(self, post_id: int):
        return await self.repository.get_comments_by_post_id(post_id)
