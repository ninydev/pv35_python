from pydantic import BaseModel, ConfigDict
from typing import TypeVar, Generic, List, Optional

T = TypeVar("T")

class PaginationParams(BaseModel):
    page: int = 1
    size: int = 10

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size

    @property
    def limit(self) -> int:
        return self.size

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int
    next_page: Optional[int]
    prev_page: Optional[int]

    model_config = ConfigDict(from_attributes=True)
