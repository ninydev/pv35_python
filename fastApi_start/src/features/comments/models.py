from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.infrastructure.base_model import Base, TimestampMixin

class Comment(Base, TimestampMixin):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # Відносини
    post: Mapped["Post"] = relationship("Post", back_populates="comments")
    author: Mapped["User"] = relationship("User", backref="comments")

    def __repr__(self) -> str:
        return f"Comment(id={self.id}, post_id={self.post_id}, author_id={self.author_id})"

# Імпорти для типізації
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.features.posts.models import Post
    from src.features.auth.models import User
