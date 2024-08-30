"""Definitions for the abstractions of Stream over regular iterators."""

import functools
from itertools import islice
from typing import Callable, Iterable, Self

from pystream_collections.base import BaseStream
from pystream_collections.enums import OperationType
from pystream_collections.typedef import Collectable, Filter, Mapper, Reducer

_NOT_SET = object()


def _is_iterable(value: Iterable) -> bool:
    try:
        iter(value)
        return True
    except TypeError:
        return False


def _parse_stream_parameters(*values) -> Iterable:
    if len(values) == 1:
        (sole_parameter,) = values
        if _is_iterable(sole_parameter):
            return iter(sole_parameter)
        return (sole_parameter,)
    return values


class Stream(BaseStream):
    """Define a stream to be used with regular synchronous iterator operations."""

    def __init__(self, *values) -> None:
        """Initialize with a sequence of values."""
        self._wrapped = _parse_stream_parameters(*values)
        self._transformations = []

    def map(self, mapper_fn: Mapper) -> Self:
        """
        Add a transformation function to the stream to be later processed.

        Provide a mapper function that will transform an individual value.
        """
        self._transformations.append((OperationType.MAP, mapper_fn))
        return self

    def filter(self, filter_fn: Filter) -> Self:
        """

        Pass a filtering function to exclude values from this step of the stream onwards.

        The function should evaluate to a boolean value.
        """
        self._transformations.append((OperationType.FILTER, filter_fn))
        return self

    def reduce[T](self, reducer_fn: Reducer, initial: T = _NOT_SET) -> object:
        """
        Reduce the stream to a final value based on the provided operation.

        The reducer function takes two arguments and resolves into a single value. This function is used to apply
        the reduction over the values the stream has so far.

        This action is FINAL, meaning the stream returns a value after this call and cannot be further chained upon.
        """
        transformations = self._apply_transformations()
        if initial is _NOT_SET:
            return functools.reduce(reducer_fn, transformations)
        return functools.reduce(reducer_fn, transformations, initial)

    def skip(self, n: int) -> Self:
        """Skip <n> elements from the current stream."""

        def fn(list_of_values: Iterable) -> Iterable:
            return islice(list_of_values, n, None)

        self._transformations.append((OperationType.SKIP, fn))
        return self

    def _reducer(self, values: Iterable, operation_type: OperationType, transformation: Callable) -> Iterable:
        match operation_type:
            case OperationType.MAP:
                return map(transformation, values)
            case OperationType.FILTER:
                return filter(transformation, values)
            case OperationType.SKIP:
                return transformation(values)
            case _:
                raise ValueError("Operation not supported")

    def _apply_transformations(self) -> Iterable:
        result = self._wrapped
        for op_type, tx in self._transformations:
            result = self._reducer(result, op_type, tx)
        return result

    def collect[TCollectable](self, collectable_type: type[Collectable] = list) -> Collectable:
        """Return the all processed values (based on previous operation) into a final collectable (by default list)."""
        result = self._apply_transformations()
        return collectable_type(result)
