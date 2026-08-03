from fastapi import APIRouter

from app.api.v1.routes._placeholders import not_implemented

router = APIRouter()


@router.post("/start", tags=["Interview Generation"])
async def start_interview() -> dict:
    not_implemented("interview.start")


@router.post("/answer", tags=["Interview Generation"])
async def submit_answer() -> dict:
    not_implemented("interview.answer")
