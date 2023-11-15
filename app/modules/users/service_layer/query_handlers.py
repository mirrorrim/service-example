from app.modules.users.domain.queries import GetUsersQuery, GetUsersQueryResult
from app.modules.users.infrastructure.repository import AbstractUserRepository
from app.seedwork.application.mediator.request import RequestHandler


class GetUsersQueryHandler(RequestHandler[GetUsersQuery, GetUsersQueryResult]):
    def __init__(self, repository: AbstractUserRepository):
        self.repo = repository

    async def handle(self, request: GetUsersQuery) -> GetUsersQueryResult:
        users = await self.repo.get_list(request.search_query, request.limit, request.offset)
        users_count = await self.repo.get_count(request.search_query)
        return GetUsersQueryResult(data=users, count=users_count)
