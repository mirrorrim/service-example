import logging.config

from app.presentation.api.api_setup import (
    setup_exception_handlers,
    setup_middleware,
    setup_sentry,
    lifespan,
    setup_dependencies,
)
from app.presentation.api.router import setup_routers
from fastapi import FastAPI

from app.presentation.bootstrap import bootstrap
from app.settings import AppSettings, LoggingSettings, WebSettings

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    container, mediator = bootstrap()

    app_settings = container.resolve(AppSettings)
    logging_settings = container.resolve(LoggingSettings)
    web_settings = container.resolve(WebSettings)

    logging.config.dictConfig(
        logging_settings.get_logging_config(is_local=logging_settings.debug)
    )
    app = FastAPI(lifespan=lifespan, **web_settings.fastapi_kwargs)

    setup_middleware(app, web_settings)
    setup_dependencies(app, container, mediator)
    setup_exception_handlers(app)
    setup_sentry(app, app_settings)
    setup_routers(app, web_settings)

    logger.info(
        f"Startup complete. Docs at http://127.0.0.1:8000{web_settings.fastapi_kwargs['docs_url']}"
    )
    return app
