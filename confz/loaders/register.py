from typing import Type, Dict

from confz.confz_source import ConfZSource, ConfZFileSource, ConfZEnvSource, ConfZCLArgSource
from confz.exceptions import ConfZException
from .loader import Loader
from .file_loader import FileLoader
from .env_loader import EnvLoader
from .cl_arg_loader import CLArgLoader


_loaders: Dict[Type[ConfZSource], Type[Loader]] = {}


def get_loader(confz_source: Type[ConfZSource]):
    if confz_source in _loaders:
        return _loaders[confz_source]
    else:
        raise ConfZException(f'Unknown config source type "{confz_source}"')


def register_loader(confz_source: Type[ConfZSource], loader: Type[Loader]):
    """Register a ´ConfZSource´ with a specific loader. Can be used to extend ´ConfZ´ with own loaders.
    :param confz_source: The ´ConfZSource´ sub-type.
    :param loader: The ´Loader´ sub-type.
    """
    _loaders[confz_source] = loader


register_loader(ConfZFileSource, FileLoader)
register_loader(ConfZEnvSource, EnvLoader)
register_loader(ConfZCLArgSource, CLArgLoader)
