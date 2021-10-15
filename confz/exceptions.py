class ConfZException(Exception):
    """The base exception. All other exceptions inherit from it."""


class ConfZUpdateException(ConfZException):
    """Exception which is raised if could not merge different config sources."""


class ConfZFileException(ConfZException):
    """Exception which is raised if something went wrong while reading a configuration file."""


class ConfZEnvException(ConfZException):
    """Exception which is raised if something went wrong while reading environment variables.
    *Placeholder, this exception is not in use right now.*"""


class ConfZCLArgException(ConfZException):
    """Exception which is raised if something went wrong while reading command line arguments.
    *Placeholder, this exception is not in use right now.*"""
