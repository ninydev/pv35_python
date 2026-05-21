from dataclasses import dataclass
from typing import Optional, Dict, Callable


# ==========================================
# 1. МОДЕЛИ И DTO (Данные)
# ==========================================

@dataclass
class UserEntity:
    """Сущность (Model): То, как данные хранятся в БД."""
    id: int
    username: str
    password_hash: str  # В БД мы храним хэш
    role: str


@dataclass
class RequestDTO:
    """Входящий запрос: Очищенный и типизированный объект от клиента."""
    method: str
    path: str
    headers: Dict[str, str]
    body: dict


@dataclass
class ResponseDTO:
    """Ответ клиенту: Строгий формат, который уйдет в браузер."""
    status_code: int
    body: dict


# ==========================================
# 2. РЕПОЗИТОРИЙ (Слой работы с БД)
# ==========================================

class UserRepository:
    """Кладовщик: Только он знает, как сохранять и искать данные."""

    def __init__(self):
        self._db = []  # Эмулируем базу данных списком
        self._next_id = 1

    def save(self, user: UserEntity) -> UserEntity:
        user.id = self._next_id
        self._db.append(user)
        self._next_id += 1
        return user

    def find_by_username(self, username: str) -> Optional[UserEntity]:
        for user in self._db:
            if user.username == username:
                return user
        return None


# ==========================================
# 3. СЕРВИС (Слой бизнес-логики)
# ==========================================

class UserService:
    """Мозг: Принимает решения, проверяет правила, но не знает про HTTP."""

    def __init__(self, repository: UserRepository):
        self.repo = repository  # Внедрение зависимости (DI)

    def register_user(self, data: dict) -> UserEntity:
        # Бизнес-правило 1: Проверка на дубликаты
        if self.repo.find_by_username(data['username']):
            raise ValueError(f"Пользователь {data['username']} уже существует!")

        # Бизнес-правило 2: Хэширование пароля (эмуляция)
        hashed_password = f"***{data['password']}***"

        # Создаем сущность
        new_user = UserEntity(
            id=0,
            username=data['username'],
            password_hash=hashed_password,
            role="client"
        )
        # Отдаем кладовщику на сохранение
        return self.repo.save(new_user)


# ==========================================
# 4. КОНТРОЛЛЕР (Слой HTTP)
# ==========================================

class UserController:
    """Менеджер: Принимает DTO, дергает сервис, отдает ResponseDTO."""

    def __init__(self, service: UserService):
        self.service = service  # Внедрение зависимости (DI)

    def create(self, request: RequestDTO) -> ResponseDTO:
        try:
            # 1. Передаем данные в Сервис
            user = self.service.register_user(request.body)

            # 2. Упаковываем ответ (ЦЕНЗУРА: убираем пароль перед отправкой!)
            safe_data = {
                "id": user.id,
                "username": user.username,
                "role": user.role
            }
            return ResponseDTO(201, {"status": "success", "data": safe_data})

        except ValueError as e:
            # Если бизнес-логика ругнулась, отдаем ошибку 400
            return ResponseDTO(400, {"status": "error", "message": str(e)})


# ==========================================
# 5. РОУТЕР (Стрелочник)
# ==========================================

class Router:
    """Маршрутизатор: Решает, какой контроллер будет обрабатывать путь."""

    def __init__(self):
        self.routes = {}

    def register(self, method: str, path: str, handler: Callable):
        self.routes[f"{method} {path}"] = handler

    def handle(self, request: RequestDTO) -> ResponseDTO:
        route_key = f"{request.method} {request.path}"
        handler = self.routes.get(route_key)

        if not handler:
            return ResponseDTO(404, {"error": "Маршрут не найден (404)"})

        return handler(request)  # Вызываем нужный метод контроллера


# ==========================================
# 6. MIDDLEWARE (Таможня)
# ==========================================

class AuthMiddleware:
    """Таможня: Проверяет "Кто это?" ДО того, как пустить к контроллерам."""

    def __init__(self, next_handler: Callable):
        self.next_handler = next_handler  # Кто будет работать после нас (Router)

    def process(self, request: RequestDTO) -> ResponseDTO:
        print(f"👮 [Middleware] Проверяем запрос: {request.method} {request.path}")

        # Проверяем заголовки на наличие правильного токена
        token = request.headers.get("Authorization")
        if token != "Bearer SecretAdminToken":
            print("👮 [Middleware] ❌ Отказ! У вас нет пропуска.")
            return ResponseDTO(403, {"error": "Доступ запрещен (403)"})

        print("👮 [Middleware] ✅ Пропуск валиден. Проходите.")
        # Передаем запрос дальше по цепочке
        return self.next_handler(request)


# ==========================================
# 🚀 ЗАПУСК ПРИЛОЖЕНИЯ (Сборка конструктора)
# ==========================================

if __name__ == "__main__":
    print("--- ⚙️ Инициализация сервера (DI Container) ---")
    # Собираем наше приложение из "кубиков", прокидывая зависимости
    repo = UserRepository()
    service = UserService(repository=repo)
    controller = UserController(service=service)

    router = Router()
    router.register("POST", "/api/users", controller.create)

    # Middleware оборачивает Роутер
    app = AuthMiddleware(next_handler=router.handle)

    print("--- 🌍 Сервер готов принимать запросы ---\n")

    # --- ТЕСТ 1: Запрос без правильного токена (Отфутболит Middleware) ---
    print("\n👉 ТЕСТ 1: Хакер пытается создать юзера")
    bad_request = RequestDTO(
        method="POST", path="/api/users",
        headers={"Authorization": "Bearer FakeToken123"},
        body={"username": "hacker", "password": "123"}
    )
    response1 = app.process(bad_request)
    print(f"Ответ сервера: {response1.status_code} | {response1.body}")

    # --- ТЕСТ 2: Правильный запрос (Пройдет весь путь) ---
    print("\n👉 ТЕСТ 2: Админ создает нового юзера")
    good_request = RequestDTO(
        method="POST", path="/api/users",
        headers={"Authorization": "Bearer SecretAdminToken"},
        body={"username": "ivan_student", "password": "secure_password_99"}
    )
    response2 = app.process(good_request)
    print(f"Ответ сервера: {response2.status_code} | {response2.body}")

    # --- ТЕСТ 3: Ошибка бизнес-логики (Отфутболит Сервис) ---
    print("\n👉 ТЕСТ 3: Создание дубликата")
    duplicate_request = RequestDTO(
        method="POST", path="/api/users",
        headers={"Authorization": "Bearer SecretAdminToken"},
        body={"username": "ivan_student", "password": "new_password"}
    )
    response3 = app.process(duplicate_request)
    print(f"Ответ сервера: {response3.status_code} | {response3.body}")