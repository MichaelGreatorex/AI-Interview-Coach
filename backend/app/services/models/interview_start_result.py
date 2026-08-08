from dataclasses import dataclass
from app.models.interview_session import InterviewSession
from app.schemas.interview_question import InterviewQuestion


@dataclass(frozen=True)
class InterviewStartResult:
    session: InterviewSession
    question: InterviewQuestion