from enum import Enum


class OperationType(Enum):
    MAP = "map"
    FILTER = "filter"
    REDUCE = "reduce"
    SKIP = "skip"
