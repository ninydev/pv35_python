import hashlib

from UserEntity import UserEntity
from UserCreateRequest import UserCreateRequest
from UserResponse import UserResponse


class UserMapper:


    @staticmethod
    def map_create_to_entity(user_create_request: UserCreateRequest) -> UserEntity:
        """ Maps a UserCreateRequest to a UserEntity."""
        # 1. Генерируем хэш пароля (эмуляция шифрования)
        password_bytes = user_create_request.password.encode('utf-8')
        hashed_password = hashlib.sha256(password_bytes).hexdigest()

        # 2. ПРАВИЛЬНО: Передаем все параметры прямо внутрь скобок!
        return UserEntity(
            id=0,  # Заглушка, настоящий ID выдаст Репозиторий
            email=user_create_request.email,
            password_hash=hashed_password,
            is_active=True,
            role="client"
        )



    @staticmethod
    def map_entity_to_response(user_entity: UserEntity) -> UserResponse:
        """ Maps a UserEntity to a UserResponse."""
        return UserResponse(
            email=user_entity.email,
            role=user_entity.role
        )

