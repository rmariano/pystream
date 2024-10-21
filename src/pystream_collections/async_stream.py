"""Async version of the Stream."""

from typing import AsyncIterator, Callable, Self

from pystream_collections.base import BaseStream
from pystream_collections.typedef import Collectable, Filter, Mapper, Reducer

from .enums import OperationType

_NOT_SET = object()


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
        self._is_closed = False

    def _validate_is_not_closed(self) -> None:
        if self._is_closed:
            raise ValueError("Stream is closed and cannot be further chained")

    def _close(self) -> None:
        self._is_closed = True

    def map(self, mapper_fn: Mapper) -> Self:
        """Add a mapper function to this stream."""
        self._validate_is_not_closed()
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
        self._validate_is_not_closed()
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
        self._validate_is_not_closed()
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

    async def _collect(self) -> AsyncIterator:
        values = self._async_iterator
        for op_type, tx_function in self._transformations:
            if op_type == OperationType.MAP:
                values = _map(tx_function, values)
            elif op_type == OperationType.FILTER:
                values = _filter(tx_function, values)
            elif op_type == OperationType.SKIP:
                values = self._skip(tx_function, values)
        return values

    async def collect[TCollectable](self, collectable_type: type[Collectable] = list) -> Collectable:
        """Return the result of the chained operations as a list."""
        self._validate_is_not_closed()
        values = await self._collect()
        self._close()
        return collectable_type([e async for e in values])

    async def reduce(self, reducer_fn: Reducer, initial: object = _NOT_SET) -> object:
        """
        Reduce the stream to a final value based on the provided operation.

        The reducer function takes two arguments and resolves into a single value. This function is used to apply
        the reduction over the values the stream has so far.

        This action is FINAL, meaning the stream returns a value after this call and cannot be further chained upon.

        Args:
        ----
            reducer_fn (Reducer): A function like f(x, y) = z where x, y, and z
                are all of the same type, and the result (z) is used as the input of
                the second pair-wise in the iteration.

                For example a stream of (x0, x1, x2) with reducer function f,
                would be computed as: f(f(x0, x1), x2)
            initial: An initial value where to start the reduction from.

        Returns:
        -------
            object: The final reduced value.

        """
        self._validate_is_not_closed()
        collected = await self._collect()
        value = _NOT_SET if initial is _NOT_SET else initial
        async for element in collected:
            if value is _NOT_SET:
                value = element
            value = reducer_fn(value, element)
        if value is _NOT_SET:
            raise TypeError("Cannot reduce with an empty async iterator and no initial value.")
        self._close()
        return value
