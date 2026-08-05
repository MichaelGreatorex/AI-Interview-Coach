from fastapi import APIRouter, File, UploadFile, status

from app.api.dependencies import InterviewWorkflowServiceDependency
from app.schemas.interview import InterviewStartResponse
from app.schemas.question import InterviewQuestionResponse

router = APIRouter(
    prefix="/interviews",
    tags=["Interviews"],
)


@router.post(
    "",
    response_model=InterviewStartResponse,
    status_code=status.HTTP_201_CREATED,
)

def start_interview(
    workflow_service: InterviewWorkflowServiceDependency,
    cv: UploadFile = File(...),
    job_description: UploadFile = File(...),
) -> InterviewStartResponse:
    result = workflow_service.start_interview(
        cv_file=cv,
        job_description_file=job_description,
    )

    return InterviewStartResponse(
        session_id=result.session.interview_session_id,
        question=InterviewQuestionResponse(
            id=result.question.id,
            text=result.question.text,
        ),
    )