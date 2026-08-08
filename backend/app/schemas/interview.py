from pydantic import BaseModel

from app.schemas.interview_question import InterviewQuestionResponse


class InterviewStartResponse(BaseModel):
    session_id: str
    question: InterviewQuestionResponse
