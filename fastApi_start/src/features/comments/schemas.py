from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.features.posts.schemas import UserShort

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class CommentRead(CommentBase):
    id: int
    post_id: int
    author_id: int
    # Ми імпортуємо UserShort всередині або використовуємо ForwardRef, 
    # щоб уникнути циклічної залежності, якщо UserShort буде в posts.schemas
    author: "UserShort" 
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

from src.features.posts.schemas import UserShort
CommentRead.model_rebuild()
