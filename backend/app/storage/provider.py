from abc import ABC, abstractmethod

from app.storage.models import StoredFile
from app.storage.prepared_upload import PreparedUpload


class StorageProvider(ABC):

    @abstractmethod
    def store(
        self,
        upload: PreparedUpload,
    ) -> StoredFile:
        """Persist a prepared upload and return its metadata."""
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        stored_file: StoredFile,
    ) -> None:
        """Delete a file from storage."""
        raise NotImplementedError