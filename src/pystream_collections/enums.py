"""Enumerations used in this project."""

from enum import Enum


class OperationType(Enum):
    """Supported Operation Types."""

    MAP = "map"
    FILTER = "filter"
    REDUCE = "reduce"
    SKIP = "skip"
