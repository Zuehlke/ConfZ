from pathlib import Path

from confz import ConfZ

ASSET_FOLDER = Path(__file__).parent.resolve() / 'assets'


class InnerConfig(ConfZ):
    something: str


class MyConfig(ConfZ):
    my_attr: str
    inner: InnerConfig

    CONFIG_SOURCES = []


if __name__ == '__main__':
    print(MyConfig(my_attr='wer', inner={'something': 'wer'}))
    print(MyConfig())
