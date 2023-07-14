from typing import Type, Dict

from confz.config_source import (
    ConfigSource,
    FileSource,
    EnvSource,
    CLArgSource,
    DataSource,
)
from confz.exceptions import ConfigException
from .cl_arg_loader import CLArgLoader
from .data_loader import DataLoader
from .env_loader import EnvLoader
from .file_loader import FileLoader
from .loader import Loader

_loaders: Dict[Type[ConfigSource], Type[Loader]] = {}


def get_loader(config_source: Type[ConfigSource]):
    if config_source in _loaders:
        return _loaders[config_source]
    raise ConfigException(f"Unknown config source type '{config_source}'")


def register_loader(config_source: Type[ConfigSource], loader: Type[Loader]):
    """Register a :class:`~confz.ConfigSource` with a specific loader. Can be used to
    extend `ConfZ` with own loaders.

    :param config_source: The :class:`~confz.ConfigSource` sub-type.
    :param loader: The :class:`~confz.loaders.Loader` sub-type.
    """
    _loaders[config_source] = loader


register_loader(FileSource, FileLoader)
register_loader(EnvSource, EnvLoader)
register_loader(CLArgSource, CLArgLoader)
register_loader(DataSource, DataLoader)
