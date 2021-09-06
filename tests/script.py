from pathlib import Path

from confz import ConfZ, ConfZFileSource

ASSET_FOLDER = Path(__file__).parent.resolve() / 'assets'


class MyConfig(ConfZ):
    some_attr: str

    CONFIG_SOURCES = ConfZFileSource(
        folder=ASSET_FOLDER,
        name=Path('config.yml')
    )


if __name__ == '__main__':
    print(MyConfig())
