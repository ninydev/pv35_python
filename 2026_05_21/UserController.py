from UserService import UserService
from UserCreateRequest import UserCreateRequest
from UserResponse import UserResponse




class UserController:
    def __init__(self, user_service: UserService):
        self._user_service = user_service

    def create_user(self, user_create_request: UserCreateRequest) -> UserResponse:
        return self._user_service.create_user(user_create_request)
