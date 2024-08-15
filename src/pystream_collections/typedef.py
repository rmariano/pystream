"""Type definitions used in the project."""

from typing import Callable, TypeAlias, TypeVar

T = TypeVar("T")
ReducedType = TypeVar("ReducedType")

Mapper: TypeAlias = Callable[[T], T]
Filter: TypeAlias = Callable[[T], bool]
Reducer: TypeAlias = Callable[[T, T], ReducedType]

Collectable: TypeAlias = list | tuple | dict
TCollectable = type[Collectable]
