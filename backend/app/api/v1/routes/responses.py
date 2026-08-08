from fastapi import APIRouter, HTTPException, status

from app.api.dependencies import (
    InterviewSessionServiceDependency,
    InterviewResponseServiceDependency,
)

from app.schemas.interview_response import InterviewResponseSchema
from app.schemas.submit_interview_response_request import (
    SubmitInterviewResponseRequest,
)


router = APIRouter(
    prefix="/sessions/{interview_session_id}/responses",
    tags=["Interview Responses"],
)


@router.post(
    "",
    response_model=InterviewResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def submit_interview_response(
    interview_session_id: str,
    request: SubmitInterviewResponseRequest,
    session_service: InterviewSessionServiceDependency,
    response_service: InterviewResponseServiceDependency,
) -> InterviewResponseSchema:
    session = session_service.get_by_public_id(interview_session_id)

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Interview session '{interview_session_id}' does not exist",
        )

    saved = response_service.save_response(
        session.id,
        request.question_id,
        request.question_text,
        request.answer,
    )

    return InterviewResponseSchema.model_validate(saved)