from confz.config_source import DataSource
from .loader import Loader


class DataLoader(Loader):
    """Config loader for fix data."""

    @classmethod
    def populate_config(cls, config: dict, config_source: DataSource):
        cls.update_dict_recursively(config, config_source.data)
