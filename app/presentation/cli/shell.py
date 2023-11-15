import IPython
from traitlets.config import Config

c = Config()

c.InteractiveShellApp.exec_lines = [
    "from app.presentation.bootstrap import bootstrap",
    "container, mediator = bootstrap()",
]
c.InteractiveShell.confirm_exit = True
c.TerminalIPythonApp.display_banner = False


def command():
    """Run IPython shell with pre-imported objects."""
    IPython.start_ipython(config=c, argv=[])
