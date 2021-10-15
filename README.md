# ConfZ – Pydantic Config Management

`ConfZ` is a configuration management library for Python based on [pydantic](https://pydantic-docs.helpmanual.io/).
It easily allows you to

* load your configuration from config files, environment variables, command line arguments and more sources
* transform the loaded data into a desired format and validate it
* access the results as Python dataclass-like objects with full IDE support

It furthermore supports you in common use cases like:

* Multiple environments
* Singleton with lazy loading
* Config changes for unit tests
* Custom config sources


## Installation

`ConfZ` is on [PyPI](https://pypi.org/project/confz/) and can be installed with pip:

```shell
pip install confz
```


## Quick Start

The first step of using `ConfZ` is to declare your config classes and sources, for example in `config.py`:

```python
from pathlib import Path

from confz import ConfZ, ConfZFileSource
from pydantic import SecretStr, AnyUrl

class DBConfig(ConfZ):
    user: str
    password: SecretStr

class APIConfig(ConfZ):
    host: AnyUrl
    port: int
    db: DBConfig

    CONFIG_SOURCES = ConfZFileSource(file=Path('/path/to/config.yml'))
```

Thanks to [pydantic](https://pydantic-docs.helpmanual.io/), you can use a wide variety of
[field types](https://pydantic-docs.helpmanual.io/usage/types/) and 
[validators](https://pydantic-docs.helpmanual.io/usage/validators/).

From now on, in any other file, you can access your config directly:

```python
from config import APIConfig

print(f"Serving API at {APIConfig().host}, port {APIConfig().port}.")
```

As can be seen, the config does neither have to be loaded explicitly, nor instantiated globally. `ConfZ` automatically
loads your config as defined in `CONFIG_SOURCES` the first time you access it. Thanks to its singleton mechanism, this
happens the first time only, afterwards you get back a cached,
[immutable](https://pydantic-docs.helpmanual.io/usage/models/#faux-immutability) instance, behaving like any other
_pydantic_ instance.

```python
assert APIConfig() is APIConfig()   # true
APIConfig().port = 1234             # raises an error
APIConfig().json()                  # get a json representation of the whole config
```

### More Config Sources

`ConfZ` is highly flexible in defining the source of your config. Do you have multiple environments? No Problem:

```python
from pathlib import Path

from confz import ConfZ, ConfZFileSource

class MyConfig(ConfZ):
    ...
    CONFIG_SOURCES = ConfZFileSource(
        folder=Path('/path/to/config/folder'),
        file_from_env='ENVIRONMENT'
    )
```

Your config file can now be defined in the environment variable `ENVIRONMENT` and is relative to `folder`.

You can also provide a list as config source and read for example from environment variables and from command line
arguments:

```python
from confz import ConfZ, ConfZEnvSource, ConfZCLArgSource

class MyConfig(ConfZ):
    ...
    CONFIG_SOURCES = [
        ConfZEnvSource(allow_all=True),
        ConfZCLArgSource(prefix='conf_')
    ]
```

`ConfZ` now tries to populate your config either from environment variables having the same name as your attributes or
by reading command line arguments that start with `conf_`. Recursive models are supported too, for example if you want
to control the user-name in the API above, you can either set the environment variable `DB__USER` or pass the command
line argument `--conf_db__user`.

### Local Configs

In some scenarios, the config should not be a singleton. Maybe the number of config instances is not even known at 
the time of defining the config class. Instead of defining `CONFIG_SOURCES` as class variable, the source can also be
passed to the constructor directly:

```python
from pathlib import Path

from confz import ConfZ, ConfZFileSource, ConfZEnvSource

class LocalConfig(ConfZ):
    number: int
    text: str

config1 = LocalConfig(config_sources=ConfZFileSource(file=Path('/path/to/config.yml')))    
config2 = LocalConfig(config_sources=ConfZEnvSource(prefix='CONF_', allow=['text']), number=1)
config3 = LocalConfig(number=1, text='hello world')
```

As can be seen, additional keyword-arguments can be provided as well. If neither class variable `CONFIG_SOURCES` nor
constructor argument `config_sources` is provided, `ConfZ` behaves like a regular _pydantic_ class.

### Change Config Values / Testing

In some scenarios, you might want to change your config values, for example within a unit test. However, if you set the
`CONFIG_SOURCES` class variable, this is not directly possible. To overcome this, every config class provides a context
manager to temporarily change your config:

```python
from pathlib import Path

from confz import ConfZ, ConfZFileSource, ConfZDataSource

class MyConfig(ConfZ):
    number: int
    CONFIG_SOURCES = ConfZFileSource(file=Path('/path/to/config.yml'))

print(MyConfig().number)                            # will print the value from the config-file

new_source = ConfZDataSource(data={'number': 42})
with MyConfig.change_config_sources(new_source):
    print(MyConfig().number)                        # will print '42'

print(MyConfig().number)                            # will print the value from the config-file again
```

### Validation

By default, your config gets loaded the first time you instantiate the class, e.g. with `MyConfig().attribute`. If the
config class cannot populate all mandatory fields, _pydantic_ will raise an error at this point. To make sure this does
not happen in an inconvenient moment, you can also instruct `ConfZ` to load all configs beforehand:

```python
from confz import validate_all_configs

if __name__ == '__main__':
    validate_all_configs()
    # your application code
```

The function `validate_all_configs` will instantiate all config classes defined in your code at any (reachable)
location that have `CONFIG_SOURCES` set. Please note that _validated_ means that _pydantic_ was able to parse your
input data, see [data conversion](https://pydantic-docs.helpmanual.io/usage/models/#data-conversion).


## Documentation

The full documentation of `ConfZ`'s features can be found at TODO.
