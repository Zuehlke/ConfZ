import sys

from confz.confz_source import ConfZCLArgSource
from .loader import Loader


class CLArgLoader(Loader):
    """Config loader for command line arguments."""

    @classmethod
    def populate_config(cls, config: dict, confz_source: ConfZCLArgSource):
        cl_args = {}
        for idx, cl_arg in enumerate(sys.argv[1:]):
            if cl_arg.startswith("--") and idx + 2 < len(sys.argv):
                cl_name = cl_arg[2:]
                cl_value = sys.argv[idx + 2]

                if confz_source.prefix is not None:
                    if not cl_name.startswith(confz_source.prefix):
                        continue
                    cl_name = cl_name[len(confz_source.prefix) :]

                if confz_source.remap is not None and cl_name in confz_source.remap:
                    cl_name = confz_source.remap[cl_name]

                cl_args[cl_name] = cl_value

        cl_args = cls.transform_nested_dicts(
            cl_args, separator=confz_source.nested_separator
        )
        cls.update_dict_recursively(config, cl_args)
