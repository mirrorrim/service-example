from fastapi import APIRouter, Body, HTTPException, Depends
from starlette import status

from app.modules.users.domain.commands import CreateUserResponse, CreateUserRequest
from app.modules.users.domain.queries import GetUsersQuery, GetUsersQueryResult
from app.modules.users.service_layer.errors import UserAlreadyRegistered
from app.presentation.api.common.errors import ErrorModel
from app.presentation.api.common.pagination import Page, Params
from app.presentation.api.common.schemas.base import ObjectCreatedResponse
from app.presentation.api.dependencies.services import MediatorDep
from app.presentation.api.users.schemas import (
    ErrorCode,
    CreateUserSchema,
    UserReadSchema,
)

router = APIRouter()


@router.post(
    "/",
    name="user:create",
    status_code=status.HTTP_201_CREATED,
    response_model=ObjectCreatedResponse,
    responses={
        status.HTTP_201_CREATED: {"description": "User created."},
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.USER_ALREADY_REGISTERED: {
                            "summary": "User with this email is already registered.",
                            "value": {"detail": ErrorCode.USER_ALREADY_REGISTERED},
                        },
                    }
                },
            },
        },
    },
)
async def create_user(
    mediator: MediatorDep,
    data: CreateUserSchema = Body(),
):
    """Create a new user."""
    try:
        user: CreateUserResponse = await mediator.send(
            CreateUserRequest(email=data.email, name=data.name)
        )
        return {"id": user.id}
    except UserAlreadyRegistered:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.USER_ALREADY_REGISTERED,
        )


@router.get(
    "/",
    response_model=Page[UserReadSchema],
    status_code=status.HTTP_200_OK,
)
async def get_users(
    mediator: MediatorDep,
    q: str | None = None,
    params: Params = Depends(),
):
    result: GetUsersQueryResult = await mediator.send(
        GetUsersQuery(search_query=q, limit=params.limit, offset=params.offset)
    )
    return Page[UserReadSchema](count=result.count, data=result.data)
