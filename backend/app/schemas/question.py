from pydantic import BaseModel

class InterviewQuestionResponse(BaseModel):
    id: int
    text: str