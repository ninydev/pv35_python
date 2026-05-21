from UserController import UserController
from UserService import UserService
from UserRepository import UserRepository
from UserCreateRequest import UserCreateRequest



request = UserCreateRequest(email="test@example.com", password="password")

controller = UserController(UserService(UserRepository()))
response = controller.create_user(request)

print(f"User created: {response}")
