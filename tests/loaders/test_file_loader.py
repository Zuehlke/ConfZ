import sys

import pytest

from confz import ConfZ, ConfZFileSource, FileFormat
from confz.exceptions import ConfZFileException
from tests.assets import ASSET_FOLDER


class InnerConfig(ConfZ):
    attr1: str


class OuterConfig(ConfZ):
    attr2: str
    inner: InnerConfig


def test_json_file():
    config = OuterConfig(config_sources=ConfZFileSource(
        file=ASSET_FOLDER / 'config.json'
    ))
    assert config.inner.attr1 == '1 🎉'
    assert config.attr2 == '2'


def test_yaml_file():
    config = OuterConfig(config_sources=ConfZFileSource(
        file=ASSET_FOLDER / 'config.yml'
    ))
    assert config.inner.attr1 == '1 🎉'
    assert config.attr2 == '2'


def test_custom_file():
    # does not recognize format per default
    with pytest.raises(ConfZFileException):
        OuterConfig(config_sources=ConfZFileSource(
            file=ASSET_FOLDER / 'config.txt'
        ))

    # can specify format
    config = OuterConfig(config_sources=ConfZFileSource(
        file=ASSET_FOLDER / 'config.txt',
        format=FileFormat.YAML
    ))
    assert config.inner.attr1 == '1 🎉'
    assert config.attr2 == '2'


def test_invalid_file():
    with pytest.raises(ConfZFileException):
        OuterConfig(config_sources=ConfZFileSource(
            file=ASSET_FOLDER / 'non_existing.json'
        ))


def test_from_env(monkeypatch):
    env_var = 'MY_CONFIG_FILE'

    # raises error if not set
    with pytest.raises(ConfZFileException):
        OuterConfig(config_sources=ConfZFileSource(
            file_from_env=env_var,
            folder=ASSET_FOLDER
        ))

    # works if set
    monkeypatch.setenv(env_var, 'config.json')
    config = OuterConfig(config_sources=ConfZFileSource(
        file_from_env=env_var,
        folder=ASSET_FOLDER
    ))
    assert config.inner.attr1 == '1 🎉'
    assert config.attr2 == '2'


def test_from_cl_arg_idx(monkeypatch):
    argv_backup = sys.argv.copy()
    cl_arg_idx = len(argv_backup)

    # raises error if not set
    with pytest.raises(ConfZFileException):
        OuterConfig(config_sources=ConfZFileSource(
            file_from_cl=cl_arg_idx,
            folder=ASSET_FOLDER
        ))

    # works if set
    monkeypatch.setattr(sys, 'argv', argv_backup + ['config.json'])
    config = OuterConfig(config_sources=ConfZFileSource(
        file_from_cl=cl_arg_idx,
        folder=ASSET_FOLDER
    ))
    assert config.inner.attr1 == '1 🎉'
    assert config.attr2 == '2'


def test_from_cl_arg_name(monkeypatch):
    argv_backup = sys.argv.copy()
    cl_arg_name = '--my_config_file'

    # raises error if not set
    with pytest.raises(ConfZFileException):
        OuterConfig(config_sources=ConfZFileSource(
            file_from_cl=cl_arg_name,
            folder=ASSET_FOLDER
        ))

    # works if set
    monkeypatch.setattr(sys, 'argv', argv_backup + [cl_arg_name, 'config.json'])
    config = OuterConfig(config_sources=ConfZFileSource(
        file_from_cl=cl_arg_name,
        folder=ASSET_FOLDER
    ))
    assert config.inner.attr1 == '1 🎉'
    assert config.attr2 == '2'
