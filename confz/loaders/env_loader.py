import io
import os
from typing import Dict, Optional, Any

from dotenv import dotenv_values

from confz.config_source import EnvSource
from .loader import Loader


class EnvLoader(Loader):
    """Config loader for environment variables."""

    @classmethod
    def _transform_name(cls, name: str):
        return name.lower().replace("-", "_")

    @classmethod
    def _transform_remap(
        cls, map_in: Optional[Dict[str, str]]
    ) -> Optional[Dict[str, str]]:
        if map_in is None:
            return None

        map_out = {}
        for key, value in map_in.items():
            map_out[cls._transform_name(key)] = value
        return map_out

    @classmethod
    def _check_allowance(cls, var_name: str, config_source: EnvSource) -> bool:
        if not config_source.allow_all:
            if config_source.allow is None:
                return False

            allow_list = [cls._transform_name(var) for var in config_source.allow]
            if var_name not in allow_list:
                return False

        if config_source.deny is not None:
            deny_list = [cls._transform_name(var) for var in config_source.deny]
            if var_name in deny_list:
                return False

        return True

    @classmethod
    def populate_config(cls, config: dict, config_source: EnvSource):
        remap = cls._transform_remap(config_source.remap)

        origin_env_vars: Dict[str, Any] = dict(os.environ)
        if config_source.file is not None:
            if not isinstance(config_source.file, bytes):
                origin_env_vars = {
                    **dotenv_values(config_source.file),
                    **origin_env_vars,
                }
            else:
                byte_stream = io.BytesIO(config_source.file)
                stream = io.TextIOWrapper(byte_stream, encoding="utf-8")
                origin_env_vars = {**dotenv_values(None, stream), **origin_env_vars}

        env_vars = {}
        for env_var in origin_env_vars:
            var_name = env_var
            if config_source.prefix is not None:
                if not var_name.startswith(config_source.prefix):
                    continue
                var_name = var_name[len(config_source.prefix) :]

            var_name = cls._transform_name(var_name)
            if not cls._check_allowance(var_name, config_source):
                continue

            if remap is not None and var_name in remap:
                var_name = remap[var_name]

            env_vars[var_name] = origin_env_vars[env_var]

        env_vars = cls.transform_nested_dicts(
            env_vars, separator=config_source.nested_separator
        )
        cls.update_dict_recursively(config, env_vars)
