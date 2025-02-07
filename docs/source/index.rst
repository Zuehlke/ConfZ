ConfZ -- Pydantic Config Management
===================================

ConfZ is a configuration management library for Python based on `pydantic <https://pydantic-docs.helpmanual.io/>`_.
It easily allows you to

* load your configuration from config files, environment variables, command line arguments and more sources
* transform the loaded data into a desired format and validate it
* access the results as Python dataclass-like objects with full IDE support

It furthermore supports you in common use cases like:

* Multiple environments
* Singleton with lazy loading
* Config changes for unit tests
* Custom config sources

.. topic:: Quick Start

   This is the documentation of ConfZ. For a quick start, see the `README <https://github.com/Zuehlke/ConfZ#readme>`_.


Installation
------------

ConfZ is on `PyPI <https://pypi.org/project/confz/>`_ and can be installed with pip:

.. code-block:: console

   pip install confz

It requires python >= 3.8.


Contents
--------

.. toctree::
   :maxdepth: 2

   usage/usage
   migration_guide
   reference/reference


Index and Search
----------------

* :ref:`genindex`
* :ref:`search`
