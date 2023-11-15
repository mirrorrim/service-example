import logging
from contextlib import asynccontextmanager
from http import HTTPStatus

import sentry_sdk
from fastapi import FastAPI
from rodi import Container
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.presentation.api.dependencies.services import get_mediator, get_container
from app.seedwork.application.mediator.mediator import Mediator
from app.settings import AppSettings, WebSettings

logger = logging.getLogger(__name__)


async def permission_error_handler(request: Request, exc: PermissionError):
    return JSONResponse(
        status_code=HTTPStatus.FORBIDDEN,
        content={"detail": str(exc) or "Permission denied"},
    )


def setup_middleware(app: FastAPI, settings: WebSettings):
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=None if settings.debug else settings.allowed_hosts,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=settings.cors_origin_regex,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    logger.info("Middleware set up")


def setup_sentry(app: FastAPI, settings: AppSettings):
    if settings.sentry_dsn:
        sentry_sdk.init(
            dsn=settings.sentry_dsn,
            integrations=[
                StarletteIntegration(transaction_style="endpoint"),
                FastApiIntegration(transaction_style="endpoint"),
            ],
        )
        logger.info("Sentry set up")
    else:
        logger.info("Sentry was not set up")


def setup_exception_handlers(app: FastAPI):
    app.add_exception_handler(PermissionError, permission_error_handler)
    logger.info("Exception handlers set up")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Lifespan: init completed")
    yield
    logger.info("Lifespan: unloaded")


def setup_dependencies(
    app: FastAPI,
    container: Container,
    mediator: Mediator,
):
    """Replace stubs with real implementation."""
    app.dependency_overrides[get_container] = lambda: container
    app.dependency_overrides[get_mediator] = lambda: mediator

    logger.info("Dependencies set up")
