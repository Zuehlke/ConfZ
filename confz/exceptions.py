class ConfigException(Exception):
    """The base exception. All other exceptions inherit from it."""


class UpdateException(ConfigException):
    """Exception which is raised if could not merge different config sources."""


class FileException(ConfigException):
    """Exception which is raised if something went wrong while reading a
    configuration file."""
