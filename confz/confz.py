from typing import ClassVar

from pydantic import BaseModel

from .confz_source import ConfZSources
from .loader import load_config


class ConfZMetaclass(type(BaseModel)):
    """ConfZ Meta Class, inheriting from the pydantic `BaseModel` MetaClass. It would have been cleaner to
    implemented the logic in `__call__` in the ConfZ class itself with `__new__` instead, but pydantic currently
    does not support to overwrite this method."""

    _confz_instances = {}

    def __call__(cls, config_sources: ConfZSources = None, **kwargs):
        """Called every time an instance of any ConfZ object is created. Injects the config value population and
        singleton mchanism."""
        if config_sources is not None:
            config = load_config(kwargs, config_sources)
            return super().__call__(**config)

        if cls.CONFIG_SOURCES is not None:
            if cls not in cls._confz_instances:
                config = load_config(kwargs, cls.CONFIG_SOURCES)
                cls._confz_instances[cls] = super().__call__(**config)
            return cls._confz_instances[cls]

        return super().__call__(**kwargs)


class ConfZ(BaseModel, metaclass=ConfZMetaclass):
    """ConfZ Base Class, parent of every config class. Internally wraps the pydantic `BaseModel` class and behaves
    transparent except for two cases:
    - If the constructor gets `config_source` as kwarg, it is used to enrich the other kwargs with the sources
    defined in the `ConfZSource` object (files, env-vars, commandline args).
    - If the config class has the class variable `CONFIG_SOURCE` defined, it is used to to enrich the existing kwargs
    with the sources defined in the `ConfZSource` object as above. Additionally, a singleton mechanism is in place
    for this case, returning the same config class instance every time the constructor is called.
    Additionally, the object is faux-immutable per default."""

    CONFIG_SOURCES: ClassVar[ConfZSources] = None

    class Config:
        allow_mutation = False
