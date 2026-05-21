from UserRepository import UserRepository
from UserCreateRequest import UserCreateRequest
from UserEntity import UserEntity
from UserMapper import UserMapper
from UserResponse import UserResponse


class UserService:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def create_user(self, user_create_request: UserCreateRequest) -> UserResponse:
        """ Creates a new user in the repository."""
        user_entity = self._user_repository.create_user(UserMapper.map_create_to_entity(user_create_request))
        user_response = UserMapper.map_entity_to_response(user_entity)
        return user_response
