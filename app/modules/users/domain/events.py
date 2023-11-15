from dataclasses import field, dataclass

from app.seedwork.application.messages import DomainEvent


@dataclass(frozen=True, kw_only=True, eq=True)
class UserCreatedEvent(DomainEvent):
    id: int = field()
    email: str = field()
    name: str = field()
