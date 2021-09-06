from ..confz_source import ConfZSource
from .file_loader import FileLoader


def load_config(config_kwargs: dict, confz_source: ConfZSource) -> dict:
    """Load config arguments based on a ´ConfZSource´.
    :param config_kwargs: Keyword-arguments provided to the config model.
    :param confz_source: Source configuration.
    :return: A dict with all config arguments.
    """
    config = config_kwargs.copy()
    FileLoader.populate_config(config, confz_source)
    return config
