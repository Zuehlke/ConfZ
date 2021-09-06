from pathlib import Path

from confz import ConfZ, ConfZCLArgSource

ASSET_FOLDER = Path(__file__).parent.resolve() / 'assets'


class InnerConfig(ConfZ):
    some_attr_2: str


class MyConfig(ConfZ):
    some_attr_new: str
    inner_config: InnerConfig

    CONFIG_SOURCES = ConfZCLArgSource(
        prefix='conf_',
        remap={'some_attr': 'some_attr_new'}
    )


if __name__ == '__main__':
    print(MyConfig())
