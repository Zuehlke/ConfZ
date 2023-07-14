from typing import Optional

import pytest
from pydantic import ValidationError

from confz import BaseConfig, EnvSource
from tests.assets import ASSET_FOLDER


class InnerConfig(BaseConfig):
    attr1_name: int
    attr_override: Optional[str] = None


class OuterConfig(BaseConfig):
    attr2: int
    inner: InnerConfig


def test_allow_all(monkeypatch):
    monkeypatch.setenv("ATTR2", "2")
    monkeypatch.setenv("INNER.ATTR1-NAME", "1")
    monkeypatch.setenv("INNER.ATTR-OVERRIDE", "secret")
    config = OuterConfig(config_sources=EnvSource(allow_all=True))
    assert config.inner.attr1_name == 1
    assert config.attr2 == 2
    assert config.inner.attr_override == "secret"


def test_allow_deny(monkeypatch):
    monkeypatch.setenv("ATTR2", "2")
    monkeypatch.setenv("INNER.ATTR1-NAME", "1")
    monkeypatch.setenv("INNER.ATTR-OVERRIDE", "secret")

    # works if all allowed
    config = OuterConfig(config_sources=EnvSource(allow=["inner.attr1_name", "attr2"]))
    assert config.attr2 == 2
    assert config.inner.attr1_name == 1
    assert config.inner.attr_override is None

    # raises error if not all allowed
    with pytest.raises(ValidationError):
        OuterConfig(config_sources=EnvSource(allow=["attr2"]))

    # raises error if none allowed
    with pytest.raises(ValidationError):
        OuterConfig(config_sources=EnvSource())

    # raises error if denied
    with pytest.raises(ValidationError):
        OuterConfig(
            config_sources=EnvSource(
                allow=["inner.attr1_name", "attr2"], deny=["attr2"]
            )
        )


def test_prefix(monkeypatch):
    monkeypatch.setenv("CONFIG_INNER.ATTR1-NAME", "1")
    monkeypatch.setenv("CONFIG_ATTR2", "2")

    # prefix works
    config = OuterConfig(config_sources=EnvSource(allow_all=True, prefix="CONFIG_"))
    assert config.attr2 == 2
    assert config.inner.attr1_name == 1

    # allow does not use prefix
    config = OuterConfig(
        config_sources=EnvSource(allow=["inner.attr1_name", "attr2"], prefix="CONFIG_")
    )
    assert config.attr2 == 2
    assert config.inner.attr1_name == 1

    # deny does not use prefix
    with pytest.raises(ValidationError):
        OuterConfig(
            config_sources=EnvSource(allow_all=True, deny=["attr2"], prefix="CONFIG_")
        )


def test_remap(monkeypatch):
    # remap works
    monkeypatch.setenv("VAL1", "1")
    monkeypatch.setenv("VAL2", "2")
    config = OuterConfig(
        config_sources=EnvSource(
            allow_all=True,
            remap={
                "val1": "inner.attr1_name",
                "val2": "attr2",
            },
        )
    )
    assert config.attr2 == 2
    assert config.inner.attr1_name == 1

    # remap does not use prefix
    monkeypatch.setenv("CONFIG_VAL1", "3")
    monkeypatch.setenv("CONFIG_VAL2", "4")
    config = OuterConfig(
        config_sources=EnvSource(
            allow_all=True,
            prefix="CONFIG_",
            remap={
                "val1": "inner.attr1_name",
                "val2": "attr2",
            },
        )
    )
    assert config.attr2 == 4
    assert config.inner.attr1_name == 3


def test_dotenv_loading(monkeypatch):
    monkeypatch.setenv("INNER.ATTR1_NAME", "21")
    monkeypatch.setenv("ATTR2", "1")
    config = OuterConfig(
        config_sources=EnvSource(allow_all=True, file=ASSET_FOLDER / "config.env")
    )
    assert config.attr2 == 1
    assert config.inner.attr1_name == 21
    assert config.inner.attr_override == "2002"


def test_dotenv_loading_missing_file(monkeypatch):
    monkeypatch.setenv("INNER.ATTR1_NAME", "21")
    monkeypatch.setenv("ATTR2", "1")
    config = OuterConfig(
        config_sources=EnvSource(allow_all=True, file=ASSET_FOLDER / "idontexist")
    )
    assert config.attr2 == 1
    assert config.inner.attr1_name == 21
    assert config.inner.attr_override is None


def test_dotenv_loading_from_bytes(monkeypatch):
    monkeypatch.setenv("INNER.ATTR1_NAME", "21")
    monkeypatch.setenv("ATTR2", "1")
    with (ASSET_FOLDER / "config.env").open("rb") as config_file:
        data = config_file.read()
    config = OuterConfig(config_sources=EnvSource(allow_all=True, file=data))
    assert config.attr2 == 1
    assert config.inner.attr1_name == 21
    assert config.inner.attr_override == "2002"


def test_separator(monkeypatch):
    monkeypatch.setenv("INNER__ATTR1_NAME", "21")
    monkeypatch.setenv("INNER__ATTR-OVERRIDE", "2002")
    monkeypatch.setenv("ATTR2", "1")
    config = OuterConfig(
        config_sources=EnvSource(allow_all=True, nested_separator="__")
    )
    assert config.attr2 == 1
    assert config.inner.attr1_name == 21
    assert config.inner.attr_override == "2002"
