from typing import ClassVar

from pydantic import BaseModel

from .zconfig_source import ZConfigSource, populate_config


class ZConfigMetaclass(type(BaseModel)):
    """ZConfig Meta Class, inheriting from the pydantic `BaseModel` MetaClass. It would have been cleaner to
    implemented the logic in `__call__` in the ZConfig class itself with `__new__` instead, but pydantic currently
    does not support to overwrite this method."""

    _zconfig_instances = {}

    def __call__(cls, config_source: ZConfigSource = None, **kwargs):
        """Called every time an instance of any ZConfig object is created. Injects the config value population and
        singleton mchanism."""
        if config_source is not None:
            config_raw = kwargs.copy()
            populate_config(config_raw, config_source)
            return super().__call__(**config_raw)

        if cls.CONFIG_SOURCE is not None:
            if cls not in cls._zconfig_instances:
                config_raw = kwargs.copy()
                populate_config(config_raw, cls.CONFIG_SOURCE)
                cls._zconfig_instances[cls] = super().__call__(**config_raw)
            return cls._zconfig_instances[cls]

        return super().__call__(**kwargs)


class ZConfig(BaseModel, metaclass=ZConfigMetaclass):
    """ZConfig Base Class, parent of every config class. Internally wraps the pydantic `BaseModel` class and behaves
    transparent except for two cases:
    - If the constructor gets `config_source` as kwarg, it is used to enrich the other kwargs with the sources
    defined in the `ZConfigSource` object (files, env-vars, commandline args).
    - If the config class has the class variable `CONFIG_SOURCE` defined, it is used to to enrich the existing kwargs
    with the sources defined in the `ZConfigSource` object as above. Additionally, a singleton mechanism is in place
    for this case, returning the same config class instance every time the constructor is called."""

    CONFIG_SOURCE: ClassVar = None
