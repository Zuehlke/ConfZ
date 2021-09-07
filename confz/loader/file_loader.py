import json
import os
import sys
from pathlib import Path
from typing import Optional

import yaml

from .loader import Loader
from ..confz_source import ConfZFileSource, FileFormat
from ..exceptions import ConfZFileException


class FileLoader(Loader):
    """Config loader for config files."""

    @classmethod
    def _get_filename(cls, confz_source: ConfZFileSource) -> Path:
        if confz_source.name is not None:
            file_path = confz_source.name
        elif confz_source.env_var is not None:
            if confz_source.env_var not in os.environ:
                raise ConfZFileException(f'Environment variable "{confz_source.env_var}" is not set.')
            file_path = Path(os.environ[confz_source.env_var])
        elif confz_source.cl_arg is not None:
            if isinstance(confz_source.cl_arg, int):
                try:
                    file_path = Path(sys.argv[confz_source.cl_arg])
                except IndexError:
                    raise ConfZFileException(f'Command-line argument number {confz_source.cl_arg} is not set.')
            else:
                try:
                    idx = sys.argv.index(confz_source.cl_arg)
                except ValueError:
                    raise ConfZFileException(f'Command-line argument "{confz_source.cl_arg}" not found.')
                try:
                    file_path = Path(sys.argv[idx+1])
                except IndexError:
                    raise ConfZFileException(f'Command-line argument "{confz_source.cl_arg}" is not set.')
        else:
            raise ConfZFileException(f'No file source set.')

        if confz_source.folder is not None:
            file_path = confz_source.folder / file_path

        return file_path

    @classmethod
    def _get_format(cls, file_path: Path, file_format: Optional[FileFormat]) -> FileFormat:
        if file_format is not None:
            return file_format

        suffix_formats = {
            '.yml': FileFormat.YAML,
            '.yaml': FileFormat.YAML,
            '.json': FileFormat.JSON
        }
        suffix = file_path.suffix
        try:
            suffix_format = suffix_formats[suffix]
        except KeyError:
            raise ConfZFileException(f'File-ending "{suffix}" is not known. Supported are: '
                                     f'{", ".join(list(suffix_formats.keys()))}.')

        return suffix_format

    @classmethod
    def _read_file(cls, file_path: Path, file_format: FileFormat) -> dict:
        try:
            with file_path.open() as f:
                if file_format == FileFormat.YAML:
                    file_content = yaml.safe_load(f)
                elif file_format == FileFormat.JSON:
                    file_content = json.load(f)
        except OSError as e:
            raise ConfZFileException(f'Could not open config file "{file_path}".') from e

        return file_content

    @classmethod
    def populate_config(cls, config: dict, confz_source: ConfZFileSource):
        file_path = cls._get_filename(confz_source)
        file_format = cls._get_format(file_path, confz_source.format)
        file_content = cls._read_file(file_path, file_format)
        cls.update_dict_recursively(config, file_content)
