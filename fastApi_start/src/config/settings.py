"""
Головний модуль конфігурації проекту (src/config/settings.py).

Цей файл відповідає за зчитування та валідацію всіх налаштувань програми.
Використовується бібліотека pydantic-settings. 

Як це працює:
1. Клас Settings описує всі необхідні змінні конфігурації та їх типи.
2. При ініціалізації (`settings = Settings()`) Pydantic автоматично шукає ці змінні:
   - Спочатку в системних змінних оточення (Environment Variables).
   - Потім у файлі `.env`, який лежить у корені проекту (через налаштування env_file=".env").
3. Якщо змінна не знайдена, але має значення за замовчуванням (як PROJECT_NAME), використовується воно.
4. Якщо змінна обов'язкова (не має дефолтного значення, як POSTGRES_USER) і її ніде немає — програма 
   не запуститься і видасть помилку. Це захищає від запуску недоконфігурованого застосунку.

Головний блок програми та інші модулі імпортують об'єкт `settings` звідси, щоб отримати доступ
до налаштувань.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    """
    Схема конфігурації застосунку.
    Успадковується від BaseSettings, що надає магію автоматичного парсингу змінних.
    """
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore" # Ігнорувати зайві змінні у файлі .env, які не описані в цьому класі
    )

    # Загальні налаштування застосунку
    PROJECT_NAME: str = "Social API"
    LOG_LEVEL: str = "INFO"
    SECRET_KEY: str # Секретний ключ для підпису JWT токенів
    ALGORITHM: str = "HS256" # Алгоритм хешування токенів
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Налаштування підключення до бази даних PostgreSQL
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    
    # Повний URL для SQLAlchemy (зазвичай генерується на основі попередніх параметрів або задається окремо)
    DATABASE_URL: str

    # Налаштування файлового сховища (де зберігати і як віддавати картинки/файли)
    UPLOAD_DIR: str = "uploads"
    STATIC_URL: str = "/static"

# Створення єдиного глобального екземпляра налаштувань, який імпортуватиметься по всьому проекту
settings = Settings()
