from pathlib import Path

from confz import ConfZ, ConfZSource

ASSET_FOLDER = Path(__file__).parent.resolve() / 'assets'


class MyConfig(ConfZ):
    some_attr: str

    CONFIG_SOURCE = ConfZSource(
        file_folder=ASSET_FOLDER,
        file=Path('config.yml')
    )


if __name__ == '__main__':
    print(MyConfig())
