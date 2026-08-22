from dataclasses import dataclass

from app.models.interview_document import InterviewDocument
from app.models.interview_session import InterviewSession


@dataclass
class InterviewDocumentProcessingResult:
    session: InterviewSession
    documents: list[InterviewDocument]