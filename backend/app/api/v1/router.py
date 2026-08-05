from fastapi import APIRouter

from app.api.v1.routes import (
    health,
    interviews,
    sessions,
    responses,
)

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(interviews.router)
api_router.include_router(sessions.router)
api_router.include_router(responses.router)

