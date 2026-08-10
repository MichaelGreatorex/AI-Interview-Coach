from fastapi import APIRouter

from app.api.dependencies import InterviewSessionServiceDependency
from app.schemas.submit_interview_response_request import (
    SubmitInterviewResponseRequest,
)
from app.schemas.submit_interview_response_response import (
    SubmitInterviewResponseResponse,
)

router = APIRouter(
    prefix="/sessions/{interview_session_id}/responses",
    tags=["Interview Responses"],
)


@router.post(
    "",
    response_model=SubmitInterviewResponseResponse,
)
def submit_interview_response(
    interview_session_id: str,
    request: SubmitInterviewResponseRequest,
    session_service: InterviewSessionServiceDependency,
) -> SubmitInterviewResponseResponse:
    return session_service.submit_response(
        interview_session_id,
        request,
    )