from enum import Enum

from pydantic import BaseModel


class AiDocumentType(str, Enum):
    CV = "cv"
    JOB_DESCRIPTION = "job_description"
    UNKNOWN = "unknown"


class AiDocumentUnderstandingResult(BaseModel):
    document_type: AiDocumentType
    extracted_text: str