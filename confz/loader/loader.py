from abc import ABC, abstractmethod

from ..confz_source import ConfZSource


class Loader(ABC):
    """An abstract base class for all config loaders."""

    @classmethod
    @abstractmethod
    def populate_config(cls, config: dict, confz_source: ConfZSource):
        """Populate the config-dict with new config arguments based on the source.
        :param config: Config dictionary, gets extended with new arguments
        :param confz_source: Source configuration.
        """
