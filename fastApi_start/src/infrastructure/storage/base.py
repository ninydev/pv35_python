from abc import ABC, abstractmethod
from fastapi import UploadFile

class StorageService(ABC):
    @abstractmethod
    async def upload_file(self, file: UploadFile) -> str:
        """
        Uploads a file and returns its URL or path.
        """
        pass

    @abstractmethod
    async def delete_file(self, file_path: str) -> bool:
        """
        Deletes a file.
        """
        pass
