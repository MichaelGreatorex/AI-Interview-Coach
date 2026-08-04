from pydantic import BaseModel


class InterviewStartResponse(BaseModel):
    session_id: str
    questions: list[str]