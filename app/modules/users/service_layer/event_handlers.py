from app.modules.users.domain.events import UserCreatedEvent
from app.seedwork.application.mediator.events.event_handler import EventHandler, E
from app.seedwork.infrastructure.email_sender import AbstractEmailSender
from app.seedwork.infrastructure.template_loader import AbstractTemplateRenderer
from app.settings import MailSettings


class UserCreatedEventHandler(EventHandler[UserCreatedEvent]):
    """
    Handles the request for user verification and sends a verification email to the user.
    """

    subject = "Email confirmation"
    template_name: str = "emails/email-confirmation.html"

    def __init__(
        self,
        email_sender: AbstractEmailSender,
        template_renderer: AbstractTemplateRenderer,
        mail_settings: MailSettings,
    ):
        self.email_sender = email_sender
        self.template_renderer = template_renderer
        self.confirmation_url = mail_settings.email_confirmation_url

    async def handle(self, event: UserCreatedEvent) -> None:
        email_body = await self.template_renderer.render(
            self.template_name,
            user_name=event.name,
            confirmation_url=f"{self.confirmation_url}?confirmation=n2oFp9TCD6N29R",
        )
        await self.email_sender.send(event.email, self.subject, email_body)
