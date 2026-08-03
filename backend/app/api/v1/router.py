from fastapi import APIRouter

from app.api.v1.routes import (
    documents,
    health,
    interview_generation,
    sessions,
)

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(interview_generation.router, prefix="/interview")
api_router.include_router(sessions.router, prefix="/sessions")
api_router.include_router(documents.router)
