from fastapi import HTTPException, status
from .repository import AuthRepository
from .schemas import UserCreate, Token
from .utils import hash_password, verify_password, create_access_token
from .models import User
from src.features.sse.connection_manager import sse_manager

class AuthService:
    def __init__(self, repository: AuthRepository):
        self.repository = repository

    async def register_user(self, user_in: UserCreate) -> User:
        user = await self.repository.get_user_by_email(user_in.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        
        # Получаем роль по умолчанию (user)
        role = await self.repository.get_role_by_name("user")
        if not role:
            # Если ролей еще нет в базе, создадим их (для демонстрации)
            role = await self.repository.create_role("user")
            await self.repository.create_role("admin")

        user_data = {
            "email": user_in.email,
            "hashed_password": hash_password(user_in.password)
        }
        
        new_user = await self.repository.create_user(user_data, [role])
        
        # Сповіщення всіх про нового користувача
        await sse_manager.broadcast({
            "type": "new_user",
            "message": f"Новий користувач {new_user.email} приєднався до нас!",
            "user_id": new_user.id
        })
        
        return new_user

    async def authenticate_user(self, email: str, password: str) -> User:
        user = await self.repository.get_user_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    def create_token(self, user: User) -> Token:
        access_token = create_access_token(data={"sub": user.email})
        return Token(access_token=access_token, token_type="bearer")
