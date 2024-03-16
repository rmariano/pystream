from typing import Self
from enum import Enum
from functools import reduce
from itertools import islice


class OperationType(Enum):
    MAP = "map"
    FILTER = "filter"
    REDUCE = "reduce"
    SKIP = "skip"


def _is_iterable(value) -> bool:
    try:
        iter(value)
        return True
    except TypeError:
        return False


def _parse_stream_parameters(*values):
    if len(values) == 1:
        (sole_parameter,) = values
        if _is_iterable(sole_parameter):
            return iter(sole_parameter)
        return (sole_parameter,)
    return values


class Stream:
    def __init__(self, *values) -> None:
        self._wrapped = _parse_stream_parameters(*values)
        self._transformations = []
        self._is_reduced = False

    def map(self, fn) -> Self:
        self._transformations.append((OperationType.MAP, fn))
        return self

    def filter(self, fn) -> Self:
        self._transformations.append((OperationType.FILTER, fn))
        return self

    def reduce(self, fn) -> Self:
        self._transformations.append((OperationType.REDUCE, fn))
        self._is_reduced = True
        return self

    def skip(self, n: int) -> Self:
        def fn(list_of_values: list):
            return islice(list_of_values, n, None)

        self._transformations.append((OperationType.SKIP, fn))
        return self

    def _reducer(self, values, operation_type: OperationType, transformation):
        match operation_type:
            case OperationType.MAP:
                return map(transformation, values)
            case OperationType.FILTER:
                return filter(transformation, values)
            case OperationType.REDUCE:
                return reduce(transformation, values)
            case OperationType.SKIP:
                return transformation(values)
            case _:
                raise ValueError("Operation not supported")

    def collect(self):
        result = self._wrapped
        for op_type, tx in self._transformations:
            result = self._reducer(result, op_type, tx)
        if self._is_reduced:
            return result
        return list(result)
