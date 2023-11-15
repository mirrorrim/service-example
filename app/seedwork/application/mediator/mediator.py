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
from typing import Type

from app.seedwork.application.mediator.container import Container
from app.seedwork.application.mediator.dispatcher import DefaultDispatcher, Dispatcher
from app.seedwork.application.mediator.events.event_emitter import EventEmitter
from app.seedwork.application.mediator.middlewares import MiddlewareChain
from app.seedwork.application.mediator.request import RequestMap
from app.seedwork.application.messages import Event, Request, Response


class Mediator:
    """The main mediator object.

    Usage::

      redis_client = Redis()  # async redis client
      message_broker = RedisMessageBroker(redis_client)
      event_map = EventMap()
      event_map.bind(UserJoinedDomainEvent, UserJoinedDomainEventHandler)
      request_map = RequestMap()
      request_map.bind(JoinUserCommand, JoinUserCommandHandler)
      event_emitter = EventEmitter(event_map, container, message_broker)

      mediator = Mediator(
        event_emitter=event_emitter,
        request_map=request_map,
        container=container
      )

      # Handles command and published events by the command handler.
      await mediator.send(join_user_command)

    """

    def __init__(
        self,
        request_map: RequestMap,
        container: Container,
        event_emitter: EventEmitter,
        middleware_chain: MiddlewareChain | None = None,
        *,
        dispatcher_type: Type[Dispatcher] = DefaultDispatcher,
    ) -> None:
        self._event_emitter = event_emitter
        self._dispatcher = dispatcher_type(
            request_map=request_map, container=container, middleware_chain=middleware_chain  # type: ignore
        )

    async def send(self, request: Request) -> Response | None:
        dispatch_result = await self._dispatcher.dispatch(request)

        if dispatch_result.events:
            await self._send_events(dispatch_result.events.copy())

        return dispatch_result.response

    async def _send_events(self, events: list[Event]) -> None:
        while events:
            event = events.pop()
            await self._event_emitter.emit(event)
