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
from typing import Protocol, Type, TypeVar

import rodi

T = TypeVar("T")
C = TypeVar("C")


class Container(Protocol[C]):
    """
    The container interface.
    """

    @property
    def external_container(self) -> C:
        ...

    def attach_external_container(self, container: C) -> None:
        ...

    async def resolve(self, type_: Type[T]) -> T:
        ...


class RodiContainer(Container[rodi.Container]):
    def __init__(self, external_container: rodi.Container | None = None) -> None:
        self._external_container: rodi.Container | None = external_container

    @property
    def external_container(self) -> rodi.Container:
        if not self._external_container:
            raise AttributeError

        return self._external_container

    def attach_external_container(self, container: rodi.Container) -> None:
        self._external_container = container

    async def resolve(self, type_: Type[T]) -> T:
        if hasattr(self.external_container, "resolve"):
            return self.external_container.resolve(type_)
        return self._build_by_provider(type_)

    def _build_by_provider(self, type_: Type[T]) -> T:
        services = self.external_container.build_provider()
        return services.get(type_)
