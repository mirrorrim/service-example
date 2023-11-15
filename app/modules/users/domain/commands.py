from dataclasses import dataclass

from app.seedwork.application.messages import Request, Response


@dataclass(frozen=True, kw_only=True)
class CreateUserRequest(Request):
    email: str
    name: str


@dataclass(frozen=True, kw_only=True)
class CreateUserResponse(Response):
    id: int
