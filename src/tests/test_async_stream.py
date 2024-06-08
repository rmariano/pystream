import pytest
from pystream_collections.async_stream import AsyncStream


async def _async_generator(n):
    for i in range(n):
        yield i


@pytest.mark.asyncio
@pytest.mark.parametrize("length, expected", ((5, [0, 1, 2, 3, 4]), (0, [])))
async def test_collect_async_iterator(length, expected):
    sut = AsyncStream(_async_generator(length))
    assert await sut.collect() == expected
