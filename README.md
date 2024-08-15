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
