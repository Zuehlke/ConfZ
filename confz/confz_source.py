from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional, Union, List


@dataclass
class ConfZSource:
    """Source config for `ConfZ` models."""


ConfZSources = Union[ConfZSource, List[ConfZSource]]


class FileFormat(Enum):
    JSON = 'json'
    YAML = 'yaml'


@dataclass
class ConfZFileSource(ConfZSource):
    """Source config for `ConfZ` models for config files"""
    # These three attributes specify a config file. The config file can either be given directly by a path `file`,
    # it can be read from an environment variable `file_env` or it can be passed as command line argument `file_cli`
    # both at a specific position (integer, e.g. 1) or after a specific option (string, e.g.
    # '--config-file config.yml').
    name: Optional[Path] = None
    env_var: Optional[str] = None
    cl_arg: Optional[Union[int, str]] = None

    # The file specified above can optionally be relative to this folder
    folder: Optional[Path] = None

    # The format of the config file. If not specified, `ConfZ` tries to infer the format from the file ending.
    format: Optional[FileFormat] = None
