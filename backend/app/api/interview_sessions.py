from fastapi import APIRouter, Depends, status
from typing import Annotated

from app.api.dependencies import get_interview_session_service, InterviewSessionServiceDependency
from app.schemas.interview_session import (
    CreateInterviewSessionRequest,
    InterviewSessionCreatedResponse,
    InterviewSessionResponse,
)

from app.services.interview_session_service import (
    InterviewSessionService,
)

router = APIRouter(prefix="/api/v1/interview-sessions", tags=["Interview Sessions"])

@router.post(
    "",
    response_model=InterviewSessionCreatedResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_interview_session(
    request: CreateInterviewSessionRequest,
    service: InterviewSessionServiceDependency,
):
    interview_session = service.create_session(request)

    return InterviewSessionCreatedResponse(
        session=InterviewSessionResponse.model_validate(interview_session)
    )