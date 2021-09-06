from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional, Union


class FileFormat(Enum):
    JSON = 'json'
    YAML = 'yaml'


@dataclass
class ConfZSource:
    """Source config for `ConfZ` models. Allows to specify files, environment variables and command line arguments as
    source for a configuration."""
    # These three attributes specify a config file. The config file can either be given directly by a path `file`,
    # it can be read from an environment variable `file_env` or it can be passed as command line argument `file_cli`
    # both at a specific position (integer, e.g. 1) or after a specific option (string, e.g.
    # '--config-file config.yml'). If none of these three options is specified, no config file is read.
    file: Optional[Path] = None
    file_env: Optional[str] = None
    file_cli: Optional[Union[int, str]] = None

    # The file specified above can optionally be relative to this folder
    file_folder: Optional[Path] = None

    # The format of the config file. If not specified, `ConfZ` tries to infer the format from the file ending.
    file_format: Optional[FileFormat] = None
