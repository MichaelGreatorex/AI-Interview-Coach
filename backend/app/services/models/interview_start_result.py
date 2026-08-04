from dataclasses import dataclass

from app.models.interview_session import InterviewSession


@dataclass
class InterviewStartResult:
    session: InterviewSession
    questions: list[str]