from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class TheResponse(BaseModel):
    is_ready: bool
    msg: str


@router.get("", response_model=TheResponse, name="main:test-example")
async def retrieve_current_user() -> TheResponse:
    return TheResponse(is_ready=True, msg="Welcome to Darqube app")
