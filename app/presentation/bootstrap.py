from rodi import Container

from app.modules.users.module import UsersModule
from app.presentation.container import setup_container
from app.seedwork.application.mediator.container import RodiContainer
from app.seedwork.application.mediator.events.event_emitter import EventEmitter
from app.seedwork.application.mediator.events.map import EventMap
from app.seedwork.application.mediator.mediator import Mediator
from app.seedwork.application.mediator.message_brokers import StubMessageBroker
from app.seedwork.application.mediator.middlewares import MiddlewareChain, LoggingMiddleware
from app.seedwork.application.mediator.request import RequestMap

MODULES = [UsersModule]


def bootstrap() -> tuple[Container, Mediator]:
    container = setup_container()

    event_map = EventMap()
    request_map = RequestMap()
    rodi_container = RodiContainer(container)

    models = []
    for module_cls in MODULES:
        module = module_cls()
        module.register_dependencies(container)
        module.register_events(event_map)
        module.register_requests(request_map)

    middleware_chain = MiddlewareChain()
    middleware_chain.add(LoggingMiddleware())

    event_emitter = EventEmitter(
        # message_broker=RedisMessageBroker(container.resolve(Redis)),
        message_broker=StubMessageBroker(),
        event_map=event_map,
        container=rodi_container,
    )

    mediator = Mediator(
        request_map=request_map,
        event_emitter=event_emitter,
        container=rodi_container,
        middleware_chain=middleware_chain,
    )
    return container, mediator
