from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.api.dependencies import InterviewWorkflowServiceDependency
from app.schemas.interview import InterviewStartResponse
from app.schemas.interview_document import InterviewDocumentResponse
from app.schemas.interview_document_processing import (
    InterviewDocumentProcessingResponse,
)
from app.schemas.interview_question import InterviewQuestionResponse


router = APIRouter(
    prefix="/interviews",
    tags=["Interviews"],
)


@router.post(
    "",
    response_model=InterviewDocumentProcessingResponse,
    status_code=status.HTTP_201_CREATED,
)
def process_documents(
    workflow_service: InterviewWorkflowServiceDependency,
    cv: UploadFile = File(...),
    job_description: UploadFile = File(...),
) -> InterviewDocumentProcessingResponse:
    result = workflow_service.process_documents(
        cv_file=cv,
        job_description_file=job_description,
    )

    return InterviewDocumentProcessingResponse(
        session_id=result.session.interview_session_id,
        documents=[
            InterviewDocumentResponse.model_validate(document)
            for document in result.documents
        ],
    )


@router.post(
    "/{interview_session_id}/start",
    response_model=InterviewStartResponse,
)
def start_interview(
    interview_session_id: str,
    workflow_service: InterviewWorkflowServiceDependency,
) -> InterviewStartResponse:
    result = workflow_service.start_interview(
        interview_session_id,
    )

    return InterviewStartResponse(
        session_id=result.session.interview_session_id,
        question=InterviewQuestionResponse(
            id=result.question.id,
            text=result.question.text,
        ),
    )