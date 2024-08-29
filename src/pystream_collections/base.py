"""Base definition for the interface of a stream object."""

from abc import ABC, abstractmethod
from typing import Self

from pystream_collections.typedef import Mapper


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
