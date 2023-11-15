import logging
from http import HTTPStatus
from typing import Any, Literal

import httpx
from pydantic import BaseModel, Field, ConfigDict

logger = logging.getLogger(__name__)

HttpMethod = Literal["GET", "OPTIONS", "HEAD", "POST", "PUT", "PATCH", "DELETE"]


class EmailUser(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    email: str = Field(alias="Email")
    name: str | None = Field(alias="Name")


class Attachment(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    content_type: str = Field(alias="ContentType")
    filename: str = Field(alias="Filename")
    base64_content: str = Field(alias="Base64Content")
    content_id: str | None = Field(alias="ContentID")


class Message(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    from_user: EmailUser = Field(alias="From")
    to_users: list[EmailUser] = Field(alias="To")
    subject: str = Field(alias="Subject")
    text_part: str | None = Field(alias="TextPart")
    html_part: str | None = Field(alias="HTMLPart")
    attachments: list[Attachment] | None = Field(alias="Attachments")
    inline_attachments: list[Attachment] | None = Field(alias="InlinedAttachments")


class MailjetClient:
    base_url = "https://api.mailjet.com/v3.1"

    def __init__(self, auth: tuple[str, str], timeout: float = 5.0):
        self.auth = auth
        self.timeout = timeout

    async def send_email(
        self,
        from_user: EmailUser,
        to_users: list[EmailUser],
        subject: str,
        text_part: str | None = None,
        html_part: str | None = None,
        attachments: list[Attachment] | None = None,
        inline_attachments: list[Attachment] | None = None,
    ) -> bool:
        """Send email. Return True if was sent, False otherwise.

        :raises TimeoutError when request to Mailjet timed out
        :raises MailjetAPIError when transport error occurred
        """
        msg = Message(
            from_user=from_user,
            to_users=to_users,
            subject=subject,
            text_part=text_part,
            html_part=html_part,
            attachments=attachments,
            inline_attachments=inline_attachments,
        )
        payload = {"Messages": [msg.dict(exclude_none=True, by_alias=True)]}
        response = await self._call_api("POST", f"{self.base_url}/send", json=payload)
        if response.status_code != HTTPStatus.OK:
            logger.error(
                "Failed to send email. Mailjet returned %d status code. Response: %s",
                response.status_code,
                response.text,
            )
            return False
        return response.json()

    async def _call_api(
        self, method: HttpMethod, url: str, json: dict[str, Any] | None = None
    ) -> httpx.Response | None:
        if not all(self.auth):
            return None
        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(
                    method,
                    url,
                    json=json,
                    auth=self.auth,
                    timeout=self.timeout,
                )
                return response
            except httpx.TimeoutException:
                raise TimeoutError from None
            except httpx.RequestError as exc:
                raise MailjetAPIError(exc) from None


class MailjetAPIError(Exception):
    ...
