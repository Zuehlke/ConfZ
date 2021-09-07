import os

import pytest
from pydantic import ValidationError

from confz import ConfZ, ConfZEnvSource
from confz.exceptions import ConfZException


class InnerConfig(ConfZ):
    attr1: int


class OuterConfig(ConfZ):
    attr2: int
    inner: InnerConfig


class ParentConfig1(OuterConfig):
    attr3: int

    CONFIG_SOURCES = ConfZEnvSource(allow_all=True, prefix='CONF_')


class ParentConfig2(OuterConfig):
    attr4: int

    CONFIG_SOURCES = ConfZEnvSource(allow_all=True, prefix='CONF_')


class ParentConfig3(OuterConfig):
    attr5: int

    CONFIG_SOURCES = ConfZEnvSource(allow_all=True, prefix='CONF_')


@pytest.fixture
def env_vars():
    os.environ['CONF_inner__attr1'] = '1'
    os.environ['CONF_attr2'] = '2'
    os.environ['CONF_attr3'] = '3'
    os.environ['CONF_attr4'] = '4'
    yield
    del os.environ['CONF_inner__attr1']
    del os.environ['CONF_attr2']
    del os.environ['CONF_attr3']
    del os.environ['CONF_attr4']


def test_transparent():
    # assert that needs kwargs
    with pytest.raises(ValidationError):
        OuterConfig()

    # assert that uses kwargs
    config1 = OuterConfig(attr2=2, inner={'attr1': 1})
    assert config1.inner.attr1 == 1
    assert config1.attr2 == 2

    # assert no singleton
    config2 = OuterConfig(attr2=2, inner={'attr1': 1})
    assert config1 is not config2


def test_class_var(env_vars):
    # assert that kwargs do not work
    with pytest.raises(ConfZException):
        ParentConfig1(attr3=3)

    # assert that uses env vars
    config1 = ParentConfig1()
    assert config1.attr2 == 2

    # asset that singleton
    assert ParentConfig1() == config1
    assert ParentConfig2() is ParentConfig2()
    assert ParentConfig1() is not ParentConfig2
    assert ParentConfig1().inner is ParentConfig1().inner
    assert ParentConfig1().inner is not ParentConfig2().inner


def test_init_arg(env_vars):
    # assert that uses env vars
    config = OuterConfig(config_sources=ConfZEnvSource(allow_all=True, prefix='CONF_'))
    assert config.attr2 == 2

    # assert that no singleton
    assert ParentConfig1() is ParentConfig1()
    config1 = ParentConfig1(config_sources=ConfZEnvSource(allow_all=True, prefix='CONF_'))
    config2 = ParentConfig1(config_sources=ConfZEnvSource(allow_all=True, prefix='CONF_'))
    assert config1 is not config2

    # assert that uses kwargs
    with pytest.raises(ValidationError):
        ParentConfig3(config_sources=ConfZEnvSource(allow_all=True, prefix='CONF_'))
    config = ParentConfig3(attr5=5, config_sources=ConfZEnvSource(allow_all=True, prefix='CONF_'))
    assert config.attr5 == 5
