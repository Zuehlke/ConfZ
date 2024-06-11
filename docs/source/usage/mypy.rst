ConfZ and MyPy
==============

ConfZ heavily relies on Metaclasses for its lazy loading and singleton design. Unfortunately, MyPy has limited support
for them so far (see `docs <https://mypy.readthedocs.io/en/stable/metaclasses.html>`_). Thus, it is likely that you
will get an error similar to this::

    Metaclass conflict: the metaclass of a derived class must be a (non-strict) subclass of the metaclasses of all its bases

So far, the only solution is to ignore these errors::

    class MyConfig(BaseConfig):  # type: ignore
        my_variable: bool

Future versions of MyPy might be able to correctly check ConfZ classes.
