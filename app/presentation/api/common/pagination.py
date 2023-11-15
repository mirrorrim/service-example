from __future__ import annotations

from collections.abc import Sequence
from typing import Generic, TypeVar

from fastapi import Query

from app.presentation.api.common.schemas.base import BaseSchema

T = TypeVar("T")


class Page(BaseSchema, Generic[T]):
    count: int
    data: Sequence[T]


class Params(BaseSchema):
    limit: int = Query(25, ge=1, le=100, description="Page size limit")
    offset: int = Query(0, ge=0, description="Page offset")
