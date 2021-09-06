from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional, Union, List, Dict


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
    # it can be read from an environment variable `env_var` or it can be passed as command line argument `cl_arg`
    # both at a specific position (integer, e.g. 1) or after a specific option (string, e.g.
    # '--config-file config.yml').
    name: Optional[Path] = None
    env_var: Optional[str] = None
    cl_arg: Optional[Union[int, str]] = None

    # The file specified above can optionally be relative to this folder
    folder: Optional[Path] = None

    # The format of the config file. If not specified, `ConfZ` tries to infer the format from the file ending.
    format: Optional[FileFormat] = None


@dataclass
class ConfZEnvSource(ConfZSource):
    """Source config for `ConfZ` models for environment variables. Environment variable names are transformed to
    lowercase and all dashes are replaced by underscores. The definitions below are not case-sensitive and can be
    written with underscore or dash. An exception is ´prefix´, which needs to match exactly."""
    # These three attributes specify environment variables to read from. Either, all environment variables can be used
    # by setting ´allow_all´ or only specific variables by populating ´allow´. In the former case, certain environment
    # variables can be excluded by populating ´deny´.
    allow_all: bool = False
    allow: Optional[List[str]] = None
    deny: Optional[List[str]] = None
    # The selection above can be narrowed down to a specific prefix, e.g. "CONFIG_". The variable in the lists above
    # do not need to include this prefix, it is automatically added.
    prefix: Optional[str] = None
    # Certain environment variables can be mapped to config arguments with a different name.
    remap: Optional[Dict[str, str]] = None
