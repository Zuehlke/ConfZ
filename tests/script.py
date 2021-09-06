from pathlib import Path

from confz import ConfZ, ConfZEnvSource

ASSET_FOLDER = Path(__file__).parent.resolve() / 'assets'


class InnerConfig(ConfZ):
    some_attr_2: str


class MyConfig(ConfZ):
    some_attr: str
    inner_config: InnerConfig

    CONFIG_SOURCES = ConfZEnvSource(
        allow_all=True,
        prefix='CONF_'
    )


if __name__ == '__main__':
    print(MyConfig())
