"""Async version of the Stream."""

from typing import AsyncIterator, Self

from pystream_collections.base import BaseStream
from pystream_collections.typedef import Collectable, Filter, Mapper

from .enums import OperationType


class AsyncStream(BaseStream):
    """A streaming object that works asynchronously."""

    def __init__(self, async_iterator: AsyncIterator) -> None:
        """
        Initialize the object with an asynchronous iterator (something that requires `... async for ... ` syntax).

        Args:
        ----
            async_iterator (AsyncIterator): the original async iterator to wrap

        """
        self._async_iterator = async_iterator
        self._transformations = []

    def map(self, mapper_fn: Mapper) -> Self:
        """Add a mapper function to this stream."""
        self._transformations.append((OperationType.MAP, mapper_fn))
        return self

    def filter(self, filter_fn: Filter) -> Self:
        """
        Register a filtering function into this stream.

        Args:
        ----
            filter_fn (Filter): A function that evaluates to a boolean.

        Returns:
        -------
            Self: A reference to this same object, with the filter registered.

        """
        self._transformations.append((OperationType.FILTER, filter_fn))
        return self

    async def collect[TCollectable](self, collectable_type: type[Collectable] = list) -> Collectable:
        """Return the result of the chained operations as a list."""
        values = [v async for v in self._async_iterator]
        for op_type, tx_function in self._transformations:
            if op_type == OperationType.MAP:
                values = map(tx_function, values)
            if op_type == OperationType.FILTER:
                values = filter(tx_function, values)
        return collectable_type(values)
