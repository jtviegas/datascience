import abc
import os
from typing import Any, Dict, Optional


class SourceException(Exception):
    pass


class NoSourceException(SourceException):
    pass


class SourceInterface(metaclass=abc.ABCMeta):
    """
    def get(self, context: Optional[Dict[str, Any]] = None) -> Any:
        raise NotImplementedError()
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, "get") and callable(subclass.get) or NotImplemented


@SourceInterface.register
class Source(abc.ABC):
    """abstract class defining a method 'get' to manage retrieval of data from somewhere as defined by implementing classes"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self._config = config

    @abc.abstractmethod
    def get(self, context: Optional[Dict[str, Any]] = None) -> Any:
        raise NotImplementedError()

    def _get_param(
        self,
        key: str,
        map: Optional[Dict[str, Any]] = None,
        default: Optional[Any] = None,
    ) -> Any:
        value = None
        if map is not None:
            value = map.get(key)
        if value is None:
            value = os.environ.get(key)
        if value is None:
            if default is not None:
                value = default
            else:
                raise ValueError(
                    f"{key} parameter not found neither in environment nor in provided configuration"
                )
        return value
