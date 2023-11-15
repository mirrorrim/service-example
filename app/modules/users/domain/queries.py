from dataclasses import dataclass, field

from app.modules.users.domain.models import User
from app.seedwork.application.messages import Request, Response


@dataclass(frozen=True, kw_only=True)
class GetUsersQuery(Request):
    search_query: str | None = field(default=None)
    limit: int = field(default=25)
    offset: int = field(default=0)


@dataclass(frozen=True, kw_only=True)
class GetUsersQueryResult(Response):
    count: int
    data: list[User]
