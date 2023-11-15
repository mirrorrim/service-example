from enum import Enum

from app.presentation.api.common.schemas.base import BaseSchema


class ErrorCode(str, Enum):
    USER_ALREADY_REGISTERED = "USER_ALREADY_REGISTERED"


class CreateUserSchema(BaseSchema):
    email: str
    name: str


class UserReadSchema(BaseSchema):
    id: int
    email: str
    name: str
