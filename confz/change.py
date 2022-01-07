import inspect
from contextlib import AbstractContextManager
from typing import (
    Type,
    Callable,
    Any,
    List,
    Dict,
    TypeVar,
    Generic,
    Optional,
    TYPE_CHECKING,
)

from .confz_source import ConfZSources

if TYPE_CHECKING:
    from .confz import ConfZ


class SourceChangeManager(AbstractContextManager):
    """Config sources change context manager, allows to change config sources within a
    controlled context and resets everything afterwards."""

    def __init__(self, config_class: Type["ConfZ"], config_sources: ConfZSources):
        self._config_class = config_class
        self._config_sources = config_sources
        self._backup_instance = None
        self._backup_sources = None

    def __enter__(self):
        self._backup_instance = self._config_class.confz_instance
        self._config_class.confz_instance = None

        self._backup_sources = self._config_class.CONFIG_SOURCES
        self._config_class.CONFIG_SOURCES = self._config_sources

        if self._config_class.listeners is not None:
            for listener in self._config_class.listeners:
                listener.change_enter(self)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._config_class.confz_instance = self._backup_instance
        self._config_class.CONFIG_SOURCES = self._backup_sources

        if self._config_class.listeners is not None:
            for listener in self._config_class.listeners:
                listener.change_exit(self)


T = TypeVar("T")


class Listener(Generic[T]):
    """Listener of config, will add singleton mechanism, aware of config changes."""

    def __init__(self, fn: Callable[[], T], config_classes: List[Type["ConfZ"]]):
        if len(inspect.getfullargspec(fn).args) != 0:
            raise ValueError("Callable should not take any arguments")

        for config_class in config_classes:
            if config_class.listeners is None:
                config_class.listeners = []
            config_class.listeners.append(self)

        self._fn = fn
        self._instance: Optional[T] = None
        self._backup_instances: Dict[SourceChangeManager, T] = {}

    @property
    def is_async(self):
        return inspect.iscoroutinefunction(self._fn)

    def __call__(self):
        if self.is_async:

            async def inner():
                if self._instance is None:
                    self._instance = await self._fn()
                return self._instance

        else:

            def inner():
                if self._instance is None:
                    self._instance = self._fn()
                return self._instance

        return inner()

    def change_enter(self, context):
        self._backup_instances[context] = self._instance
        self._instance = None

    def change_exit(self, context):
        self._instance = self._backup_instances[context]
        del self._backup_instances[context]


def depends_on(*args):
    """Decorator to transform a function into a singleton and register it to a set of
    config classes."""
    if len(args) == 1 and inspect.isfunction(args[0]):
        return Listener(args[0], [])

    def inner(fn: Callable[[], Any]) -> Listener:
        return Listener(fn, list(args))

    return inner
