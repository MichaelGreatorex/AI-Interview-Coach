from pydantic import BaseModel

from app.schemas.interview_document import InterviewDocumentResponse


class InterviewDocumentProcessingResponse(BaseModel):
    session_id: str
    documents: list[InterviewDocumentResponse]