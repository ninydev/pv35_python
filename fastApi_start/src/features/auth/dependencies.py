from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database import get_db
from .repository import AuthRepository
from .service import AuthService
from .utils import decode_access_token
from .models import User
from typing import List

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    repository = AuthRepository(db)
    return AuthService(repository)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
        
    user = await auth_service.repository.get_user_by_email(email)
    if user is None:
        raise credentials_exception
    return user

class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)):
        user_roles = [role.name for role in user.roles]
        for role in self.allowed_roles:
            if role in user_roles:
                return True
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have enough permissions"
        )
