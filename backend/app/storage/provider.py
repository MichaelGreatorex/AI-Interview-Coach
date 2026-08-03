from abc import ABC, abstractmethod

from fastapi import UploadFile

from app.storage.models import StoredFile


class StorageProvider(ABC):

    @abstractmethod
    def store(
        self,
        file: UploadFile,
    ) -> StoredFile:
        """Persist a file and return its metadata."""
        raise NotImplementedError