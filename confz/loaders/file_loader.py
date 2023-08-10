from contextlib import contextmanager
import io
import json
import os
import sys
from pathlib import Path
from typing import Iterator, Optional, TextIO, Union

import toml
import yaml

from confz.config_source import FileSource, FileFormat
from confz.exceptions import FileException
from .loader import Loader


class FileLoader(Loader):
    """Config loader for config files."""

    @classmethod
    def _get_filename(cls, config_source: FileSource) -> Path:
        if config_source.file is not None:
            if isinstance(config_source.file, bytes):
                raise FileException("Can not detect filename from type bytes")
            file_path = Path(config_source.file)
        elif config_source.file_from_env is not None:
            if config_source.file_from_env not in os.environ:
                raise FileException(
                    f"Environment variable '{config_source.file_from_env}' is not set."
                )
            file_path = Path(os.environ[config_source.file_from_env])
        elif config_source.file_from_cl is not None:
            if isinstance(config_source.file_from_cl, int):
                try:
                    file_path = Path(sys.argv[config_source.file_from_cl])
                except IndexError as e:
                    raise FileException(
                        f"Command-line argument number {config_source.file_from_cl} "
                        f"is not set."
                    ) from e
            else:
                try:
                    idx = sys.argv.index(config_source.file_from_cl)
                except ValueError as e:
                    raise FileException(
                        f"Command-line argument '{config_source.file_from_cl}' "
                        f"not found."
                    ) from e
                try:
                    file_path = Path(sys.argv[idx + 1])
                except IndexError as e:
                    raise FileException(
                        f"Command-line argument '{config_source.file_from_cl}' is not "
                        f"set."
                    ) from e
        else:
            raise FileException("No file source set.")

        if config_source.folder is not None:
            file_path = Path(config_source.folder) / file_path

        return file_path

    @classmethod
    def _get_format(
        cls, file_path: Path, file_format: Optional[FileFormat]
    ) -> FileFormat:
        if file_format is not None:
            return file_format

        suffix_formats = {
            ".yml": FileFormat.YAML,
            ".yaml": FileFormat.YAML,
            ".json": FileFormat.JSON,
            ".toml": FileFormat.TOML,
        }
        suffix = file_path.suffix
        try:
            suffix_format = suffix_formats[suffix]
        except KeyError as e:
            raise FileException(
                f"File-ending '{suffix}' is not known. Supported are: "
                f"{', '.join(list(suffix_formats.keys()))}."
            ) from e

        return suffix_format

    @classmethod
    def _parse_stream(
        cls,
        stream: Union[TextIO],
        file_format: FileFormat,
    ) -> dict:
        if file_format == FileFormat.YAML:
            file_content = yaml.load(stream, Loader=yaml.SafeLoader)
        elif file_format == FileFormat.JSON:
            file_content = json.load(stream)
        elif file_format == FileFormat.TOML:
            file_content = toml.load(stream)
        else:
            raise FileException(f"Unknown file format {file_format}.")
        return file_content

    @classmethod
    @contextmanager
    def _create_stream(cls, file_path: Path, file_encoding: str) -> Iterator[TextIO]:
        try:
            stream = file_path.open(encoding=file_encoding)
        except OSError as e:
            raise FileException(f"Could not open config file '{file_path}'.") from e
        with stream:
            yield stream

    @classmethod
    def _populate_config_from_bytes(
        cls, config: dict, data: bytes, config_source: FileSource
    ):
        if config_source.format is None:
            raise FileException(
                "The format needs to be defined if the "
                "configuration is passed as byte-string"
            )
        byte_stream = io.BytesIO(data)
        text_stream = io.TextIOWrapper(byte_stream, encoding=config_source.encoding)
        file_content = cls._parse_stream(text_stream, config_source.format)
        cls.update_dict_recursively(config, file_content)

    @classmethod
    def populate_config(cls, config: dict, config_source: FileSource):
        if config_source.file is not None and isinstance(config_source.file, bytes):
            cls._populate_config_from_bytes(
                config=config, data=config_source.file, config_source=config_source
            )
            return
        try:
            file_path = cls._get_filename(config_source)
        except FileException as e:
            if config_source.optional:
                return
            raise e
        file_format = cls._get_format(file_path, config_source.format)
        try:
            with cls._create_stream(file_path, config_source.encoding) as file_stream:
                file_content = cls._parse_stream(file_stream, file_format)
        except FileException as e:
            if config_source.optional:
                return
            raise e
        cls.update_dict_recursively(config, file_content)
