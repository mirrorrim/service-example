from importlib.metadata import version
from pathlib import Path
from typing import Literal, Any

from pydantic import field_validator, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

VERSION = version("service-example")  # name of the package specified pyproject.toml

base_path: Path = Path(__file__).parent.parent

ENVFILE = base_path / ".env"


class BaseAppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENVFILE, env_file_encoding='utf-8', env_prefix="APP_")

    debug: bool = False


class AppSettings(BaseAppSettings):
    base_path: Path = base_path
    project_path: Path = base_path / "app"
    sentry_dsn: str = ""


class WebSettings(BaseAppSettings):
    """Settings used for FastAPI instance."""

    disable_docs: bool = False
    project_name: str = "Example API"

    allowed_hosts: list[str] = [
        "*",
    ]
    cors_origin_regex: str = (
        r"^(https?:\/\/(?:.+\.)?(localhost|127\.0\.0\.1)(?::\d{1,5})?)$"
    )
    url_prefix: str = "/api"

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        fastapi_kwargs = {
            "debug": self.debug,
            "docs_url": f"{self.url_prefix}/docs/",
            "openapi_prefix": "",
            "openapi_url": f"{self.url_prefix}/openapi.json",
            "redoc_url": f"{self.url_prefix}/redoc/",
            "title": self.project_name,
            "version": VERSION,
        }
        if self.disable_docs:
            fastapi_kwargs.update(
                {"docs_url": None, "openapi_url": None, "redoc_url": None},
            )
        return fastapi_kwargs


class LoggingSettings(BaseAppSettings):
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    @field_validator("log_level", mode="before")
    def upper_case(cls, value):  # noqa: N805
        return value.upper()

    def get_logging_config(self, is_local: bool):
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "verbose": {
                    "format": "%(levelname)s %(asctime)s %(name)s:%(lineno)d %(process)d %(message)s %(extra_data)s",
                    "()": "app.seedwork.infrastructure.log_formatters.LogsFormatter",
                },
                "json": {
                    "format": "%(levelname)s %(asctime)s %(pathname)s:%(lineno)d %(process)d %(message)s %(extra_data)s",
                    "()": "app.seedwork.infrastructure.log_formatters.JsonLogsFormatter",
                    "json_ensure_ascii": False,
                },
            },
            "handlers": {
                "console": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "formatter": "json",
                },
                # Developers probably want to see formatted Traceback in console
                "local_console": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "formatter": "verbose",
                },
            },
            "loggers": {
                "app": {
                    "handlers": ["local_console"] if is_local else ["console"],
                    "level": self.log_level,
                    "propagate": False,
                },
                "": {
                    "handlers": ["local_console"] if is_local else ["console"],
                    "level": "WARNING",
                },
            },
        }


class MailSettings(BaseAppSettings):
    mailjet_api_key: str = ""
    mailjet_secret_key: str = ""
    default_from_email: str = "noreply@example.com"
    default_from_email_name: str = "example.com"

    root_domain: str = "example.com"
    app_url: str = f"https://app.{root_domain}"
    email_confirmation_url: str = f"{app_url}/confirm"
    reset_password_url: str = f"{app_url}/reset-password"
    privacy_url: str = f"{app_url}/privacy"
    user_settings_url: str = f"{app_url}/settings"
    email_unsubscribe_url: str = f"{app_url}/unsubscribe"


class RedisSettings(BaseAppSettings):
    redis_url: RedisDsn = "redis://localhost:6379"
