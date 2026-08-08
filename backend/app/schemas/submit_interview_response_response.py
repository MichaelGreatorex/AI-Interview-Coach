from pydantic import BaseModel

from app.schemas.interview_question import InterviewQuestion


class SubmitInterviewResponseResponse(BaseModel):
    interview_complete: bool
    next_question: InterviewQuestion | None = None