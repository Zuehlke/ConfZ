import sys

from confz.config_source import CLArgSource
from .loader import Loader


class CLArgLoader(Loader):
    """Config loader for command line arguments."""

    @classmethod
    def populate_config(cls, config: dict, config_source: CLArgSource):
        cl_args = {}
        for idx, cl_arg in enumerate(sys.argv[1:]):
            if cl_arg.startswith("--") and idx + 2 < len(sys.argv):
                cl_name = cl_arg[2:]
                cl_value = sys.argv[idx + 2]

                if config_source.prefix is not None:
                    if not cl_name.startswith(config_source.prefix):
                        continue
                    cl_name = cl_name[len(config_source.prefix) :]

                if config_source.remap is not None and cl_name in config_source.remap:
                    cl_name = config_source.remap[cl_name]

                cl_args[cl_name] = cl_value

        cl_args = cls.transform_nested_dicts(
            cl_args, separator=config_source.nested_separator
        )
        cls.update_dict_recursively(config, cl_args)
