import asyncio
from functools import partial, wraps
from typing import Callable


def async_command(func: Callable):
    """Run async command"""

    @wraps(func)
    def _inner(*args, **kwargs):
        asyncio.run(partial(func, *args, **kwargs)())

    return _inner
