
class AsyncStream:
    """A streaming object that works asynchronously."""

    def __init__(self, async_iterator) -> None:
        """Initialize the object with an asynchronous iterator (something that requires `... async for ... ` syntax).

        Args:
            async_iterator (AsyncIterator): the original async iterator to wrap
        """
        self._async_iterator = async_iterator


    async def collect(self) -> list:
        """Return the result of the chained operations as a list."""
        return [e async for e in self._async_iterator]
