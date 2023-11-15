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
from dataclasses import dataclass, field

from app.seedwork.application.mediator.container import Container
from app.seedwork.application.mediator.middlewares import MiddlewareChain
from app.seedwork.application.mediator.request import RequestMap
from app.seedwork.application.messages import Event, Request, Response


@dataclass
class DispatchResult:
    response: Response | None = field(default=None)
    events: list[Event] = field(default_factory=list)


class Dispatcher(abc.ABC):
    async def dispatch(self, request: Request) -> DispatchResult:
        ...


class DefaultDispatcher(Dispatcher):
    def __init__(
        self,
        request_map: RequestMap,
        container: Container,
        middleware_chain: MiddlewareChain | None = None,
    ) -> None:
        self._request_map = request_map
        self._container = container
        self._middleware_chain = middleware_chain or MiddlewareChain()

    async def dispatch(self, request: Request) -> DispatchResult:
        handler_type = self._request_map.get(type(request))

        handler = await self._container.resolve(handler_type)

        wrapped_handle = self._middleware_chain.wrap(handler.handle)

        response = await wrapped_handle(request)

        return DispatchResult(response=response, events=handler.events)
