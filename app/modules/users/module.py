from rodi import Container

from app.modules.users.domain.commands import CreateUserRequest
from app.modules.users.domain.events import UserCreatedEvent
from app.modules.users.domain.queries import GetUsersQuery
from app.modules.users.infrastructure.repository import InMemoryUserRepository, AbstractUserRepository
from app.modules.users.service_layer.command_handlers import CreateUserHandler
from app.modules.users.service_layer.event_handlers import UserCreatedEventHandler
from app.modules.users.service_layer.query_handlers import GetUsersQueryHandler
from app.seedwork.application.mediator.events.map import EventMap
from app.seedwork.application.mediator.request import RequestMap
from app.seedwork.application.modules import BusinessModule


class UsersModule(BusinessModule):

    def register_dependencies(self, container: Container):
        container.register(AbstractUserRepository, InMemoryUserRepository)
        container.register(CreateUserHandler)
        container.register(UserCreatedEventHandler)
        container.register(GetUsersQueryHandler)

    def register_requests(self, request_map: RequestMap):
        request_map.bind(CreateUserRequest, CreateUserHandler)
        request_map.bind(GetUsersQuery, GetUsersQueryHandler)

    def register_events(self, event_map: EventMap):
        event_map.bind(UserCreatedEvent, UserCreatedEventHandler)
