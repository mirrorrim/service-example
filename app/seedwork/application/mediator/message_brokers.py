"""
MIT License

Copyright (c) 2023 Murad Akhundov

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import abc
import json
import logging
from dataclasses import dataclass, field
from uuid import UUID, uuid4

from redis.asyncio import Redis

from app.seedwork.infrastructure.encoders import jsonable_encoder

logger = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class Message:
    message_type: str = field()
    message_name: str = field()
    message_id: UUID = field(default_factory=uuid4)
    payload: dict = field()


class MessageBroker(abc.ABC):
    """The interface over a message broker.

    Used for sending messages to message brokers (currently only redis supported).
    """

    @abc.abstractmethod
    async def send_message(self, message: Message) -> None:
        ...


class StubMessageBroker(MessageBroker):
    async def send_message(self, message: Message) -> None:
        logger.debug(
            "Sending message to stub message broker, message_id=%s", message.message_id
        )


class RedisMessageBroker(MessageBroker):
    def __init__(self, client: Redis, *, channel_prefix: str | None = None) -> None:
        self._client = client
        self._channel_prefix = channel_prefix or "app"

    async def send_message(self, message: Message) -> None:
        async with self._client.pubsub() as pubsub:
            channel = (
                f"{self._channel_prefix}:{message.message_type}:{message.message_id}"
            )

            await pubsub.subscribe(channel)

            logger.debug("Sending message to Redis Pub/Sub %s.", message.message_id)
            await self._client.publish(channel, json.dumps(jsonable_encoder(message)))
