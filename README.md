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
