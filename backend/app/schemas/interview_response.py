from datetime import datetime

from pydantic import BaseModel, ConfigDict


class InterviewResponseSchema(BaseModel):
    id: int
    question_id: int
    question_text: str
    answer: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )