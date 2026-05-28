from sqlalchemy import String, ForeignKey, Table, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.infrastructure.base_model import Base, TimestampMixin
from typing import List

# Таблица связи для Many-to-Many
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
)

class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    users: Mapped[List["User"]] = relationship(
        secondary=user_roles, back_populates="roles"
    )

    def __repr__(self) -> str:
        return f"Role(name={self.name})"

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    roles: Mapped[List["Role"]] = relationship(
        secondary=user_roles, back_populates="users", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"User(email={self.email})"
