import pytest
from pydantic import ValidationError

from confz import ConfZ, ConfZDataSource, validate_all_configs, depends_on


def test_validate():
    # works with new configs
    class NewInner(ConfZ):
        attr1: int

    class NewOuter(ConfZ):
        inner: NewInner
        attr2: int

        CONFIG_SOURCES = ConfZDataSource(data={'inner': {'attr1': 1}, 'attr2': 2})

    validate_all_configs()

    # detects missing data
    class NewOuter2(ConfZ):
        inner: NewInner
        attr2: int

        CONFIG_SOURCES = ConfZDataSource(data={'attr2': 2})

    with pytest.raises(ValidationError):
        validate_all_configs()

    # adjust config sources so successive test don't fail because of NewOuter2
    NewOuter2.CONFIG_SOURCES = ConfZDataSource(data={'inner': {'attr1': 1}, 'attr2': 2})


def test_listeners():
    class EmptyConfig(ConfZ):
        CONFIG_SOURCES = []

    @depends_on(EmptyConfig)
    def working_fn():
        pass

    validate_all_configs(include_listeners=False)
    validate_all_configs(include_listeners=True)

    @depends_on(EmptyConfig)
    def broken_fn():
        raise ValueError

    validate_all_configs(include_listeners=False)
    with pytest.raises(ValueError):
        validate_all_configs(include_listeners=True)
