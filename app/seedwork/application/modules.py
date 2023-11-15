import abc
import logging

from rodi import Container

from app.seedwork.application.mediator.events.map import EventMap
from app.seedwork.application.mediator.request import RequestMap

logger = logging.getLogger(__name__)


class BusinessModule:
    @abc.abstractmethod
    def register_dependencies(self, container: Container):
        ...

    @abc.abstractmethod
    def register_requests(self, request_map: RequestMap):
        ...

    @abc.abstractmethod
    def register_events(self, event_map: EventMap):
        ...
