from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import BACKEND_DIR
from app.storage.models import StoredFile
from app.storage.provider import StorageProvider


class LocalStorageProvider(StorageProvider):
	"""Store uploaded files on local disk under storage/uploads."""

	def __init__(self, uploads_dir: Path | None = None) -> None:
		self._uploads_dir = uploads_dir or (BACKEND_DIR / "storage" / "uploads")

	def store(self, file: UploadFile) -> StoredFile:
		self._uploads_dir.mkdir(parents=True, exist_ok=True)

		original_filename = file.filename or "upload"
		extension = "".join(Path(original_filename).suffixes)
		stored_filename = f"{uuid4()}{extension}"
		destination_path = self._uploads_dir / stored_filename

		file.file.seek(0)
		content = file.file.read()

		with destination_path.open("wb") as output:
			output.write(content)

		return StoredFile(
			original_filename=original_filename,
			stored_filename=stored_filename,
			storage_path=str(destination_path),
			mime_type=file.content_type or "application/octet-stream",
			file_size=len(content),
		)
	
	def delete(self, stored_file: StoredFile) -> None:
		file_path = Path(stored_file.storage_path)
		if file_path.exists():
			file_path.unlink()
