from pydantic import BaseModel, Field


class SubmitInterviewResponseRequest(BaseModel):
    question_id: int = Field(..., description="The identifier of the question being answered")
    question_text: str = Field(..., description="The exact question shown to the candidate")
    answer: str = Field(..., description="The candidate's submitted answer")