The ConfZ Class
===============

Raw Class
---------

Per default, the :class:`~confz.BaseConfig` class behaves like `BaseModel` of pydantic and allows to specify your config with
typehints, either using standard Python types or more
`advanced ones <https://pydantic-docs.helpmanual.io/usage/types/>`_:

>>> from confz import BaseConfig
>>> from pydantic import SecretStr, AnyUrl

>>> class DBConfig(BaseConfig):
...     user: str
...     password: SecretStr

>>> class APIConfig(BaseConfig):
...     host: AnyUrl
...     port: int
...     db: DBConfig

`Validators <https://pydantic-docs.helpmanual.io/usage/validators/>`_ are supported too.

This class can now be instantiated with keyword arguments:

>>> api_config = APIConfig(
...     host="http://my-host.com",
...     port=1234,
...     db={"user": "my-user", "password": "my-password"}
... )

>>> api_config
APIConfig(
    host=AnyUrl('http://my-host.com', scheme='http', host='my-host.com', tld='com', host_type='domain'),
    port=1234,
    db=DBConfig(user='my-user', password=SecretStr('**********'))
)

.. note::

   Pydantic sees itself as a parsing library, not a validation library. This means, it may cast input data to force it
   to conform to model field types, and in some cases this may result in a loss of information. See
   `data conversion <https://pydantic-docs.helpmanual.io/usage/models/#data-conversion>`_ for detailed information.

Since ``api_config`` is a standard python object, your IDE will give you full support like code-completion and
type-checks. It also supports all methods available by `BaseModel` of pydantic, for example:

>>> api_config.model_dump_json()
'{"host": "http://my-host.com", "port": 1234, "db": {"user": "my-user", "password": "**********"}}'

It is `faux-immutable <https://pydantic-docs.helpmanual.io/usage/models/#faux-immutability>`_ per default:

>>> api_config.port = 1
TypeError: "APIConfig" is immutable and does not support item assignment


Sources as Keyword
------------------

In most cases, we would not want to provide the config as keyword arguments. Instead, we can provide
:class:`~confz.ConfigSources` as argument `config_sources` and :class:`~confz.BaseConfig` will load them. For example,
if we have a config file in yaml format like this:

.. code-block:: yaml

    host: http://my-host.com
    port: 1234
    db:
        user: my-user
        password: my-password

We can load this file as follows:

>>> from confz import FileSource
>>> APIConfig(config_sources=FileSource(file="/path/to/config.yaml"))
APIConfig(
    host=AnyUrl('http://my-host.com', scheme='http', host='my-host.com', tld='com', host_type='domain'),
    port=1234,
    db=DBConfig(user='my-user', password=SecretStr('**********'))
)

ConfZ supports a rich set of sources, see :ref:`sources_loaders`. Of course, keyword arguments and config sources can
also be combined.

Sources as Class Variable
-------------------------

Defining config sources as keyword argument still requires you to explicitly instantiate your config class and passing
it to all corresponding software components. :class:`~confz.BaseConfig` provides an alternative to this by defining your
source as a class variable `CONFIG_SOURCES`:

>>> class DBConfig(BaseConfig):
...     user: str
...     password: SecretStr

>>> class APIConfig(BaseConfig):
...     host: AnyUrl
...     port: int
...     db: DBConfig
...
...     CONFIG_SOURCES = FileSource(file="/path/to/config.yaml")

From now on, your config values are accessible from anywhere within your code by just importing ``APIConfig`` and
instantiating it:

>>> APIConfig().port
1234
>>> APIConfig().db.user
'my-user'

By defining `CONFIG_SOURCES`, your class will furthermore automatically be a singleton. The first time you access
the constructor, the config sources are loaded. All successive calls will return the same cached instance
(lazy loading):

>>> APIConfig() is APIConfig()
True

As a consequence, an error will be raised if you try to pass keyword arguments to a config class with `CONFIG_SOURCES`
set.

Early Loading
^^^^^^^^^^^^^

:class:`~confz.BaseConfig` could also load your config sources directly during class creation. However, this yields unwanted
side effects like reading files and command line arguments during import of your config classes, which should be
avoided. Thus, :class:`~confz.BaseConfig` loads your config the first time you instantiate the class.

If at this point the config class cannot populate all mandatory fields, pydantic will raise an error. To make sure
this does not happen in an inconvenient moment, you can also manually load all configs at the beginning of your
program::

    from confz import validate_all_configs

    if __name__ == '__main__':
        validate_all_configs()
        # your application code

The function :func:`~confz.validate_all_configs` will instantiate all config classes defined in your code at any
(reachable) location that have `CONFIG_SOURCES` set.
