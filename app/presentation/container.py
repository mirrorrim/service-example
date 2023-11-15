import redis.asyncio
from redis.asyncio import Redis
from rodi import ActivationScope, Container

from app.seedwork.infrastructure.email_sender import AbstractEmailSender, StubEmailSender
from app.seedwork.infrastructure.template_loader import FileSystemTemplateRenderer, AbstractTemplateRenderer
from app.settings import (
    AppSettings,
    LoggingSettings,
    MailSettings,
    RedisSettings,
    WebSettings,
)


def setup_container() -> Container:
    """Setup common dependencies."""
    container = Container()

    # register settings factories
    container.add_transient_by_factory(lambda: AppSettings(), AppSettings)
    container.add_transient_by_factory(lambda: WebSettings(), WebSettings)
    container.add_transient_by_factory(lambda: LoggingSettings(), LoggingSettings)
    container.add_transient_by_factory(lambda: MailSettings(), MailSettings)
    container.add_transient_by_factory(lambda: RedisSettings(), RedisSettings)

    # register singletons
    container.add_singleton_by_factory(_build_redis_client, Redis)

    # register factories
    container.add_transient_by_factory(
        _build_template_renderer, AbstractTemplateRenderer
    )
    container.add_transient_by_factory(_build_email_sender, AbstractEmailSender)

    return container


def _build_redis_client(scope: ActivationScope) -> Redis:
    settings = scope.provider.get(RedisSettings)
    return redis.asyncio.from_url(settings.redis_url, decode_responses=True)


def _build_template_renderer(scope: ActivationScope) -> AbstractTemplateRenderer:
    app_settings = scope.provider.get(AppSettings)
    settings = scope.provider.get(MailSettings)
    return FileSystemTemplateRenderer(
        app_settings.project_path / "templates",
        default_render_kwargs=dict(
            privacy_url=settings.privacy_url,
            settings_url=settings.user_settings_url,
            unsubscribe_url=settings.email_unsubscribe_url,
        ),
    )


def _build_email_sender(scope: ActivationScope) -> AbstractEmailSender:
    # return EmailSender(
    #     MailjetClient((settings.mailjet_api_key, settings.mailjet_secret_key)),
    #     from_email=settings.default_from_email,
    #     from_email_name=settings.default_from_email_name,
    # )
    return StubEmailSender()
