from typing import Self

from pystream_collections.operation_type import OperationType


class AsyncStream:
    """A streaming object that works asynchronously."""

    def __init__(self, async_iterator) -> None:
        """Initialize the object with an asynchronous iterator (something that requires `... async for ... ` syntax).

        Args:
            async_iterator (AsyncIterator): the original async iterator to wrap
        """
        self._async_iterator = async_iterator
        self._transformations = []

    def map(self, fn) -> Self:
        self._transformations.append((OperationType.MAP, fn))
        return self

    # def filter(self, fn) -> Self:
    #     self._transformations.append((OperationType.FILTER, fn))
    #     return self

    # def reduce(self, fn) -> Self:
    #     self._transformations.append((OperationType.REDUCE, fn))
    #     self._is_finished = True
    #     return self

    # def skip(self, n: int) -> Self:
    #     def fn(list_of_values: list):
    #         return islice(list_of_values, n, None)

    #     self._transformations.append((OperationType.SKIP, fn))
    #     return self
    async def _map(self, values, transformation):
        async for value in values:
            yield transformation(value)

    async def _reducer(self, values, operation_type: OperationType, transformation):
        match operation_type:
            case OperationType.MAP:
                return await self._map(values, transformation)
            case _:
                raise ValueError("Operation not supported")

    async def collect(self) -> list:
        """Return the result of the chained operations as a list."""
        result = self._async_iterator
        for op_type, tx in self._transformations:
            result = self._reducer(result, op_type, tx)

        return [e async for e in result]
