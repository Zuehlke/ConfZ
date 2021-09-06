from ..confz_source import ConfZSources, ConfZSource, ConfZFileSource, ConfZEnvSource
from ..exceptions import ConfZException
from .file_loader import FileLoader
from .env_loader import EnvLoader


def _populate_config(config: dict, confz_source: ConfZSource):
    if isinstance(confz_source, ConfZFileSource):
        FileLoader.populate_config(config, confz_source)
    elif isinstance(confz_source, ConfZEnvSource):
        EnvLoader.populate_config(config, confz_source)
    else:
        raise ConfZException(f'Unknown config source type "{type(confz_source)}"')


def load_config(config_kwargs: dict, confz_sources: ConfZSources) -> dict:
    """Load config arguments based on a ´ConfZSource´.
    :param config_kwargs: Keyword-arguments provided to the config model.
    :param confz_sources: Source configuration.
    :return: A dict with all config arguments.
    """
    config = config_kwargs.copy()
    if isinstance(confz_sources, list):
        for confz_source in confz_sources:
            _populate_config(config, confz_source)
    else:
        _populate_config(config, confz_sources)
    return config
