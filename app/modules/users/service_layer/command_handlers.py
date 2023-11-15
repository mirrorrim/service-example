import logging

from app.modules.users.domain.commands import CreateUserRequest, CreateUserResponse
from app.modules.users.domain.events import UserCreatedEvent
from app.modules.users.infrastructure.errors import DuplicateKeyError
from app.modules.users.infrastructure.repository import AbstractUserRepository
from app.modules.users.service_layer.errors import UserAlreadyRegistered
from app.seedwork.application.mediator.request import RequestHandler

logger = logging.getLogger(__name__)


class CreateUserHandler(RequestHandler[CreateUserRequest, CreateUserResponse]):
    def __init__(self, repository: AbstractUserRepository):
        self.repo = repository
        self._events = []

    async def handle(self, request: CreateUserRequest) -> CreateUserResponse:
        try:
            user_id = await self.repo.create(request.email, request.name)
        except DuplicateKeyError:
            raise UserAlreadyRegistered("User with this email already registered.")
        self.events.append(
            UserCreatedEvent(id=user_id, email=request.email, name=request.name)
        )
        return CreateUserResponse(id=user_id)

    @property
    def events(self):
        return self._events
