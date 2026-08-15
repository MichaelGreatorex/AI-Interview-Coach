from abc import ABC, abstractmethod
from pathlib import Path


class DocumentTextExtractor(ABC):

    @abstractmethod
    def extract(
        self,
        file_path: Path,
    ) -> str:
        """Extract readable text from a document."""
        raise NotImplementedError