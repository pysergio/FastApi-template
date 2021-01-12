from fastapi import APIRouter

from app.api.routes import info
from app.api.routes.auth import authentication

router = APIRouter()
router.include_router(authentication.router, tags=["authentication"], prefix="/auth", dependencies=[])
router.include_router(info.router, prefix="/info", tags=["info"])
