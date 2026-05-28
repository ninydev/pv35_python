from src.config.settings import settings
from .base import StorageService
from .local import LocalStorageService

def get_storage_service() -> StorageService:
    # Тут ми можемо легко перемикати реалізацію
    return LocalStorageService(
        upload_dir=settings.UPLOAD_DIR,
        base_url=settings.STATIC_URL
    )
