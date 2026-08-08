from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.interview_session import InterviewSession
from app.db import session
from app.models.interview_document import InterviewDocument


class InterviewSessionRepository:
    def __init__(self, db: Session):
        self._db = db

    def create(
        self,
        interview_session: InterviewSession,
    ) -> InterviewSession:
        self._db.add(interview_session)
        self._db.commit()
        self._db.refresh(interview_session)

        return interview_session
    
    def update(
        self,
        interview_session: InterviewSession,
    ) -> InterviewSession:
        self._db.commit()
        self._db.refresh(interview_session)

        return interview_session

    def get_by_public_id(
        self,
        interview_session_id: str,
    ) -> InterviewSession | None:
        return (
            self._db.query(InterviewSession)
            .filter(
                InterviewSession.interview_session_id == interview_session_id
            )
            .first()
        )
        
    def delete(
        self,
        session: InterviewSession,
    ) -> None:
        self._db.delete(session)
        self._db.commit()