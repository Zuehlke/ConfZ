class ConfZException(Exception):
    """The base exception. All other exceptions inherit from it."""


class ConfZFileException(ConfZException):
    """Exception which is raised if something went wrong while reading a configuration file."""


class ConfZEnvException(ConfZException):
    """Exception which is raised if something went wrong while reading environment variables."""
