from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import DocumentType


class InterviewDocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    interview_session_id: int
    document_type: DocumentType
    original_filename: str
    stored_filename: str
    mime_type: str
    file_size: int
    extracted_text: str
    created_at: datetime
    updated_at: datetime


class InterviewDocumentUploadResponse(BaseModel):
    document: InterviewDocumentResponse