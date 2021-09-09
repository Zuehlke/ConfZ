from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional, Union, List, Dict, Any


@dataclass
class ConfZSource:
    """Source config for `ConfZ` models."""


ConfZSources = Union[ConfZSource, List[ConfZSource]]


class FileFormat(Enum):
    JSON = 'json'
    YAML = 'yaml'


@dataclass
class ConfZFileSource(ConfZSource):
    """Source config for `ConfZ` models for config files."""
    # These three attributes specify a config file. The config file can either be given directly by a path `name`,
    # it can be read from an environment variable `name_from_env` or it can be passed as command line argument
    # `name_from_cl` both at a specific position (integer, e.g. 1) or after a specific option (string, e.g.
    # '--config-file config.yml').
    name: Optional[Path] = None
    name_from_env: Optional[str] = None
    name_from_cl: Optional[Union[int, str]] = None

    # The file specified above can optionally be relative to this folder
    folder: Optional[Path] = None

    # The format of the config file. If not specified, `ConfZ` tries to infer the format from the file ending.
    format: Optional[FileFormat] = None


@dataclass
class ConfZEnvSource(ConfZSource):
    """Source config for `ConfZ` models for environment variables. Environment variable names are transformed to
    lowercase and all dashes are replaced by underscores. The definitions below are not case-sensitive and can be
    written with underscore or dash. An exception is ´prefix´, which needs to match exactly. Double underscores
    can be used to access recursive configurations."""
    # These three attributes specify environment variables to read from. Either, all environment variables can be used
    # by setting ´allow_all´ or only specific variables by populating ´allow´. In the former case, certain environment
    # variables can be excluded by populating ´deny´.
    allow_all: bool = False
    allow: Optional[List[str]] = None
    deny: Optional[List[str]] = None
    # The selection above can be narrowed down to a specific prefix, e.g. "CONFIG_". The variables in the lists above
    # or the map below do not need to include this prefix, it is automatically added. This option is especially
    # recommended, if ´allow_all´ is set.
    prefix: Optional[str] = None
    # Certain environment variables can be mapped to config arguments with a different name.
    remap: Optional[Dict[str, str]] = None


@dataclass
class ConfZCLArgSource(ConfZSource):
    """Source config for `ConfZ` models for command line arguments. Command line arguments are case-sensitive.
    Double underscore can be used to access recursive configurations."""
    # Optionally, all command line arguments can have a prefix, e.g. "config_". The map below does not need to include
    # this prefix, it is automatically added.
    prefix: Optional[str] = None
    # Certain command line arguments can be mapped to config arguments with a different name.
    remap: Optional[Dict[str, str]] = None


@dataclass
class ConfZDataSource(ConfZSource):
    """Source config for `ConfZ` models for raw data, i.e. constants. This can be useful for unit-test together with
    ´set_config_sources()´ to inject test data into the config."""
    # All data should go into this (possibly nested) dict.
    data: Dict[str, Any]
