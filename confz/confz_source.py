from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional, Union, List, Dict, Any


@dataclass
class ConfZSource:
    """Source configuration for :class:`~confz.ConfZ` models."""


ConfZSources = Union[ConfZSource, List[ConfZSource]]


class FileFormat(Enum):
    """Enum for file format."""
    JSON = 'json'   #: JSON file format
    YAML = 'yaml'   #: YAML file format


@dataclass
class ConfZFileSource(ConfZSource):
    """Source config for files."""
    file: Optional[Path] = None
    """Specify a config file directly by a path."""
    file_from_env: Optional[str] = None
    """Alternatively, use this environment variable to get the file."""
    file_from_cl: Optional[Union[int, str]] = None
    """Alternatively, use this command line argument to get the file name/path. It can be a specific position
    (integer, e.g. `1`) or after a specific option (string, e.g. `\\-\\-config-file`). In the latter case, the file
    name must follow after whitespace, an equal sign between argument and value is not supported at the moment."""
    folder: Optional[Path] = None
    """The file specified above can optionally be relative to this folder."""
    format: Optional[FileFormat] = None
    """The format of the config file. If not specified, it will be inferred from the file ending."""


@dataclass
class ConfZEnvSource(ConfZSource):
    """Source config for environment variables and .env files. On loading of the source, the dotenv file
    values (if available) are merged with the environment, with environment always taking precedence in case of
    name collusion. All loaded variable names are transformed to lowercase and all dashes are replaced by underscores.
    The definitions below are not case-sensitive and can be written with underscore or dash. An exception is `prefix`,
    which needs to match exactly. Dot-notation can be used to access nested configurations."""
    allow_all: bool = False
    """Allow potentially all environment variables to be read as config option."""
    allow: Optional[List[str]] = None
    """Only allow a list of environment variables as input."""
    deny: Optional[List[str]] = None
    """Do not allow to read from environemnt variables in this list. Useful if `allow_all` is set and certain variables
    should be excluded."""
    prefix: Optional[str] = None
    """The selection above can be narrowed down to a specific prefix, e.g. `CONFIG_`. The variables in the lists above
    or the map below do not need to include this prefix, it is automatically added. This option is especially
    recommended, if ´allow_all´ is set."""
    remap: Optional[Dict[str, str]] = None
    """Certain environment variables can be mapped to config arguments with a different name."""
    file: Optional[Path] = None
    """Built in .env file loading with lower than environment precedence."""


@dataclass
class ConfZCLArgSource(ConfZSource):
    """Source config for command line arguments. Command line arguments are case-sensitive. Dot-notation can be
    used to access nested configurations. Only command line arguments starting with two dashes (\\-\\-) are considered.
    Between argument and value must be whitespace, an equal sign is not supported at the moment."""
    prefix: Optional[str] = None
    """Optionally, all command line arguments can have a prefix, e.g. `config_`. The prefix does not need to include
    the two dashes at the beginning. The map below does not need to include the prefix, it is automatically added."""
    remap: Optional[Dict[str, str]] = None
    """Certain command line arguments can be mapped to config arguments with a different name. The map does not need to
    include the two dashes at the beginning."""


@dataclass
class ConfZDataSource(ConfZSource):
    """Source config for raw data, i.e. constants. This can be useful for unit-test together with
    :meth:`~confz.ConfZ.change_config_sources` to inject test data into the config."""
    data: Dict[str, Any]
    """All data should go into this (possibly nested) dict."""
