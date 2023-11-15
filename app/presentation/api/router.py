import logging

from fastapi import APIRouter, FastAPI

from app.presentation.api.users.router import router as users_router
from app.settings import WebSettings

logger = logging.getLogger(__name__)


def setup_routers(app: FastAPI, settings: WebSettings):
    router = APIRouter(prefix="/v1")
    router.include_router(users_router, prefix="/users", tags=["users"])

    app.include_router(router, prefix=settings.url_prefix)
    logger.info("Routes set up")
