"""Test the asynchronous implementation."""

import operator
from collections import Counter
from typing import AsyncGenerator, NamedTuple

import pytest
from pystream_collections import AsyncStream
from pystream_collections.typedef import Collectable


async def _async_generator(n: int, start: int = 0) -> AsyncGenerator[int, None]:
    for i in range(start, n):
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


@pytest.mark.asyncio
async def test_skip() -> None:
    """Skip some elements from the async stream iterator."""
    astream_1 = AsyncStream(_async_generator(5)).skip(3)
    astream_2 = AsyncStream(_async_generator(5)).skip(5)
    astream_3 = AsyncStream(_async_generator(5)).skip(0).skip(10).skip(0).skip(3)
    astream_4 = AsyncStream(_async_generator(2)).skip(0)

    assert await astream_1.collect() == [3, 4], "Skip some elements"
    assert await astream_2.collect() == [], "Expected skipping all elements to yield empty."
    assert await astream_3.collect() == [], "Chained skip should work"
    assert await astream_4.collect() == [0, 1], "No skipping should work"


@pytest.mark.asyncio
async def test_skip_map() -> None:
    """First skip, then map."""
    astream = AsyncStream(_async_generator(5)).skip(3).map(lambda x: x + 1)
    assert await astream.collect() == [4, 5]


@pytest.mark.asyncio
async def test_map_skip() -> None:
    """First map, then skip."""
    astream = AsyncStream(_async_generator(5)).map(str).skip(4)
    assert await astream.collect() == ["4"]


@pytest.mark.asyncio
async def test_skip_filter() -> None:
    """Filter, then skip."""
    astream_empty = AsyncStream(_async_generator(5)).filter(lambda x: x > 99).skip(0)
    astream_one = AsyncStream(_async_generator(3)).filter(bool).skip(1)

    assert await astream_empty.collect() == []
    assert await astream_one.collect() == [2]


@pytest.mark.asyncio
async def test_filter_skip() -> None:
    """Skip, then filter."""
    astream_empty = AsyncStream(_async_generator(5)).skip(9).filter(lambda _: True)
    astream_one = AsyncStream(_async_generator(3)).skip(1).filter(lambda x: x > 1)

    assert await astream_empty.collect() == []
    assert await astream_one.collect() == [2]


@pytest.mark.asyncio
async def test_reduce() -> None:
    """Return the final value, based on a function."""
    assert await AsyncStream(_async_generator(11)).reduce(operator.add) == 55, "sum(0..10) == 55"
    assert await AsyncStream(_async_generator(10)).reduce(operator.mul) == 0
    assert await AsyncStream(_async_generator(5, start=1)).reduce(operator.mul) == 24, "4! == 24"


@pytest.mark.asyncio
async def test_reduce_initial_value() -> None:
    """Test reducing a stream with different initial values."""
    assert await AsyncStream(_async_generator(4)).reduce(operator.add, initial=0) == 6
    assert await AsyncStream(_async_generator(2, start=1)).reduce(operator.add, initial=99) == 100
    assert await AsyncStream(_async_generator(0)).reduce(operator.add, initial=1) == 1


@pytest.mark.asyncio
async def test_reduce_empty() -> None:
    """Reduce cannot be done if there're no values and not initial (default) value."""
    with pytest.raises(TypeError):
        await AsyncStream(_async_generator(0)).reduce(operator.mul)


@pytest.mark.asyncio
async def test_all_methods_then_collect() -> None:
    """Combine multiple chained operations, and then do a final collect."""

    class Locker(NamedTuple):
        name: str
        size: str
        is_available: bool

    async def _get_db_records() -> AsyncGenerator:
        yield Locker("park street 1", "L", False)
        yield Locker("Union street", "S", True)
        yield Locker("Main Square 12", "M", False)
        yield Locker("Central Station", "M", True)
        yield Locker("Central Station2", "L", True)
        yield Locker("Central Station3", "L", True)

    count = (
        await AsyncStream(_get_db_records())
        .filter(lambda locker: locker.is_available)
        .map(lambda locker: locker.size)
        .collect(Counter)
    )
    assert count == {"S": 1, "M": 1, "L": 2}


@pytest.mark.asyncio
async def test_api_reduce() -> None:
    """Chain several methods, then reduce."""
    stream = AsyncStream(_async_generator(100)).filter(lambda x: x == 0 or x >= 90).map(str).skip(1)
    result = await stream.reduce(operator.add, initial="Numbers: ")
    assert result == "Numbers: 90919293949596979899"
