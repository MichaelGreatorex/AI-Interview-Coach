from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.interview_session_repository import (
    InterviewSessionRepository,
)
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
    db: Session = Depends(get_db),
) -> InterviewSessionCreatedResponse:

    repository = InterviewSessionRepository(db)
    service = InterviewSessionService(repository)

    interview_session = service.create_session(request)

    return InterviewSessionCreatedResponse(
        session=InterviewSessionResponse.model_validate(interview_session)
    )