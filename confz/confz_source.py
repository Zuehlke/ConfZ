from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class ConfZSource:
    """TODO"""
    file: Optional[Path] = None


def populate_config(config: dict, confz_source: ConfZSource):  # TODO
    print('  POPULATE', confz_source)
    config['some_attr'] = 'some_val'
