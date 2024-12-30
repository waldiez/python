"""Import position enum."""

from enum import Enum


class ImportPosition(Enum):
    """Import position.

    Attributes
    ----------
    BUILTINS : int
        The top of the import (builtins)
    THIRD_PARTY : int
        The third party imports.
    LOCAL : int
        The local imports.
    """

    BUILTINS = 0
    THIRD_PARTY = 1
    LOCAL = 2