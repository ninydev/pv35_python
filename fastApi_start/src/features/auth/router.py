from fastapi import APIRouter, Depends, status
from .schemas import UserCreate, UserRead, Token, UserLogin
from .service import AuthService
from .dependencies import get_auth_service, get_current_user, RoleChecker
from .models import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
):
    return await auth_service.register_user(user_in)

@router.post("/login", response_model=Token)
async def login(
    login_data: UserLogin,
    auth_service: AuthService = Depends(get_auth_service)
):
    user = await auth_service.authenticate_user(login_data.email, login_data.password)
    return auth_service.create_token(user)

@router.get("/me", response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

# Пример эндпоинта только для админа
@router.get("/admin-only", dependencies=[Depends(RoleChecker(["admin"]))])
async def admin_only():
    return {"message": "Hello Admin"}
