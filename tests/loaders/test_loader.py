from dataclasses import dataclass

import pytest

from confz import ConfZ, ConfZDataSource, ConfZSource, ConfZEnvSource
from confz.exceptions import ConfZUpdateException, ConfZException
from confz.loaders import Loader, register_loader


class InnerConfig(ConfZ):
    attr1: int


class OuterConfig(ConfZ):
    attr2: int
    inner: InnerConfig


@dataclass
class CustomSource(ConfZSource):
    custom_attr: int


@dataclass
class CustomSource2(ConfZSource):
    pass


class CustomLoader(Loader):
    @classmethod
    def populate_config(cls, config: dict, confz_source: CustomSource):
        assert config == {"kwarg_2": 2}
        assert confz_source.custom_attr == 1
        config["attr2"] = 2
        config["inner"] = {"attr1": 1}


register_loader(CustomSource, CustomLoader)


def test_update_dict_recursively():
    config = OuterConfig(
        config_sources=[
            ConfZDataSource(data={"inner": {"attr1": 1}, "attr2": 2}),
            ConfZDataSource(data={"inner": {"attr1": 3}}),
            ConfZDataSource(data={"attr2": 4}),
        ]
    )
    assert config.inner.attr1 == 3
    assert config.attr2 == 4


def test_dict_contradiction(monkeypatch):
    with pytest.raises(ConfZUpdateException):
        OuterConfig(
            config_sources=[
                ConfZDataSource(data={"inner": "something"}),
                ConfZDataSource(data={"inner": {"attr1": 3}}),
            ]
        )
    monkeypatch.setenv("INNER", "something")
    monkeypatch.setenv("INNER.ATTR1", "3")
    with pytest.raises(ConfZUpdateException):
        OuterConfig(config_sources=ConfZEnvSource(allow_all=True))


def test_own_loader():
    config = OuterConfig(config_sources=CustomSource(custom_attr=1), kwarg_2=2)
    assert config.inner.attr1 == 1
    assert config.attr2 == 2


def test_unregistered_source():
    InnerConfig(attr1=2)

    with pytest.raises(ConfZException):
        InnerConfig(config_sources=CustomSource2(), attr1=2)
