.. _context_manager:

Context Manager
===============

In some scenarios, you might want to change your config values, for example within a unit test. However, if you set the
`CONFIG_SOURCES` class variable, this is not directly possible:

>>> from pathlib import Path
>>> from confz import BaseConfig, FileSource, DataSource

>>> class MyConfig(BaseConfig):
...     number: int
...     CONFIG_SOURCES = FileSource(file="/path/to/config.yml")

>>> print(MyConfig().number)
1

To overcome this, every config class provides a context manager to temporarily change your config:

>>> new_source = DataSource(data={"number": 42})
>>> with MyConfig.change_config_sources(new_source):
...     print(MyConfig().number)
...
42

As soon as the context is left, the old config is loaded again:

>>> print(MyConfig().number)
1

At entry, the context manager backs up the old config source definition and singleton instance, deletes it and sets
the new source definition. At exit, it undoes these steps, making sure the same singleton instance is available again
as before the context.

A common use case for this are pytest fixtures::

    @pytest.fixture
    def test_database():
        new_db_source = ...
        with DBConfig.change_config_sources(new_db_source):
            yield
