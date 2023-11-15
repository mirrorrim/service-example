import logging.config

import typer
import uvicorn

from app.presentation.bootstrap import bootstrap
from app.presentation.cli import shell
from app.settings import LoggingSettings, VERSION

app = typer.Typer()

app.command("shell", help="Run python shell.")(shell.command)


@app.command("runserver")
def run_server():
    uvicorn.run(
        "app.presentation.api.factory:create_app",
        port=8000,
        factory=True,
        reload=True,
        log_config=None,
    )


@app.command()
def version():
    """Echo the version."""
    typer.echo(f"v{VERSION}")


@app.command("dropdb")
def drop_db():
    """Drop the database."""
    typer.echo("Co ty kurwa robisz?")


def startup():
    container, mediator = bootstrap()
    settings = container.resolve(LoggingSettings)
    logging.config.dictConfig(settings.get_logging_config(is_local=settings.debug))
    app()


if __name__ == "__main__":
    startup()
