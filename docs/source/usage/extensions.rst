.. _extending-confz:

Extending ConfZ
===============

The modular structure of ConfZ with its different sources and loader allow to easily extend it. To do so, you can
define and register your own sources and loaders. Lets assume, we want the current platform and python version in our
config::

    import sys
    from dataclasses import dataclass

    from confz import ConfigSource
    from confz.loaders import Loader, register_loader


    @dataclass
    class CustomSource(ConfigSource):
        platform: str = None    # Write the current platform into a config variable with this name
        version: str = None     # Write the current python version into a config variable with this name


    class CustomLoader(Loader):
        @classmethod
        def populate_config(cls, config: dict, config_source: CustomSource):
            config_update = {
                config_source.platform: sys.platform,
                config_source.version: f"{sys.version_info[0]}.{sys.version_info[1]}"
            }
            cls.update_dict_recursively(config, config_update)


    register_loader(CustomSource, CustomLoader)

Now, any config class can use this new source:

>>> from confz import BaseConfig
>>> class MyConfig(BaseConfig):
...     attr1: str
...     attr2: str

>>> MyConfig(config_sources=CustomSource(
...     platform="attr1",
...     version="attr2"
... ))
MyConfig(attr1='win32' attr2='3.9')

See the documentation of :class:`~confz.loaders.Loader` for helper functions to reuse common functionality while writing
such a loader.
