import abc
import logging

from app.modules.users.domain.models import User
from app.modules.users.infrastructure.errors import DuplicateKeyError

logger = logging.getLogger(__name__)

USERS_STORAGE: list[User] = []


class AbstractUserRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, email: str, name: str) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_list(
        self, search_query: str | None = None, limit: int = 25, offset: int = 0
    ) -> list[User]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_count(self, search_query: str | None) -> int:
        raise NotImplementedError


class InMemoryUserRepository(AbstractUserRepository):
    async def create(self, email: str, name: str) -> int:
        email = email.strip().lower()
        for user in USERS_STORAGE:
            if user.email == email:
                raise DuplicateKeyError()
        user_ids = [0] + [user.id for user in USERS_STORAGE]
        new_id = max(user_ids) + 1

        user = User(id=new_id, email=email, name=name)
        USERS_STORAGE.append(user)

        logger.info("User %s saved", user)
        return new_id

    async def get_list(
        self, search_query: str | None = None, limit: int = 25, offset: int = 0
    ) -> list[User]:
        users = USERS_STORAGE
        if search_query:
            users = [user for user in users if search_query in user.email or search_query in user.name]
        return users[offset:limit]

    async def get_count(self, search_query: str | None) -> int:
        users = USERS_STORAGE
        if search_query:
            users = [user for user in users if search_query in user.email or search_query in user.name]
        return len(users)
