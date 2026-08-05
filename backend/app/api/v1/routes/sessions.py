from fastapi import APIRouter, Response, status

from app.api.dependencies import (
    
    InterviewSessionServiceDependency,
)

router = APIRouter(
    prefix="/sessions",
    tags=["Interview Sessions"],
)


@router.delete(
    "/{interview_session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_session(
    interview_session_id: str,
    service: InterviewSessionServiceDependency,
) -> Response:
    service.delete_session(interview_session_id)

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
