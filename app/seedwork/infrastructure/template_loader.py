import abc
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape


class AbstractTemplateRenderer(abc.ABC):
    @abc.abstractmethod
    async def render(self, template_name: str, **kwargs) -> str:
        """Render template with passed name with passed parameters."""


class FileSystemTemplateRenderer(AbstractTemplateRenderer):
    def __init__(
        self, source_dir: str | Path, default_render_kwargs: dict[str, Any] = None
    ):
        self.env = Environment(
            loader=FileSystemLoader(source_dir),
            autoescape=select_autoescape(),
            enable_async=True,
        )
        self.default_render_kwargs = default_render_kwargs or {}

    async def render(self, template_name: str, **kwargs) -> str:
        """Render template with passed name with passed parameters."""
        template = self.env.get_template(template_name)
        rendered_template = await template.render_async(
            **(self.default_render_kwargs | kwargs)
        )
        return rendered_template
