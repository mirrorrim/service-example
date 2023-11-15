from collections import defaultdict
from typing import Callable, Type, TypeVar

from app.seedwork.application.messages import DomainEvent
from app.seedwork.application.mediator.events.event_handler import EventHandler

E = TypeVar("E", bound=DomainEvent, contravariant=True)


class EventMap:
    def __init__(self) -> None:
        self._event_map: dict[
            Type[DomainEvent], list[Callable[[], EventHandler]]
        ] = defaultdict(lambda: [])

    def bind(
        self, event_type: Type[E], handler_type: Callable[[], EventHandler[E]]
    ) -> None:
        self._event_map[event_type].append(handler_type)

    def get(self, event_type: Type[E]) -> list[Callable[[], EventHandler[E]]]:
        return self._event_map[event_type]

    def get_events(self) -> list[Type[DomainEvent]]:
        return list(self._event_map.keys())

    def __str__(self) -> str:
        return str(self._event_map)


class EventHandlerDoesNotExists(Exception):
    ...
