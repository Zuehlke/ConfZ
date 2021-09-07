from pathlib import Path

from confz import ConfZ, ConfZEnvSource, ConfZCLArgSource

ASSET_FOLDER = Path(__file__).parent.resolve() / 'assets'


class InnerConfig(ConfZ):
    some_attr_2: str
    some_attr_3: str


class MyConfig(ConfZ):
    some_attr_1: str
    inner_config: InnerConfig

    CONFIG_SOURCES = [
        ConfZEnvSource(allow_all=True),
        ConfZCLArgSource()
    ]


if __name__ == '__main__':
    print(MyConfig())
