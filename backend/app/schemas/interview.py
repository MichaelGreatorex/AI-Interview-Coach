from unittest import result

from pydantic import BaseModel
from app.schemas.question import InterviewQuestionResponse

class InterviewStartResponse(BaseModel):
    session_id: str
    question: InterviewQuestionResponse
