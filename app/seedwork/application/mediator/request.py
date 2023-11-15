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
from typing import Callable, Protocol, Type, TypeVar

from app.seedwork.application.messages import Event, Request, Response

Req = TypeVar("Req", bound=Request, contravariant=True)
Res = TypeVar("Res", Response, None, covariant=True)


class RequestHandler(Protocol[Req, Res]):
    """The request handler interface.

    The request handler is an object, which gets a request as input and may return a response as a result.

    Command handler example::

      class JoinMeetingCommandHandler(RequestHandler[JoinMeetingCommand, None])
          def __init__(self, meetings_api: MeetingAPIProtocol) -> None:
              self._meetings_api = meetings_api
              self.events: list[Event] = []

          async def handle(self, request: JoinMeetingCommand) -> None:
              await self._meetings_api.join_user(request.user_id, request.meeting_id)

    Query handler example::

      class ReadMeetingQueryHandler(RequestHandler[ReadMeetingQuery, ReadMeetingQueryResult])
          def __init__(self, meetings_api: MeetingAPIProtocol) -> None:
              self._meetings_api = meetings_api
              self.events: list[Event] = []

          async def handle(self, request: ReadMeetingQuery) -> ReadMeetingQueryResult:
              link = await self._meetings_api.get_link(request.meeting_id)
              return ReadMeetingQueryResult(link=link, meeting_id=request.meeting_id)

    """

    @property
    def events(self) -> list[Event]:
        return []

    @abc.abstractmethod
    async def handle(self, request: Req) -> Res:
        raise NotImplementedError


class RequestMap:
    def __init__(self) -> None:
        self._request_map: dict[Type[Request], Callable[[], RequestHandler]] = {}

    def bind(
        self,
        request_type: Type[Request],
        handler_type: Callable[[], RequestHandler],
    ) -> None:
        self._request_map[request_type] = handler_type

    def get(self, request_type: Type[Request]) -> Callable[[], RequestHandler]:
        handler_type = self._request_map.get(request_type)
        if not handler_type:
            raise RequestHandlerDoesNotExist(
                "RequestHandler not found matching Request type."
            )

        return handler_type

    def __str__(self) -> str:
        return str(self._request_map)


class RequestHandlerDoesNotExist(Exception):
    ...
