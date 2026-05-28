from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.infrastructure.base_model import Base, TimestampMixin

class Like(Base, TimestampMixin):
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Відносини
    post: Mapped["Post"] = relationship("Post", back_populates="likes")
    user: Mapped["User"] = relationship("User", backref="likes")

    __table_args__ = (
        UniqueConstraint("post_id", "user_id", name="uq_post_user_like"),
    )

    def __repr__(self) -> str:
        return f"Like(post_id={self.post_id}, user_id={self.user_id})"

# Імпорти для типізації
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.features.posts.models import Post
    from src.features.auth.models import User
