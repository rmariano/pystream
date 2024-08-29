"""Async version of the Stream."""

from typing import AsyncIterator, Callable, Self

from pystream_collections.base import BaseStream
from pystream_collections.typedef import Collectable, Filter, Mapper

from .enums import OperationType


async def _map(mapper_fn: Mapper, values: AsyncIterator) -> AsyncIterator:
    async for e in values:
        yield mapper_fn(e)


async def _filter(filter_fn: Filter, values: AsyncIterator) -> AsyncIterator:
    async for e in values:
        if filter_fn(e):
            yield e


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

    def skip(self, n: int) -> Self:
        """
        Skip <n> elements from this asynchronous stream iterator.

        Args:
        ----
            n (int): The number of the first elements to skip.

        Returns:
        -------
            Self: A reference to this same object, with the skip registered.

        """
        self._transformations.append((OperationType.SKIP, lambda i: i < n))
        return self

    async def _skip(self, tx_function: Callable[[int], bool], values: AsyncIterator) -> AsyncIterator:
        """
        Return the <values> from the original iterator with the first N elements skipped.

        This is determined by the applied function <tx_function>.

        Args:
        ----
            tx_function (callable[[int], bool]): A function to evaluate over
                every Nth element on the iteration to determine if it needs to be
                skipped or not.
            values (AsyncIterator): The original values in the async iterator.

        Returns:
        -------
            AsyncIterator: The reduced async iterator.

        """
        index = 0
        async for e in values:
            if not tx_function(index):
                yield e
            index += 1

    async def collect[TCollectable](self, collectable_type: type[Collectable] = list) -> Collectable:
        """Return the result of the chained operations as a list."""
        values = self._async_iterator
        for op_type, tx_function in self._transformations:
            if op_type == OperationType.MAP:
                values = _map(tx_function, values)
            elif op_type == OperationType.FILTER:
                values = _filter(tx_function, values)
            elif op_type == OperationType.SKIP:
                values = self._skip(tx_function, values)

        return collectable_type([e async for e in values])
