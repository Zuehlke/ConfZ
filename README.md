# ConfZ – Pydantic Config Management

ConfZ is a ... (TODO).

**Note:** PREVIEW, this project is under construction!

## Installation

`ConfZ` is on [PyPI](https://pypi.org/project/confz/) and can be installed with pip:

```shell
pip install confz
```

## Example Usage

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

    CONFIG_SOURCES = ConfZFileSource(name=Path('/path/to/config.yml'))
```

Thanks to [pydantic](https://pydantic-docs.helpmanual.io/), you can use a wide variety of
[field types](https://pydantic-docs.helpmanual.io/usage/types/) and 
[validators](https://pydantic-docs.helpmanual.io/usage/validators/).

From now on, in any other file, you can access your config directly:

```python
from config import APIConfig

print(f"Serving API at {APIConfig().host}, port {APIConfig().port}.")
```

As can be seen, the config does neither have to be loaded explicitly, nor instantiated globally. `ConfZ` automatically loads
your config as defined in `CONFIG_SOURCES` the first time you access it. Thanks to its singleton mechanism, this
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
        name_from_env='ENVIRONMENT'
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

Next to composition, `ConfZ` also supports inheritance. This allows to even further re-use your config, for example:

```python
from pathlib import Path

from confz import ConfZ, ConfZFileSource
from pydantic import SecretStr, AnyUrl

class DBConfig(ConfZ):
    user: str
    password: SecretStr

class LocalDBConfig(DBConfig):
    CONFIG_SOURCES = ConfZFileSource(name=Path('/path/to/config/local_db.yml'))

class RemoteDBConfig(DBConfig):
    host: AnyUrl
    CONFIG_SOURCES = ConfZFileSource(name=Path('/path/to/config/remote_db.yml'))
```

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

config1 = LocalConfig(config_sources=ConfZFileSource(name=Path('/path/to/config.yml')))    
config2 = LocalConfig(config_sources=ConfZEnvSource(prefix='CONF_', allow=['text']), number=1)
config3 = LocalConfig(number=1, text='hello world')
```

As can be seen, additional keyword-arguments can be provided as well. If neither class variable `CONFIG_SOURCES` nor
constructor argument `config_sources` is provided, `ConfZ` behaves like a regular _pydantic_ class.

## Documentation

TODO:
- Behaviour of ConfZ
  - Bare class
  - Usage with class variable (singleton, no kwargs)
  - Usage with init argument (no singleton, kwargs)
  - Restriction that only leaves can have class variables
- Loaders and their ConfZSource
  - Order / what overwrites whats (incl. kwargs)
  - Config Files
  - Environment Variables
  - CL Arguments
- Register own Loaders
- Exceptions
