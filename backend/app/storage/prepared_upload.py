from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class PreparedUpload:
    filename: str
    content_type: str | None
    content: bytes

    @property
    def file_size(self) -> int:
        return len(self.content)