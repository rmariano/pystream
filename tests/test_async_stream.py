"""Test the asynchronous implementation."""

from typing import AsyncGenerator

import pytest
from pystream_collections import AsyncStream


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
