from fastapi import APIRouter, status

from app.api.dependencies import (
    InterviewResponseServiceDependency,
    InterviewSessionServiceDependency,
)

from app.schemas.submit_interview_response_request import (
    SubmitInterviewResponseRequest,
)

from app.schemas.interview_response import (
    InterviewResponseSchema,
)


router = APIRouter(
    prefix="/sessions/{interview_session_id}/responses",
    tags=["Interview Responses"],
)


@router.post(
    "",
    response_model=InterviewResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def submit_interview_response(
    interview_session_id: str,
    request: SubmitInterviewResponseRequest,
    session_service: InterviewSessionServiceDependency,
    response_service: InterviewResponseServiceDependency,
) -> InterviewResponseSchema:

    session = session_service.get_by_public_id(
        interview_session_id,
    )

    if session is None:
        raise ValueError(
            f"Interview session '{interview_session_id}' does not exist"
        )

    response = response_service.save_response(
        session_id=session.id,
        question_id=request.question_id,
        question_text=request.question_text,
        answer=request.answer,
    )

    return InterviewResponseSchema.model_validate(response)