from enum import Enum

from fastapi import HTTPException
from starlette import status

from app.presentation.api.common.schemas.base import BaseSchema


class ErrorModel(BaseSchema):
    detail: str


class CommonErrorCode(str, Enum):
    NOT_FOUND = "NOT_FOUND"


class HTTPNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=CommonErrorCode.NOT_FOUND
        )
