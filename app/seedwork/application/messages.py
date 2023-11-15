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
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass(frozen=True, kw_only=True)
class Request:
    """Base class for request-type objects.

    The request is an input of the request handler.
    Often Request is used for defining queries or commands.

    Usage::

      @dataclass(frozen=True, kw_only=True)
      class JoinMeetingCommand(Request):
          meeting_id: int = field()
          user_id: int = field()

      @dataclass(frozen=True, kw_only=True)
      class ReadMeetingByIdQuery(Request):
          meeting_id: int = field()

    """

    request_id: UUID = field(default_factory=uuid4)


@dataclass(frozen=True, kw_only=True)
class Response:
    """Base class for response type objects.

    The response is a result of the request handling, which hold by RequestHandler.

    Often the response is used for defining the result of the query.

    Usage::

        @dataclass(frozen=True, kw_only=True)
        class ReadMeetingQueryResult(Response):
            meeting_id: int = field()
            link: str = field()
            status: MeetingStatusEnum = field()

    """


@dataclass(frozen=True, kw_only=True)
class Event:
    ...


@dataclass(frozen=True, kw_only=True)
class DomainEvent(Event):
    """The base class for domain events."""


@dataclass(frozen=True, kw_only=True)
class NotificationEvent(Event):
    """The base class for notification events.

    Contains only identification information about state change.

    Example plain structure::

      {
          "event_id": "82a0b10e-1b3d-4c3c-9bdd-3934f8f824c2",
          "event_timestamp": "2023-03-06 12:11:35.103792",
          "changed_user_id": 987
      }

    """

    event_id: UUID = field(default_factory=uuid4)
    event_timestamp: datetime = field(default_factory=datetime.utcnow)
    _event_type = "notification_event"


@dataclass(frozen=True, kw_only=True)
class ECSTEvent(Event):
    """Base class for ECST events.

    ECST means event-carried state transfer.

    Contains full information about state change.

    Example plain structure::

      {
          "event_id": "82a0b10e-1b3d-4c3c-9bdd-3934f8f824c2",
          "event_timestamp": "2023-03-06 12:11:35.103792",
          "user_id": 987,
          "new_user_last_name": "Doe",
          "new_user_nickname": "kend"
      }

    """

    event_id: UUID = field(default_factory=uuid4)
    event_timestamp: datetime = field(default_factory=datetime.utcnow)
    _event_type = "ecst_event"
