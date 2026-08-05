from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.interview_response import InterviewResponse


class InterviewResponseRepository:
    def __init__(self, db: Session):
        self._db = db

    def create(
        self,
        interview_response: InterviewResponse,
    ) -> InterviewResponse:
        self._db.add(interview_response)
        self._db.commit()
        self._db.refresh(interview_response)

        return interview_response

    def get_for_session(
        self,
        session_id: int,
    ) -> list[InterviewResponse]:
        return (
            self._db.query(InterviewResponse)
            .filter(
                InterviewResponse.interview_session_id == session_id
            )
            .order_by(
                InterviewResponse.created_at
            )
            .all()
        )
    
    def get_by_session_and_question(
        self,
        session_id: int,
        question_id: int,
    ) -> InterviewResponse | None:
        statement = (
            select(InterviewResponse)
            .where(
                InterviewResponse.interview_session_id == session_id,
                InterviewResponse.question_id == question_id,
            )
        )

        return self._db.scalar(statement)

    def delete_for_session(
        self,
        session_id: int,
    ) -> None:
        responses = self.get_for_session(session_id)

        for response in responses:
            self._db.delete(response)

        self._db.commit()