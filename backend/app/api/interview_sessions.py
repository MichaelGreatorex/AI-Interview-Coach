from fastapi import APIRouter, status

from app.api.dependencies import InterviewSessionServiceDependency
from app.schemas.interview_session import (
    CreateInterviewSessionRequest,
    InterviewSessionCreatedResponse,
    InterviewSessionResponse,
)

router = APIRouter(prefix="/api/v1/interview-sessions", tags=["Interview Sessions"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
def create_interview_session(
    request: CreateInterviewSessionRequest,
    service: InterviewSessionServiceDependency,
) -> InterviewSessionCreatedResponse:
    interview_session = service.create_session(request)

    return InterviewSessionCreatedResponse(
        session=InterviewSessionResponse.model_validate(interview_session)
    )