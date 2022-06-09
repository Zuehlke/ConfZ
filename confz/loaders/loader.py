from abc import ABC, abstractmethod
from typing import Dict, Any

from confz.exceptions import ConfZUpdateException


class Loader(ABC):
    """An abstract base class for all config loaders."""

    @classmethod
    def update_dict_recursively(cls, original_dict: Dict, update_dict: Dict):
        """Updates the original dict with the new data. Similar to `dict.update()`, but
        works with nested dicts.

        :param original_dict: The original dictionary to update in-place.
        :param update_dict: The new data.
        :raises ConfZUpdateException: If dict keys contradict each other.
        """
        for key, value in update_dict.items():
            if isinstance(value, dict) and key in original_dict:
                if not isinstance(original_dict[key], dict):
                    raise ConfZUpdateException(
                        f"Config variables contradict each other: "
                        f"Key '{key}' is both a value and a nested dict."
                    )
                cls.update_dict_recursively(original_dict[key], value)
            else:
                original_dict[key] = value

    @classmethod
    def transform_nested_dicts(
        cls, dict_in: Dict[str, Any], separator: str = "."
    ) -> Dict[str, Any]:
        """Transform dictionaries into nested dictionaries, using a separator in the
        keys as hint.

        :param dict_in: A dictionary with string-keys.
        :param separator: The string used to separate dict keys.
                          Default value will no longer be set in a future release.
        :return: The transformed dictionary, splitting keys at the separator and
            creating a new dictionary out of it.
        :raises ConfZUpdateException: If dict keys contradict each other.
        """
        dict_out: Dict[str, Any] = {}
        for key, value in dict_in.items():
            if separator in key and not key.startswith(separator):
                inner_keys = key.split(separator)
                dict_inner = dict_out
                for idx, inner_key in enumerate(inner_keys):
                    if idx == len(inner_keys) - 1:
                        dict_inner[inner_key] = value
                    else:
                        if inner_key not in dict_inner:
                            dict_inner[inner_key] = {}
                        elif not isinstance(dict_inner[inner_key], dict):
                            raise ConfZUpdateException(
                                f"Config variables contradict each other: Key "
                                f"'{inner_key}' is both a value and a nested dict."
                            )
                        dict_inner = dict_inner[inner_key]
            else:
                dict_out[key] = value

        return dict_out

    @classmethod
    @abstractmethod
    def populate_config(cls, config: dict, confz_source):
        """Populate the config-dict with new config arguments based on the source.

        :param config: Config dictionary, gets extended with new arguments
        :param confz_source: Source configuration.
        """
