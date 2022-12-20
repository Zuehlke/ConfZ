import io
import os
from typing import Dict, Optional, Any

from dotenv import dotenv_values

from confz.confz_source import ConfZEnvSource
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
    def _check_allowance(cls, var_name: str, confz_source: ConfZEnvSource) -> bool:
        if not confz_source.allow_all:
            if confz_source.allow is None:
                return False

            allow_list = [cls._transform_name(var) for var in confz_source.allow]
            if var_name not in allow_list:
                return False

        if confz_source.deny is not None:
            deny_list = [cls._transform_name(var) for var in confz_source.deny]
            if var_name in deny_list:
                return False

        return True

    @classmethod
    def populate_config(cls, config: dict, confz_source: ConfZEnvSource):
        remap = cls._transform_remap(confz_source.remap)

        origin_env_vars: Dict[str, Any] = dict(os.environ)
        if confz_source.file is not None:
            if not isinstance(confz_source.file, bytes):
                origin_env_vars = {
                    **dotenv_values(confz_source.file),
                    **origin_env_vars,
                }
            else:
                byte_stream = io.BytesIO(confz_source.file)
                stream = io.TextIOWrapper(byte_stream, encoding="utf-8")
                origin_env_vars = {**dotenv_values(None, stream), **origin_env_vars}

        env_vars = {}
        for env_var in origin_env_vars:
            var_name = env_var
            if confz_source.prefix is not None:
                if not var_name.startswith(confz_source.prefix):
                    continue
                var_name = var_name[len(confz_source.prefix) :]

            var_name = cls._transform_name(var_name)
            if not cls._check_allowance(var_name, confz_source):
                continue

            if remap is not None and var_name in remap:
                var_name = remap[var_name]

            env_vars[var_name] = origin_env_vars[env_var]

        env_vars = cls.transform_nested_dicts(
            env_vars, separator=confz_source.nested_separator
        )
        cls.update_dict_recursively(config, env_vars)
