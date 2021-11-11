import pytest
from pydantic import ValidationError

from confz import ConfZ, ConfZDataSource, validate_all_configs


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
