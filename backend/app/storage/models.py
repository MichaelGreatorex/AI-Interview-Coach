from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class StoredFile:
    original_filename: str
    stored_filename: str
    storage_path: str
    mime_type: str
    file_size: int