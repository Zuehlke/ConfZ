from dataclasses import dataclass

import pytest

from confz import BaseConfig, DataSource, ConfigSource, EnvSource
from confz.exceptions import UpdateException, ConfigException
from confz.loaders import Loader, register_loader


class InnerConfig(BaseConfig):
    attr1: int


class OuterConfig(BaseConfig):
    attr2: int
    inner: InnerConfig


@dataclass
class CustomSource(ConfigSource):
    custom_attr: int


@dataclass
class CustomSource2(ConfigSource):
    pass


class CustomLoader(Loader):
    @classmethod
    def populate_config(cls, config: dict, config_source: CustomSource):
        assert config == {"kwarg_2": 2}
        assert config_source.custom_attr == 1
        config["attr2"] = 2
        config["inner"] = {"attr1": 1}


register_loader(CustomSource, CustomLoader)


def test_update_dict_recursively():
    config = OuterConfig(
        config_sources=[
            DataSource(data={"inner": {"attr1": 1}, "attr2": 2}),
            DataSource(data={"inner": {"attr1": 3}}),
            DataSource(data={"attr2": 4}),
        ]
    )
    assert config.inner.attr1 == 3
    assert config.attr2 == 4


def test_dict_contradiction(monkeypatch):
    with pytest.raises(UpdateException):
        OuterConfig(
            config_sources=[
                DataSource(data={"inner": "something"}),
                DataSource(data={"inner": {"attr1": 3}}),
            ]
        )
    monkeypatch.setenv("INNER", "something")
    monkeypatch.setenv("INNER.ATTR1", "3")
    with pytest.raises(UpdateException):
        OuterConfig(config_sources=EnvSource(allow_all=True))


def test_own_loader():
    config = OuterConfig(config_sources=CustomSource(custom_attr=1), kwarg_2=2)
    assert config.inner.attr1 == 1
    assert config.attr2 == 2


def test_unregistered_source():
    InnerConfig(attr1=2)

    with pytest.raises(ConfigException):
        InnerConfig(config_sources=CustomSource2(), attr1=2)
