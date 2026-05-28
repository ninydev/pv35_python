import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from fastapi import UploadFile
from .base import StorageService

class LocalStorageService(StorageService):
    def __init__(self, upload_dir: str, base_url: str = "/static"):
        self.upload_dir = Path(upload_dir)
        self.base_url = base_url
        # Переконаємося, що головна папка існує
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def upload_file(self, file: UploadFile) -> str:
        # Створюємо шлях: рік/місяць
        now = datetime.now()
        relative_path = Path(str(now.year)) / f"{now.month:02d}"
        full_upload_path = self.upload_dir / relative_path
        full_upload_path.mkdir(parents=True, exist_ok=True)

        # Генеруємо унікальне ім'я файлу
        file_extension = Path(file.filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        
        file_path = full_upload_path / unique_filename
        
        # Зберігаємо файл
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Повертаємо URL для доступу
        # Формат: /static/2026/05/uuid.png
        url_path = f"{self.base_url}/{now.year}/{now.month:02d}/{unique_filename}"
        return url_path

    async def delete_file(self, file_url: str) -> bool:
        # Перетворюємо URL назад у шлях до файлу
        if not file_url.startswith(self.base_url):
            return False
            
        relative_part = file_url[len(self.base_url):].lstrip("/")
        file_path = self.upload_dir / relative_part
        
        if file_path.exists():
            os.remove(file_path)
            return True
        return False
