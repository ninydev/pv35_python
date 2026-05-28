from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.infrastructure.base_model import Base, TimestampMixin
from typing import List, Optional

class Post(Base, TimestampMixin):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)

    # Відносини
    author: Mapped["User"] = relationship("User", backref="posts")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    likes: Mapped[List["Like"]] = relationship("Like", back_populates="post", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Post(id={self.id}, author_id={self.author_id})"

# Для коректної роботи relationship нам потрібно імпортувати інші моделі
# Використовуємо TYPE_CHECKING або імпортуємо в кінці файлу для SQLAlchemy
from src.features.auth.models import User
from src.features.comments.models import Comment
from src.features.likes.models import Like
