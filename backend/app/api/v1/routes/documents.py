from fastapi import APIRouter, File, Form, UploadFile, status

from app.api.dependencies import DocumentServiceDependency
from app.models.enums import DocumentType
from app.schemas.interview_document import (
    InterviewDocumentResponse,
    InterviewDocumentUploadResponse,
)

router = APIRouter(
    prefix="/sessions/{interview_session_id}/documents",
    tags=["Documents"],
)


@router.post(
    "",
    response_model=InterviewDocumentUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_document(
    interview_session_id: str,
    service: DocumentServiceDependency,
    document_type: DocumentType = Form(...),
    file: UploadFile = File(...),
):
    document = service.upload_document(
        interview_session_id=interview_session_id,
        document_type=document_type,
        file=file,
    )

    return InterviewDocumentUploadResponse(
        document=InterviewDocumentResponse.model_validate(document)
    )