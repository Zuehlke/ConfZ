class ConfZException(Exception):
    """The base exception. All other exceptions inherit from it."""


class ConfZUpdateException(ConfZException):
    """Exception which is raised if could not merge different config sources."""


class ConfZFileException(ConfZException):
    """Exception which is raised if something went wrong while reading a configuration file."""


class ConfZEnvException(ConfZException):
    """Exception which is raised if something went wrong while reading environment variables.
    PLACEHOLDER, NOT IN USE RIGHT NOW."""


class ConfZCLArgException(ConfZException):
    """Exception which is raised if something went wrong while reading command line arguments.
    PLACEHOLDER, NOT IN USE RIGHT NOW."""
