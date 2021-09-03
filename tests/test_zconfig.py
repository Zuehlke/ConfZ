from pathlib import Path

from zconfig import ZConfig, ZConfigSource


class DummyConfig(ZConfig):
    some_attr: str


class MyConfig(ZConfig):
    some_attr: str

    CONFIG_SOURCE = ZConfigSource(
        file=Path('asdf1')
    )


class MyConfig2(ZConfig):
    some_attr: str

    CONFIG_SOURCE = ZConfigSource(
        file=Path('asdf2')
    )


def test_general():
    print()
    print(' ', DummyConfig(some_attr='qwer'))
    print(' ', MyConfig())
    print(' ', MyConfig2())
    print(' ', MyConfig())
    print(' ', MyConfig2())
    print(' ', MyConfig(config_source=ZConfigSource()))
    print(' ', MyConfig2(config_source=ZConfigSource()))
    print(MyConfig() is MyConfig())
