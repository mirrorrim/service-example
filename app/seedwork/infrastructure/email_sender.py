import abc
import logging

from app.seedwork.infrastructure.mailjet import EmailUser, MailjetClient

logger = logging.getLogger(__name__)


class AbstractEmailSender(abc.ABC):
    @abc.abstractmethod
    async def send(self, destination: str, subject: str, message: str):
        pass


class EmailSender(AbstractEmailSender):
    def __init__(self, client: MailjetClient, from_email: str, from_email_name: str):
        self.client = client
        self.from_user = EmailUser(email=from_email, name=from_email_name)

    async def send(self, destination: str, subject: str, message: str):
        to_user = EmailUser(email=destination)
        await self.client.send_email(
            self.from_user, [to_user], subject, html_part=message
        )


class StubEmailSender(AbstractEmailSender):
    async def send(self, destination: str, subject: str, message: str):
        logger.info(
            "FAKE EMAIL SENDER\nDestination: %s\n\nSubject: %s\n\nMessage: %s",
            destination,
            subject,
            message,
        )
