"""
Модуль маршрутизатора (контролера) для роботи з постами (публікаціями).

У архітектурі FastAPI цей роутер виконує роль контролера (Controller) з патерну MVC.
Головний блок програми (FastAPI app у main.py) очікує від цього файлу набір
зареєстрованих кінцевих точок (endpoints), які відповідають за певну частину предметної області (фічу).

Обов'язки цього роутера:
1. Визначення HTTP-маршрутів (GET, POST тощо) для роботи з постами.
2. Валідація вхідних даних (через параметри функцій та Pydantic схеми).
3. Перевірка авторизації (через FastAPI Depends та get_current_user).
4. Виклик бізнес-логіки (PostService) для обробки запиту.
5. Формування HTTP-відповідей або викидання помилок (HTTPException), якщо щось пішло не так.

Роутер не містить прямої логіки роботи з базою даних, він лише делегує це Сервісу, залишаючись "тонким клієнтом" для бізнес-логіки.
"""

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database import get_db
from src.features.auth.dependencies import get_current_user, get_optional_current_user
from src.features.auth.models import User
from .schemas import PostCreate, PostRead, PostDetailRead
from .repository import PostRepository
from .service import PostService
from src.infrastructure.storage.base import StorageService
from src.infrastructure.storage.dependencies import get_storage_service
from src.infrastructure.schemas import PaginationParams, PaginatedResponse
from typing import Optional

router = APIRouter(prefix="/posts", tags=["Social - Posts"])

async def get_post_service(
    db: AsyncSession = Depends(get_db),
    storage: StorageService = Depends(get_storage_service)
) -> PostService:
    """
    Фабрика-залежність (Dependency) для створення екземпляра PostService.
    
    Завіщо створено: FastAPI використовує систему впровадження залежностей (Dependency Injection).
    Цей метод дозволяє автоматично конструювати сервіс для кожного запиту, автоматично
    отримуючи сесію бази даних та сервіс збереження файлів, і передаючи їх у репозиторій та сервіс.
    Таким чином, роутерам не потрібно самим знати, як створювати ці об'єкти.
    """
    repository = PostRepository(db)
    return PostService(repository, storage)

@router.post("/", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create_post(
    content: str = Form(..., description="Текст публікації"),
    image: Optional[UploadFile] = File(None, description="Опціональне зображення для посту"),
    current_user: User = Depends(get_current_user),
    service: PostService = Depends(get_post_service)
):
    """
    Створення нового посту.
    
    Завіщо створено: Обробляє POST-запити для створення публікацій.
    Приймає дані як Form та File, оскільки запит містить файли (multipart/form-data), 
    а не звичайний JSON. 
    Вимагає обов'язкової авторизації (через get_current_user) і передає виклик у сервіс.
    """
    return await service.create_post(content, current_user.id, image)

@router.get("/", response_model=PaginatedResponse[PostRead])
async def get_posts(
    params: PaginationParams = Depends(),
    current_user: Optional[User] = Depends(get_optional_current_user),
    service: PostService = Depends(get_post_service)
):
    """
    Отримання списку постів з підтримкою пагінації.
    
    Завіщо створено: Обробляє GET-запити для відображення стрічки постів.
    Авторизація встановлена як опціональна (get_optional_current_user), щоб неавторизовані 
    користувачі також могли бачити стрічку постів, але авторизовані могли отримати 
    додаткові дані (наприклад, чи поставили вони лайк на цьому пості).
    """
    return await service.get_posts_paginated(params, current_user.id if current_user else None)

@router.get("/{post_id}", response_model=PostDetailRead)
async def get_post(
    post_id: int,
    current_user: Optional[User] = Depends(get_optional_current_user),
    service: PostService = Depends(get_post_service)
):
    """
    Отримання детальної інформації про конкретний пост за його ідентифікатором.
    
    Завіщо створено: Дозволяє відкрити пост окремо.
    Метод викликає сервіс для отримання даних. Якщо пост не знайдено (сервіс повернув None), 
    саме роутер бере на себе відповідальність перервати виконання і повернути 
    стандартну 404 помилку (HTTPException).
    """
    post = await service.get_post_detail(post_id, current_user.id if current_user else None)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post
