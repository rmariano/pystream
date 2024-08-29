"""Test the asynchronous implementation."""

from typing import AsyncGenerator

import pytest
from pystream_collections import AsyncStream
from pystream_collections.typedef import Collectable


async def _async_generator(n: int) -> AsyncGenerator[int, None]:
    for i in range(n):
        yield i


@pytest.mark.asyncio
@pytest.mark.parametrize("length, expected", ((5, [0, 1, 2, 3, 4]), (0, [])))
async def test_collect_async_iterator(length: int, expected: list) -> None:
    """Simply gather an asynchronous iterator into a list (no transformations applied)."""
    sut = AsyncStream(_async_generator(length))
    assert await sut.collect() == expected


@pytest.mark.asyncio
async def test_map() -> None:
    """Test the results with a transformation applied."""
    sut = AsyncStream(_async_generator(10)).map(lambda x: x * 10)
    assert await sut.collect() == [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]


@pytest.mark.asyncio
async def test_chained_map() -> None:
    """Test the results with more than one transformations applied."""
    sut = AsyncStream(_async_generator(10)).map(lambda x: x * 10).map(lambda x: x + 1)
    assert await sut.collect() == [1, 11, 21, 31, 41, 51, 61, 71, 81, 91]


@pytest.mark.parametrize(
    "collectable_type, expected",
    (
        (list, ["first", "second", "third"]),
        (tuple, ("first", "second", "third")),
        (set, {"first", "second", "third"}),
    ),
)
@pytest.mark.asyncio
async def test_collect_different_containers(collectable_type: type[Collectable], expected: Collectable) -> None:
    """Collecting the values using the <collectable_type> should return the <expected>."""

    async def _stream() -> AsyncGenerator[str, None]:
        yield "first"
        yield "second"
        yield "third"

    stream = AsyncStream(_stream())
    assert await stream.collect(collectable_type) == expected


@pytest.mark.asyncio
async def test_filter() -> None:
    """Filter results."""
    async_stream = AsyncStream(_async_generator(10)).filter(lambda x: x > 5)
    result = await async_stream.collect()
    assert result == [6, 7, 8, 9]


@pytest.mark.asyncio
async def test_chained_filter() -> None:
    """Filter results, multiple times."""
    async_stream = AsyncStream(_async_generator(10)).filter(lambda x: x > 5).filter(lambda x: x % 2 == 0)
    result = await async_stream.collect()
    assert result == [6, 8]


@pytest.mark.asyncio
async def test_filter_map() -> None:
    """First filter, then map."""
    async_stream = AsyncStream(_async_generator(10)).filter(lambda x: x > 5).map(lambda x: x % 2)
    result = await async_stream.collect()
    assert result == [0, 1, 0, 1]


@pytest.mark.asyncio
async def test_map_filter() -> None:
    """First map, then filter."""
    async_stream = AsyncStream(_async_generator(10)).map(lambda x: x % 5).filter(bool)
    result = await async_stream.collect()
    assert result == [1, 2, 3, 4, 1, 2, 3, 4]
