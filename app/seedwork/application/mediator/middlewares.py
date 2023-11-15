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
import functools
import logging
from typing import Awaitable, Callable, Mapping, Protocol, TypeVar

from app.seedwork.application.messages import Request, Response

Req = TypeVar("Req", bound=Request, contravariant=True)
Res = TypeVar("Res", Response, None, covariant=True)
HandleType = Callable[[Req], Awaitable[Res]]


class Middleware(abc.ABC):
    @abc.abstractmethod
    async def __call__(self, request: Request, handle: HandleType) -> Res:
        ...


Handle = Callable[[Req], Awaitable[Res]]


class MiddlewareChain:
    def __init__(self) -> None:
        self._chain: list[Middleware] = []

    def set(self, chain: list[Middleware]) -> None:
        self._chain = chain

    def add(self, middleware: Middleware) -> None:
        self._chain.append(middleware)

    def wrap(self, handle: Handle) -> Handle:
        for middleware in reversed(self._chain):
            handle = functools.partial(middleware.__call__, handle=handle)

        return handle


class Logger(Protocol):
    def log(
        self, level: int, msg: str, *args, extra: Mapping[str, object] | None = None
    ) -> None:
        ...


class LoggingMiddleware(Middleware):
    def __init__(
        self,
        logger: Logger | None = None,
        level: int = logging.DEBUG,
    ) -> None:
        self._logger = logger or logging.getLogger(__name__)
        self._level = level

    async def __call__(self, request: Request, handle: HandleType) -> Res:
        self._logger.log(
            self._level,
            "Handle %s request",
            type(request).__name__,
            extra={"request": request},
        )
        response = await handle(request)
        self._logger.log(
            self._level,
            "Request %s handled. Response: %s",
            type(request).__name__,
            response,
            extra={"request": request},
        )

        return response
