import sys
from typing import List

import pytest

from confz import BaseConfig, FileSource, FileFormat
from confz.exceptions import FileException
from confz.loaders.file_loader import FileLoader
from tests.assets import ASSET_FOLDER


class InnerConfig(BaseConfig):
    attr1: str


class OuterConfig(BaseConfig):
    attr2: str
    inner: InnerConfig


class ListElementConfig(BaseConfig):
    key: str
    value: str


class SecondOuterConfig(OuterConfig):
    attrs: List[ListElementConfig]


def test_json_file():
    config = OuterConfig(config_sources=FileSource(file=ASSET_FOLDER / "config.json"))
    assert config.inner.attr1 == "1 🎉"
    assert config.attr2 == "2"


def test_yaml_file():
    config = OuterConfig(config_sources=FileSource(file=ASSET_FOLDER / "config.yml"))
    assert config.inner.attr1 == "1 🎉"
    assert config.attr2 == "2"


def test_multiple_yaml_files_both_available():
    config = OuterConfig(
        config_sources=[
            FileSource(file=ASSET_FOLDER / "config.yml"),
            FileSource(file=ASSET_FOLDER / "config_2.yml"),
        ]
    )
    assert config.inner.attr1 == "4 🎉"
    assert config.attr2 == "10"


def test_multiple_yaml_files_one_is_optional_and_unavailable():
    config = OuterConfig(
        config_sources=[
            FileSource(file=ASSET_FOLDER / "config.yml"),
            FileSource(file=ASSET_FOLDER / "config_not_existing.yml", optional=True),
        ]
    )
    assert config.inner.attr1 == "1 🎉"
    assert config.attr2 == "2"


def test_toml_file():
    config = SecondOuterConfig(
        config_sources=FileSource(file=ASSET_FOLDER / "config.toml")
    )
    assert config.inner.attr1 == "1 🎉"
    assert config.attr2 == "2"
    assert config.attrs[0].key == "A"
    assert config.attrs[0].value == "1"
    assert config.attrs[1].key == "B"
    assert config.attrs[1].value == "2"


def test_bytes_file():
    json_dummy_content = b'{"inner":{"attr1": "2"}, "attr2": "5"}'
    config = OuterConfig(
        config_sources=FileSource(file=json_dummy_content, format=FileFormat.JSON)
    )
    assert config.attr2 == "5"
    assert config.inner.attr1 == "2"
    with pytest.raises(FileException):
        OuterConfig(config_sources=FileSource(file=json_dummy_content))


def test_custom_file():
    # does not recognize format per default
    with pytest.raises(FileException):
        OuterConfig(config_sources=FileSource(file=ASSET_FOLDER / "config.txt"))

    # can specify format
    config = OuterConfig(
        config_sources=FileSource(
            file=ASSET_FOLDER / "config.txt", format=FileFormat.YAML
        )
    )
    assert config.inner.attr1 == "1 🎉"
    assert config.attr2 == "2"


def test_file_path_from_bytes():
    json_dummy_content = b'{"inner":{"attr1": "2"}, "attr2": "5"}'
    source = FileSource(file=json_dummy_content, format=FileFormat.JSON)
    with pytest.raises(FileException):
        FileLoader._get_filename(source)


def test_custom_file_str_path():
    # can specify format
    config = OuterConfig(
        config_sources=FileSource(
            file=str(ASSET_FOLDER) + "/config.txt", format=FileFormat.YAML
        )
    )
    assert config.inner.attr1 == "1 🎉"
    assert config.attr2 == "2"


def test_wrong_format():
    with pytest.raises(FileException):
        OuterConfig(
            config_sources=FileSource(
                file=str(ASSET_FOLDER) + "/config.txt", format="wrong value"
            )
        )


def test_invalid_file():
    with pytest.raises(FileException):
        OuterConfig(config_sources=FileSource(file=ASSET_FOLDER / "non_existing.json"))


def test_invalid_file_str():
    with pytest.raises(FileException):
        OuterConfig(
            config_sources=FileSource(file=str(ASSET_FOLDER) + "/non_existing.json")
        )


def test_no_file():
    with pytest.raises(FileException):
        OuterConfig(config_sources=FileSource())


def test_from_env(monkeypatch):
    env_var = "MY_CONFIG_FILE"

    # raises error if not set
    with pytest.raises(FileException):
        OuterConfig(
            config_sources=FileSource(file_from_env=env_var, folder=ASSET_FOLDER)
        )

    # works if set
    monkeypatch.setenv(env_var, "config.json")
    config = OuterConfig(
        config_sources=FileSource(file_from_env=env_var, folder=ASSET_FOLDER)
    )
    assert config.inner.attr1 == "1 🎉"
    assert config.attr2 == "2"


def test_from_env_using_str_path(monkeypatch):
    env_var = "MY_CONFIG_FILE"

    # works if set
    monkeypatch.setenv(env_var, "config.json")
    assert_folder_str: str = str(ASSET_FOLDER)
    config = OuterConfig(
        config_sources=FileSource(file_from_env=env_var, folder=assert_folder_str)
    )
    assert config.inner.attr1 == "1 🎉"
    assert config.attr2 == "2"


def test_from_cl_arg_idx(monkeypatch):
    argv_backup = sys.argv.copy()
    cl_arg_idx = len(argv_backup)

    # raises error if not set
    with pytest.raises(FileException):
        OuterConfig(
            config_sources=FileSource(file_from_cl=cl_arg_idx, folder=ASSET_FOLDER)
        )

    # works if set
    monkeypatch.setattr(sys, "argv", argv_backup + ["config.json"])
    config = OuterConfig(
        config_sources=FileSource(file_from_cl=cl_arg_idx, folder=ASSET_FOLDER)
    )
    assert config.inner.attr1 == "1 🎉"
    assert config.attr2 == "2"


def test_from_cl_arg_name(monkeypatch):
    argv_backup = sys.argv.copy()
    cl_arg_name = "--my_config_file"

    # raises error if not set
    with pytest.raises(FileException):
        OuterConfig(
            config_sources=FileSource(file_from_cl=cl_arg_name, folder=ASSET_FOLDER)
        )

    # raises error if missing value
    with pytest.raises(FileException):
        monkeypatch.setattr(sys, "argv", argv_backup + [cl_arg_name])
        OuterConfig(
            config_sources=FileSource(file_from_cl=cl_arg_name, folder=ASSET_FOLDER)
        )

    # works if set
    monkeypatch.setattr(sys, "argv", argv_backup + [cl_arg_name, "config.json"])
    config = OuterConfig(
        config_sources=FileSource(file_from_cl=cl_arg_name, folder=ASSET_FOLDER)
    )
    assert config.inner.attr1 == "1 🎉"
    assert config.attr2 == "2"


def test_from_cl_arg_optional():
    # if not set, should load the config file without errors
    config = OuterConfig(
        config_sources=[
            FileSource(file_from_cl="--my_config_file", optional=True),
            FileSource(file=ASSET_FOLDER / "config.yml"),
        ]
    )
    assert config.inner.attr1 == "1 🎉"
    assert config.attr2 == "2"
