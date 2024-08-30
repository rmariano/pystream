# PyStream - A library for managing collections more conveniently

Inspired by other language's features (e.g. Java's streaming API, or JavaScript functional traits on arrays),
this library helps you interact with collections or iterable objects, by easily chaining operations,
and collecting the results at the end (thus, having lazy-evaluation).

Some basic examples:

```python
from pystream.stream import Stream

Stream(2, 3, 5, 7, 11).skip(2).collect()  # [5, 7, 11]
Stream([1, 2, 3]).map(lambda x: x + 1).filter(lambda x: x > 2).collect()  # [3, 4]
```

You can also use the `.reduce()` function to obtain a final result based on a provided transformation function:

```python
>>> stream = Stream(("paris", "london", "stockholm")).map(str.title)
>>> stream.reduce(lambda w1, w2: f"{w1}, {w2}")
"Paris, London, Stockholm"
```

It's also possible to use a specific object to collect the results into (by default is a list). For example, if the
stream consists of key/value pairs, you can collect them into a dictionary:

```python
>>> Stream(("one", 1), ("two", 2), ("forty two", 42))
>>> stream.collect(dict)
{"one": 1, "two": 2, "forty two": 42}
```

## Asynchronous Code
This library supports working with coroutines and asynchronous iterators as well. Working with the built-in `map()`, and
`filter()` functions is great, and also the niceties of the `itertools` module, but there's no counterpart of these
capabilities for asynchronous code.

Instead, this more compact (and functional-like) object is provided, which can work like this:

```python
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

>>> count = (
    await AsyncStream(_get_db_records())
    .filter(lambda locker: locker.is_available)
    .map(lambda locker: locker.size)
    .collect(Counter)
)
{"S": 1, "M": 1, "L": 2}
```

## Motivation
Missing the `itertools`-like capabilities is one of the most annoying things,
when working with asynchronous code.  In addition, adding another interface for
the programmer that allows chaining data structures, similar to how Unix
pipelines work, enables programmers to think more clearly about their programs.
