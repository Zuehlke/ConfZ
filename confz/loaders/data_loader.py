from confz.confz_source import DataSource
from .loader import Loader


class DataLoader(Loader):
    """Config loader for fix data."""

    @classmethod
    def populate_config(cls, config: dict, confz_source: DataSource):
        cls.update_dict_recursively(config, confz_source.data)
