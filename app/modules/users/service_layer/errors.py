class BaseUserError(Exception):
    """Base user error."""


class UserAlreadyRegistered(BaseUserError):
    """User already registered."""
