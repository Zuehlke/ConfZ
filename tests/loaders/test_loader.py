from confz import ConfZ, ConfZDataSource


class InnerConfig(ConfZ):
    attr1: int


class OuterConfig(ConfZ):
    attr2: int
    inner: InnerConfig


def test_update_dict_recursively():
    config = OuterConfig(config_sources=[
        ConfZDataSource(data={'inner': {'attr1': 1}, 'attr2': 2}),
        ConfZDataSource(data={'inner': {'attr1': 3}}),
        ConfZDataSource(data={'attr2': 4})
    ])
    assert config.inner.attr1 == 3
    assert config.attr2 == 4
