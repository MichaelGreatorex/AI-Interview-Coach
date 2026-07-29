from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated

from app.api.dependencies import get_interview_session_repository

from app.db.session import get_db
from app.repositories.interview_session_repository import (
    InterviewSessionRepository,
)
from app.services.interview_session_service import (
    InterviewSessionService,
)

def get_interview_session_service(
    repository: InterviewSessionRepository = Depends(
        get_interview_session_repository,
    ),
) -> InterviewSessionService:
    return InterviewSessionService(repository)


def get_interview_session_repository(
    db: Session = Depends(get_db),
) -> InterviewSessionRepository:
    return InterviewSessionRepository(db)


InterviewSessionServiceDependency = Annotated[
    InterviewSessionService,
    Depends(get_interview_session_service),
]