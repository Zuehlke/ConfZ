import sys

from confz import ConfZ, ConfZCLArgSource


class InnerConfig(ConfZ):
    attr1: int


class OuterConfig(ConfZ):
    attr2: int
    inner: InnerConfig


def test_default(monkeypatch):
    argv_backup = sys.argv.copy()
    monkeypatch.setattr(
        sys, "argv", argv_backup + ["--inner.attr1", "1", "--attr2", "2"]
    )
    config = OuterConfig(config_sources=ConfZCLArgSource())
    assert config.inner.attr1 == 1
    assert config.attr2 == 2


def test_prefix(monkeypatch):
    argv_backup = sys.argv.copy()
    monkeypatch.setattr(
        sys, "argv", argv_backup + ["--conf_inner.attr1", "1", "--conf_attr2", "2"]
    )
    config = OuterConfig(config_sources=ConfZCLArgSource(prefix="conf_"))
    assert config.inner.attr1 == 1
    assert config.attr2 == 2


def test_remap(monkeypatch):
    argv_backup = sys.argv.copy()
    monkeypatch.setattr(sys, "argv", argv_backup + ["--val1", "1", "--attr2", "2"])
    config = OuterConfig(config_sources=ConfZCLArgSource(remap={"val1": "inner.attr1"}))
    assert config.inner.attr1 == 1
    assert config.attr2 == 2
