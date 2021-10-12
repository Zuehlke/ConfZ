import pytest
from pydantic import ValidationError

from confz import ConfZ, ConfZEnvSource


class InnerConfig(ConfZ):
    attr1_name: int


class OuterConfig(ConfZ):
    attr2: int
    inner: InnerConfig


def test_allow_all(monkeypatch):
    monkeypatch.setenv('INNER__ATTR1-NAME', '1')
    monkeypatch.setenv('ATTR2', '2')
    config = OuterConfig(config_sources=ConfZEnvSource(
        allow_all=True
    ))
    assert config.inner.attr1_name == 1
    assert config.attr2 == 2


def test_allow_deny(monkeypatch):
    monkeypatch.setenv('INNER__ATTR1-NAME', '1')
    monkeypatch.setenv('ATTR2', '2')

    # works if all allowed
    config = OuterConfig(config_sources=ConfZEnvSource(
        allow=['inner__attr1_name', 'attr2']
    ))
    assert config.inner.attr1_name == 1
    assert config.attr2 == 2

    # raises error if not all allowed
    with pytest.raises(ValidationError):
        OuterConfig(config_sources=ConfZEnvSource(
            allow=['attr2']
        ))

    # raises error if denied
    with pytest.raises(ValidationError):
        OuterConfig(config_sources=ConfZEnvSource(
            allow=['inner__attr1_name', 'attr2'],
            deny=['attr2']
        ))


def test_prefix(monkeypatch):
    monkeypatch.setenv('CONFIG_INNER__ATTR1-NAME', '1')
    monkeypatch.setenv('CONFIG_ATTR2', '2')

    # prefix works
    config = OuterConfig(config_sources=ConfZEnvSource(
        allow_all=True,
        prefix='CONFIG_'
    ))
    assert config.inner.attr1_name == 1
    assert config.attr2 == 2

    # allow does not use prefix
    config = OuterConfig(config_sources=ConfZEnvSource(
        allow=['inner__attr1_name', 'attr2'],
        prefix='CONFIG_'
    ))
    assert config.inner.attr1_name == 1
    assert config.attr2 == 2

    # deny does not use prefix
    with pytest.raises(ValidationError):
        OuterConfig(config_sources=ConfZEnvSource(
            allow_all=True,
            deny=['attr2'],
            prefix='CONFIG_'
        ))


def test_remap(monkeypatch):
    # remap works
    monkeypatch.setenv('VAL1', '1')
    monkeypatch.setenv('VAL2', '2')
    config = OuterConfig(config_sources=ConfZEnvSource(
        allow_all=True,
        remap={
            'val1': 'inner__attr1_name',
            'val2': 'attr2',
        }
    ))
    assert config.inner.attr1_name == 1
    assert config.attr2 == 2

    # remap does not use prefix
    monkeypatch.setenv('CONFIG_VAL1', '3')
    monkeypatch.setenv('CONFIG_VAL2', '4')
    config = OuterConfig(config_sources=ConfZEnvSource(
        allow_all=True,
        prefix='CONFIG_',
        remap={
            'val1': 'inner__attr1_name',
            'val2': 'attr2',
        }
    ))
    assert config.inner.attr1_name == 3
    assert config.attr2 == 4
