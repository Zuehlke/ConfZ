from dataclasses import dataclass

from confz import ConfZ, ConfZDataSource, ConfZSource
from confz.loaders import Loader, register_loader


class InnerConfig(ConfZ):
    attr1: int


class OuterConfig(ConfZ):
    attr2: int
    inner: InnerConfig


@dataclass
class CustomSource(ConfZSource):
    custom_attr: int


class CustomLoader(Loader):

    @classmethod
    def populate_config(cls, config: dict, confz_source: CustomSource):
        assert config == {'kwarg_2': 2}
        assert confz_source.custom_attr == 1
        config['attr2'] = 2
        config['inner'] = {'attr1': 1}


register_loader(CustomSource, CustomLoader)


def test_update_dict_recursively():
    config = OuterConfig(config_sources=[
        ConfZDataSource(data={'inner': {'attr1': 1}, 'attr2': 2}),
        ConfZDataSource(data={'inner': {'attr1': 3}}),
        ConfZDataSource(data={'attr2': 4})
    ])
    assert config.inner.attr1 == 3
    assert config.attr2 == 4


def test_own_loader():
    config = OuterConfig(config_sources=CustomSource(
        custom_attr=1
    ), kwarg_2=2)
    assert config.inner.attr1 == 1
    assert config.attr2 == 2
