"""Tests for stream.py."""

from pystream_collections.stream import Stream


def test_collect_simple_filter():
    """Test collecting with map + filter."""
    assert (res := Stream([1, 2, 3]).map(lambda x: x + 1).filter(lambda x: x > 2).collect()) == [3, 4], res


def test_reduce_string():
    """Test reducing a stream expression."""
    stream = Stream(("paris", "london", "stockholm")).map(str.title)
    assert stream.reduce(lambda w1, w2: f"{w1}, {w2}") == "Paris, London, Stockholm"


def test_reduce_string_skip():
    """Test reducing a stream expression."""
    stream = Stream(("paris", "london", "stockholm")).skip(1).map(str.title)
    assert stream.reduce(lambda w1, w2: f"{w1}, {w2}") == "London, Stockholm"


def test_create_from_variable_length_arguments():
    """The stream object can be created from variable lengths of arguments."""
    assert Stream(1).collect() == [1]
    assert Stream(2, 3, 5, 7, 11).skip(2).collect() == [5, 7, 11]
    assert (res := Stream(range(10)).skip(2).skip(3).collect()) == list(range(5, 10)), res
