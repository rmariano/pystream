from pystream.stream import Stream


def test_collect_simple_filter():
    assert (res := Stream([1, 2, 3]).map(lambda x: x + 1).filter(lambda x: x > 2).collect()) == [3, 4], res


def test_reduce_string():
    assert (
        res := Stream(("paris", "london", "stockholm")).map(str.title).reduce(lambda w1, w2: f"{w1}, {w2}").collect()
    ) == "Paris, London, Stockholm", res


def test_create_from_variable_length_arguments():
    assert Stream(1).collect() == [1]
    assert Stream(2, 3, 5, 7, 11).skip(2).collect() == [5, 7, 11]
    assert (res := Stream(range(10)).skip(2).skip(3).collect()) == list(range(5, 10)), res
