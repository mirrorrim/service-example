class RepositoryError(Exception):
    """Base repository error."""


class DuplicateKeyError(RepositoryError):
    """Duplicate key error."""
