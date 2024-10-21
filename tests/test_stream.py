"""Tests for stream.py."""

import operator

import pytest

from pystream_collections import Stream
from pystream_collections.typedef import Collectable


def test_collect_simple_filter() -> None:
    """Test collecting with map + filter."""
    assert (res := Stream([1, 2, 3]).map(lambda x: x + 1).filter(lambda x: x > 2).collect()) == [3, 4], res


def test_reduce_string() -> None:
    """Test reducing a stream expression."""
    stream = Stream(("paris", "london", "stockholm")).map(str.title)
    assert stream.reduce(lambda w1, w2: f"{w1}, {w2}") == "Paris, London, Stockholm"


def test_reduce_initial_value() -> None:
    """Test reducing a stream with different initial values."""
    assert Stream(1, 2, 3).reduce(operator.add, initial=0) == 6
    assert Stream(1).reduce(operator.add, initial=99) == 100
    assert Stream().reduce(operator.add, initial=1) == 1


def test_reduce_empty() -> None:
    """Reduce cannot be done if there're no values and not initial (default) value."""
    with pytest.raises(TypeError):
        Stream().reduce(operator.mul)

def test_reduce_string_skip() -> None:
    """Test reducing a stream expression."""
    stream = Stream(("paris", "london", "stockholm")).skip(1).map(str.title)
    assert stream.reduce(lambda w1, w2: f"{w1}, {w2}") == "London, Stockholm"


def test_create_from_variable_length_arguments() -> None:
    """The stream object can be created from variable lengths of arguments."""
    assert Stream(1).collect() == [1]
    assert Stream(2, 3, 5, 7, 11).skip(2).collect() == [5, 7, 11]
    assert (res := Stream(range(10)).skip(2).skip(3).collect()) == list(range(5, 10)), res


@pytest.mark.parametrize(
    "collectable_type, expected",
    (
        (list, ["first", "second", "third"]),
        (tuple, ("first", "second", "third")),
    ),
)
def test_collect_list_tuple(collectable_type: type[Collectable], expected: Collectable) -> None:
    """Collecting the values using the <collectable_type> should return the <expected>."""
    stream = Stream("first", "second", "third")
    assert stream.collect(collectable_type) == expected


def test_collect_dict() -> None:
    """Can use a dict to gather the <key,value> pairs."""
    stream = Stream(("one", 1), ("two", 2), ("forty two", 42))
    expected = {"one": 1, "two": 2, "forty two": 42}
    assert stream.collect(dict) == expected


class TestStreamClosed:
    """
    Test stream is closed.

    After any of the final operations has been called (e.g collect(), reduce()),
    the stream can't be used anymore, so calling any other operation, should raise
    an exception.
    """

    def test_collect_closes_the_stream(self) -> None:
        """Once .collect() is invoked, nothing else can be called."""
        stream = Stream(1, 2, 3)
        assert stream.collect() == [1, 2, 3]

        with pytest.raises(ValueError):
            stream.map(lambda x: x + 1)
        with pytest.raises(ValueError):
            stream.filter(lambda x: x > 1)
        with pytest.raises(ValueError):
            stream.skip(1)
        with pytest.raises(ValueError):
            stream.reduce(operator.add)
        with pytest.raises(ValueError):
            stream.collect()


    def test_reduce_closes_the_stream(self) -> None:
        """Once .reduce() is invoked, nothing else can be called."""
        stream = Stream(1, 2, 3)
        assert stream.reduce(operator.add) == 6

        with pytest.raises(ValueError):
            stream.map(lambda x: x + 1)
        with pytest.raises(ValueError):
            stream.filter(lambda x: x > 1)
        with pytest.raises(ValueError):
            stream.skip(1)
        with pytest.raises(ValueError):
            stream.reduce(operator.mul)
        with pytest.raises(ValueError):
            stream.collect()
