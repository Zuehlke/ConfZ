import pytest
from pydantic import ValidationError

from confz import BaseConfig, DataSource
from confz.exceptions import ConfigException


class InnerConfig(BaseConfig):
    attr1: int


class OuterConfig(BaseConfig):
    attr2: int
    inner: InnerConfig


class ParentConfig1(OuterConfig):
    attr3: int

    CONFIG_SOURCES = DataSource(data={"inner": {"attr1": 1}, "attr2": 2, "attr3": 3})


class ParentConfig2(OuterConfig):
    attr4: int

    CONFIG_SOURCES = DataSource(data={"inner": {"attr1": 1}, "attr2": 2, "attr4": 4})


class ParentConfig3(OuterConfig):
    attr5: int


def test_simple():
    # needs kwargs
    with pytest.raises(ValidationError):
        OuterConfig()

    # uses kwargs
    config1 = OuterConfig(attr2=2, inner={"attr1": 1})
    assert config1.inner.attr1 == 1
    assert config1.attr2 == 2

    # no singleton
    config2 = OuterConfig(attr2=2, inner={"attr1": 1})
    assert config1 == config2
    assert config1 is not config2


def test_class_var():
    # uses sources
    config1 = ParentConfig1()
    assert config1.attr2 == 2

    # kwargs do not work
    with pytest.raises(ConfigException):
        ParentConfig1(attr3=3)

    # singleton
    assert ParentConfig1() is config1
    assert ParentConfig2() is ParentConfig2()
    assert ParentConfig1() is not ParentConfig2()
    assert ParentConfig1().inner is ParentConfig1().inner
    assert ParentConfig1().inner is not ParentConfig2().inner


def test_init_arg():
    # assert that uses sources
    config = OuterConfig(
        config_sources=DataSource(data={"inner": {"attr1": 1}, "attr2": 20})
    )
    assert config.attr2 == 20

    # no singleton
    assert ParentConfig1() is ParentConfig1()
    config1 = ParentConfig1(
        config_sources=DataSource(data={"inner": {"attr1": 1}, "attr2": 2, "attr3": 3})
    )
    config2 = ParentConfig1(
        config_sources=DataSource(data={"inner": {"attr1": 1}, "attr2": 2, "attr3": 3})
    )
    assert config1 == config2
    assert config1 is not config2

    # uses kwargs
    with pytest.raises(ValidationError):
        ParentConfig3(
            config_sources=DataSource(data={"inner": {"attr1": 1}, "attr2": 2})
        )
    config = ParentConfig3(
        attr5=5,
        config_sources=DataSource(data={"inner": {"attr1": 1}, "attr2": 2}),
    )
    assert config.attr5 == 5
