from typing import ClassVar

from pydantic import BaseModel

from .confz_source import ConfZSource, populate_config


class ConfZMetaclass(type(BaseModel)):
    """ConfZ Meta Class, inheriting from the pydantic `BaseModel` MetaClass. It would have been cleaner to
    implemented the logic in `__call__` in the ConfZ class itself with `__new__` instead, but pydantic currently
    does not support to overwrite this method."""

    _confz_instances = {}

    def __call__(cls, config_source: ConfZSource = None, **kwargs):
        """Called every time an instance of any ConfZ object is created. Injects the config value population and
        singleton mchanism."""
        if config_source is not None:
            config_raw = kwargs.copy()
            populate_config(config_raw, config_source)
            return super().__call__(**config_raw)

        if cls.CONFIG_SOURCE is not None:
            if cls not in cls._confz_instances:
                config_raw = kwargs.copy()
                populate_config(config_raw, cls.CONFIG_SOURCE)
                cls._confz_instances[cls] = super().__call__(**config_raw)
            return cls._confz_instances[cls]

        return super().__call__(**kwargs)


class ConfZ(BaseModel, metaclass=ConfZMetaclass):
    """ConfZ Base Class, parent of every config class. Internally wraps the pydantic `BaseModel` class and behaves
    transparent except for two cases:
    - If the constructor gets `config_source` as kwarg, it is used to enrich the other kwargs with the sources
    defined in the `ConfZSource` object (files, env-vars, commandline args).
    - If the config class has the class variable `CONFIG_SOURCE` defined, it is used to to enrich the existing kwargs
    with the sources defined in the `ConfZSource` object as above. Additionally, a singleton mechanism is in place
    for this case, returning the same config class instance every time the constructor is called."""

    CONFIG_SOURCE: ClassVar = None
