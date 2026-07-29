from .session import Base

__all__ = ["Base"]


def __getattr__(name: str):
    if name == "InterviewSession":
        from app.models.interview_session import InterviewSession

        return InterviewSession
    raise AttributeError(name)
