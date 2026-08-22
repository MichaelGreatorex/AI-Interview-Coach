from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.interview_document import InterviewDocument


class InterviewDocumentRepository:
    def __init__(self, db: Session):
        self._db = db

    def create(
        self,
        interview_document: InterviewDocument,
    ) -> InterviewDocument:
        self._db.add(interview_document)
        self._db.commit()
        self._db.refresh(interview_document)

        return interview_document

    def get_by_interview_session_id(
        self,
        interview_session_id: int,
    ) -> list[InterviewDocument]:
        statement = (
            select(InterviewDocument)
            .where(
                InterviewDocument.interview_session_id == interview_session_id,
            )
            .order_by(InterviewDocument.created_at)
        )

        return list(self._db.scalars(statement))
    
    def get_by_id(
        self,
        document_id: int,
    ) -> InterviewDocument | None:
        return self._db.get(
            InterviewDocument,
            document_id,
        )


    def update(
        self,
        interview_document: InterviewDocument,
    ) -> InterviewDocument:
        self._db.commit()
        self._db.refresh(interview_document)

        return interview_document

    def delete(
        self,
        interview_document: InterviewDocument,
    ) -> None:
        self._db.delete(interview_document)
        self._db.flush()