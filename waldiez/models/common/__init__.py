"""Common utils for all models."""

from datetime import datetime, timezone

from .base import WaldiezBase
from .method_utils import check_function, generate_function, parse_code_string


def now() -> str:
    """Get the current date and time in UTC.

    Returns
    -------
    str
        The current date and time in UTC.
    """
    return (
        datetime.now(tz=timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )


__all__ = [
    "WaldiezBase",
    "now",
    "check_function",
    "generate_function",
    "parse_code_string",
]
