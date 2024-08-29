"""Base definition for the interface of a stream object."""

from abc import ABC, abstractmethod
from typing import Self

from pystream_collections.typedef import Filter, Mapper


class BaseStream(ABC):
    """Interface for a stream object."""

    @abstractmethod
    def map(self, mapper_fn: Mapper) -> Self:
        """
        Apply a transformation into the current stage of the stream.

        Args:
        ----
            mapper_fn (Mapper): A unary function that transforms single values.

        Returns:
        -------
            Self: object with the transformation saved.

        """

    @abstractmethod
    def filter(self, filter_fn: Filter) -> Self:
        """
        Add a filter function to the stream at the current stage.

        Args:
        ----
            filter_fn (Filter): A function that takes as an argument a value of
            the type the stream is currently holding, and evaluates to a boolean
            expression.  f(x) -> true/false

        Returns:
        -------
            Self: A reference to the same object, after the filtering function
            has been registered.

        """

    @abstractmethod
    def skip(self, n: int) -> Self:
        """
        Skip the first <n> values from the stream.

        Args:
        ----
            n (int): The number of elements to skip.

        Returns:
        -------
            Self: A reference to the same object, with the function registered.

        """
