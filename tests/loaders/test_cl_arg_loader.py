import sys

from confz import BaseConfig, CLArgSource


class InnerConfig(BaseConfig):
    attr1: int


class OuterConfig(BaseConfig):
    attr2: int
    inner: InnerConfig


def test_default(monkeypatch):
    argv = sys.argv.copy() + ["--inner.attr1", "1", "--attr2", "2"]
    monkeypatch.setattr(sys, "argv", argv)
    config = OuterConfig(config_sources=CLArgSource())
    assert config.inner.attr1 == 1
    assert config.attr2 == 2


def test_prefix(monkeypatch):
    argv = sys.argv.copy() + [
        "--conf_inner.attr1",
        "1",
        "--conf_attr2",
        "2",
        "--attr1",
        "100",
    ]
    monkeypatch.setattr(sys, "argv", argv)
    config = OuterConfig(config_sources=CLArgSource(prefix="conf_"))
    assert config.inner.attr1 == 1
    assert config.attr2 == 2


def test_remap(monkeypatch):
    argv = sys.argv.copy() + ["--val1", "1", "--attr2", "2"]
    monkeypatch.setattr(sys, "argv", argv)
    config = OuterConfig(config_sources=CLArgSource(remap={"val1": "inner.attr1"}))
    assert config.inner.attr1 == 1
    assert config.attr2 == 2


def test_nested_separator(monkeypatch):
    argv = sys.argv.copy() + [
        "--conf_inner__attr1",
        "1",
        "--conf_attr2",
        "2",
        "--attr1",
        "100",
    ]
    monkeypatch.setattr(sys, "argv", argv)
    config = OuterConfig(
        config_sources=CLArgSource(prefix="conf_", nested_separator="__")
    )
    assert config.inner.attr1 == 1
    assert config.attr2 == 2
