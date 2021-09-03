from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class ZConfigSource:
    file: Optional[Path] = None


def populate_config(config: dict, zconfig_source: ZConfigSource):  # TODO
    print('  POPULATE', zconfig_source)
    config['some_attr'] = 'some_val'
