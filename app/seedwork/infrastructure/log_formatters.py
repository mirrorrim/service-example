"""Module contains logs formatters."""
from logging import Formatter

from pythonjsonlogger.jsonlogger import JsonFormatter

BUILTIN_ATTRS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
    "status_code",  # custom field
    "request",  # custom field
}


def format_record(record):
    """Moves all additional data in log record to field 'extra_data'."""
    extra_data = {}

    for key, value in record.__dict__.items():
        if key not in BUILTIN_ATTRS:
            extra_data[key] = value

    for key in extra_data:
        record.__dict__.pop(key, None)

    record.__dict__["extra_data"] = (
        "; ".join(f"{key}: {value}" for key, value in extra_data.items())
        if extra_data
        else ""
    )

    return record


class LogsFormatter(Formatter):
    """Formatter for logs."""

    def format(self, record):
        """Format logs."""
        formatted_record = format_record(record)
        return super().format(formatted_record)


class JsonLogsFormatter(JsonFormatter):
    """Formatter for json logs."""

    def format(self, record):
        """Format logs."""
        formatted_record = format_record(record)
        return super().format(formatted_record)
