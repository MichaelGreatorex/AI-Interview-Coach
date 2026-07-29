from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CreateInterviewSessionRequest(BaseModel):
    candidate_name: Optional[str] = None
    job_title: Optional[str] = None


class InterviewSessionResponse(BaseModel):
    interview_session_id: str
    candidate_name: Optional[str]
    job_title: Optional[str]
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class InterviewSessionCreatedResponse(BaseModel):
    session: InterviewSessionResponse