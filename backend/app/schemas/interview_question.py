from pydantic import BaseModel

class InterviewQuestion(BaseModel):
    id: int
    text: str


InterviewQuestionResponse = InterviewQuestion