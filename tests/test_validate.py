import pytest
from pydantic import ValidationError

from confz import BaseConfig, DataSource, validate_all_configs, depends_on


def test_validate():
    # works with new configs
    class NewInner(BaseConfig):
        attr1: int

    class NewOuter(BaseConfig):
        inner: NewInner
        attr2: int

        CONFIG_SOURCES = DataSource(data={"inner": {"attr1": 1}, "attr2": 2})

    validate_all_configs()

    # detects missing data
    class NewOuter2(BaseConfig):
        inner: NewInner
        attr2: int

        CONFIG_SOURCES = DataSource(data={"attr2": 2})

    with pytest.raises(ValidationError):
        validate_all_configs()

    # adjust config sources so successive test don't fail because of NewOuter2
    NewOuter2.CONFIG_SOURCES = DataSource(data={"inner": {"attr1": 1}, "attr2": 2})


@pytest.mark.asyncio
async def test_listeners():
    class EmptyConfig(BaseConfig):
        CONFIG_SOURCES = []

    called_sync = False

    @depends_on(EmptyConfig)
    def working_fn_sync():
        nonlocal called_sync
        called_sync = True

    called_async = False

    @depends_on(EmptyConfig)
    async def working_fn_async():
        nonlocal called_async
        called_async = True

    validate_all_configs(include_listeners=False)
    assert not called_sync
    assert not called_async
    await validate_all_configs(include_listeners=True)
    assert called_sync
    assert called_async

    @depends_on(EmptyConfig)
    def broken_fn():
        raise ValueError

    validate_all_configs(include_listeners=False)
    with pytest.raises(ValueError):
        await validate_all_configs(include_listeners=True)
