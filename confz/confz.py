from __future__ import annotations  # for sphinx's autodoc_type_aliases

from contextlib import AbstractContextManager
from typing import ClassVar, List, Optional, Any

from pydantic import BaseModel

from .change import SourceChangeManager
from .confz_source import ConfZSources
from .exceptions import ConfZException
from .loaders import get_loader


def _load_config(config_kwargs: dict, confz_sources: ConfZSources) -> dict:
    config = config_kwargs.copy()
    if isinstance(confz_sources, list):
        for confz_source in confz_sources:
            loader = get_loader(type(confz_source))
            loader.populate_config(config, confz_source)
    else:
        loader = get_loader(type(confz_sources))
        loader.populate_config(config, confz_sources)
    return config


# Metaclass of pydantic.BaseModel is not in __all__, so use type(BaseModel).
# ConfZ will be only class with this meta class.
# Both of these things confuse mypy and pylint, so had to disable multiple times.
class ConfZMetaclass(type(BaseModel)):  # type: ignore
    """ConfZ Meta Class, inheriting from the pydantic `BaseModel` MetaClass."""

    # pylint: disable=no-self-argument,no-member
    def __call__(cls, config_sources: Optional[ConfZSources] = None, **kwargs):
        """Called every time an instance of any ConfZ object is created. Injects the
        config value population and singleton mechanism."""
        if config_sources is not None:
            config = _load_config(kwargs, config_sources)
            return super().__call__(**config)

        if cls.CONFIG_SOURCES is not None:  # type: ignore
            # pylint: disable=access-member-before-definition
            # pylint: disable=attribute-defined-outside-init
            if len(kwargs) > 0:
                raise ConfZException(
                    'Singleton mechanism enabled ("CONFIG_SOURCES" is defined), so '
                    "keyword arguments are not supported"
                )
            if cls.confz_instance is None:  # type: ignore
                config = _load_config(kwargs, cls.CONFIG_SOURCES)  # type: ignore
                cls.confz_instance = super().__call__(**config)
            return cls.confz_instance

        return super().__call__(**kwargs)


class ConfZ(BaseModel, metaclass=ConfZMetaclass):
    """Base class, parent of every config class. Internally wraps :class:`BaseModel`of
    pydantic and behaves transparent except for two cases:

    - If the constructor gets `config_sources` as kwarg, these sources are used as
      input to enrich the other kwargs.
    - If the class has the class variable `CONFIG_SOURCES` defined, these sources are
      used as input.

    In the latter case, a singleton mechanism is activated, returning the same config
    class instance every time the constructor is called."""

    CONFIG_SOURCES: ClassVar[Optional[ConfZSources]] = None  #: Sources to use as input.

    # type is ClassVar[Optional["ConfZ"]] (pydantic throws error with forward ref)
    confz_instance: ClassVar[Optional[Any]] = None  #: *for internal use only*

    # type is ClassVar[Optional[List["Listener"]]] (same here)
    listeners: ClassVar[Optional[List[Any]]] = None  #: *for internal use only*

    class Config:
        allow_mutation = False

    @classmethod
    def change_config_sources(
        cls, config_sources: ConfZSources
    ) -> AbstractContextManager:
        """Change the `CONFIG_SOURCES` class variable within a controlled context.
        Within this context, the sources will be different and the singleton reset.
        This can be useful in unit tests to temporarily change a configuration.

        :param config_sources: The temporary config sources for within the context.
        :return: Context manager for change of config sources.
        """
        return SourceChangeManager(cls, config_sources)
