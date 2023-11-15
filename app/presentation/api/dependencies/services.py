from typing import Annotated, Any, Protocol

from fastapi import Depends, Request
from rodi import Container
from starlette.datastructures import URL

from app.seedwork.application.mediator.mediator import Mediator
from app.settings import AppSettings


def get_container() -> Container:
    ...


def get_mediator() -> Mediator:
    ...


ContainerDep = Annotated[Container, Depends(get_container)]
MediatorDep = Annotated[Mediator, Depends(get_mediator)]


def depends(typ: Any):
    """Extract dependency from rodi container."""
    def _inner(container: Annotated[Container, Depends(get_container)]):
        obj = container.resolve(typ)
        return obj
    return Depends(_inner)


class GetUrlFor(Protocol):
    def __call__(self, name: str, **path_params: Any) -> str:
        ...


def get_url_for_factory(
    request: Request, settings: Annotated[AppSettings, depends(AppSettings)]
) -> GetUrlFor:
    def _inner(name: str, **path_params: Any) -> str:
        project_url = URL(str(request.url_for(name, **path_params)))
        if not settings.DEBUG:
            project_url = project_url.replace(scheme="https")
        return str(project_url)

    return _inner
