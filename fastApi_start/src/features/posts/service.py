from .repository import PostRepository
from .schemas import PostCreate, PostRead, PostDetailRead
from .models import Post
from src.infrastructure.schemas import PaginationParams, PaginatedResponse
from src.infrastructure.storage.base import StorageService
from fastapi import UploadFile
from typing import List, Optional, Any, Dict

class PostService:
    def __init__(self, repository: PostRepository, storage: Optional[StorageService] = None):
        self.repository = repository
        self.storage = storage

    async def create_post(
        self, 
        content: str, 
        author_id: int, 
        image: Optional[UploadFile] = None
    ) -> Post:
        image_url = None
        if image and self.storage:
            image_url = await self.storage.upload_file(image)

        post_data = {
            "content": content,
            "author_id": author_id,
            "image_url": image_url
        }
        return await self.repository.create_post(post_data)

    async def get_posts_paginated(
        self, 
        params: PaginationParams, 
        current_user_id: Optional[int] = None
    ) -> PaginatedResponse[Dict]:
        posts, total = await self.repository.get_posts(params.offset, params.limit)
        
        items = []
        for post in posts:
            post_dict = self._post_to_dict(post)
            post_dict["likes_count"] = len(post.likes)
            items.append(post_dict)
            
        pages = (total + params.size - 1) // params.size
        
        return PaginatedResponse(
            items=items,
            total=total,
            page=params.page,
            size=params.size,
            pages=pages,
            next_page=params.page + 1 if params.page < pages else None,
            prev_page=params.page - 1 if params.page > 1 else None
        )

    async def get_post_detail(self, post_id: int, current_user_id: Optional[int] = None) -> Optional[Dict]:
        post = await self.repository.get_post_by_id(post_id)
        if not post:
            return None
        
        post_dict = self._post_to_dict(post)
        post_dict["likes_count"] = len(post.likes)
        post_dict["comments"] = post.comments
        
        if current_user_id:
            post_dict["is_liked"] = any(like.user_id == current_user_id for like in post.likes)
        else:
            post_dict["is_liked"] = False
            
        return post_dict

    async def get_user_posts_paginated(
        self, 
        user_id: int,
        params: PaginationParams
    ) -> PaginatedResponse[Dict]:
        posts, total = await self.repository.get_user_posts(user_id, params.offset, params.limit)
        
        items = []
        for post in posts:
            post_dict = self._post_to_dict(post)
            post_dict["likes_count"] = len(post.likes)
            post_dict["comments"] = post.comments
            post_dict["is_liked"] = False
            items.append(post_dict)
            
        pages = (total + params.size - 1) // params.size
        
        return PaginatedResponse(
            items=items,
            total=total,
            page=params.page,
            size=params.size,
            pages=pages,
            next_page=params.page + 1 if params.page < pages else None,
            prev_page=params.page - 1 if params.page > 1 else None
        )

    def _post_to_dict(self, post: Post) -> Dict:
        return {
            "id": post.id,
            "content": post.content,
            "image_url": post.image_url,
            "author_id": post.author_id,
            "author": post.author,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
        }
