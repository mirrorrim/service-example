import logging
from functools import singledispatchmethod

from app.seedwork.application.mediator.container import Container
from app.seedwork.application.mediator.events.map import EventMap
from app.seedwork.application.mediator.message_brokers import Message, MessageBroker
from app.seedwork.application.messages import (
    DomainEvent,
    ECSTEvent,
    Event,
    NotificationEvent,
)
from app.seedwork.infrastructure.encoders import jsonable_encoder

logger = logging.getLogger(__name__)


class EventEmitter:
    """
    The event emitter is responsible for sending events to the according handlers or
    to the message broker abstraction.

    Usage::

      redis_client = Redis()  # async redis client
      message_broker = RedisMessageBroker(redis_client)
      event_map =  EventMap()
      event_map.bind(UserJoinedDomainEvent, UserJoinedDomainEventHandler)

      event_emitter = EventEmitter(event_map, container, message_broker)

      # Uses UserJoinedDomainEventHandler for handling event:
      await event_emitter.emit(user_joined_domain_event)

      # Sends event to the Redis Pub/Sub:
      await event_emitter.emit(user_joined_notification_event)

    """

    def __init__(
        self,
        event_map: EventMap,
        container: Container,
        message_broker: MessageBroker | None = None,
    ) -> None:
        self._event_map = event_map
        self._container = container
        self._message_broker = message_broker

    @singledispatchmethod
    async def emit(self, event: Event) -> None:
        ...

    @emit.register
    async def _(self, event: DomainEvent) -> None:
        handlers_types = self._event_map.get(type(event))

        for handler_type in handlers_types:
            handler = await self._container.resolve(handler_type)
            logger.debug(
                "Handling Event(%s) via event handler(%s)",
                type(event).__name__,
                handler_type.__name__,
            )
            await handler.handle(event)

    @emit.register
    async def _(self, event: NotificationEvent) -> None:
        if not self._message_broker:
            raise RuntimeError(
                "To use NotificationEvent, message_broker argument must be specified."
            )

        message = _build_message(event)

        logger.debug(
            "Sending Notification Event(%s) to message broker %s",
            event.event_id,
            type(self._message_broker).__name__,
        )

        await self._message_broker.send_message(message)

    @emit.register
    async def _(self, event: ECSTEvent) -> None:
        if not self._message_broker:
            raise RuntimeError(
                "To use ECSTEvent, message_broker argument must be specified."
            )

        message = _build_message(event)

        logger.debug(
            "Sending ECST event(%s) to message broker %s",
            event.event_id,
            type(self._message_broker).__name__,
        )

        await self._message_broker.send_message(message)


def _build_message(event: NotificationEvent | ECSTEvent) -> Message:
    payload = jsonable_encoder(event)
    return Message(
        message_type=event._event_type,
        message_name=type(event).__name__,
        message_id=event.event_id,
        payload=payload,
    )
