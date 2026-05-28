from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import User, Role
from typing import Optional, List

class AuthRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str) -> Optional[User]:
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create_user(self, user_data: dict, roles: List[Role]) -> User:
        new_user = User(**user_data)
        new_user.roles = roles
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user

    async def get_role_by_name(self, name: str) -> Optional[Role]:
        query = select(Role).where(Role.name == name)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
        
    async def create_role(self, name: str) -> Role:
        role = Role(name=name)
        self.db.add(role)
        await self.db.commit()
        await self.db.refresh(role)
        return role
