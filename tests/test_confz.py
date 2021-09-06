from pathlib import Path

from confz import ConfZ, ConfZSource


class DummyConfig(ConfZ):
    some_attr: str


class MyConfig(ConfZ):
    some_attr: str

    CONFIG_SOURCE = ConfZSource(
        file=Path('asdf1')
    )


class MyConfig2(ConfZ):
    some_attr: str

    CONFIG_SOURCE = ConfZSource(
        file=Path('asdf2')
    )


def test_general():
    print()
    print(' ', DummyConfig(some_attr='qwer'))
    print(' ', MyConfig())
    print(' ', MyConfig2())
    print(' ', MyConfig())
    print(' ', MyConfig2())
    print(' ', MyConfig(config_source=ConfZSource()))
    print(' ', MyConfig2(config_source=ConfZSource()))
    print(MyConfig() is MyConfig())
