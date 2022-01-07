Config Listeners
================

With config sources as class variables, ConfZ provides an easy way to load configs the first time you need it.
Still, you can change it for e.g. unit tests with the corresponding context manager.

However, some libraries require you to define certain objects **on module level**, e.g.
`SQLAlchemy <https://docs.sqlalchemy.org/en/14/tutorial/engine.html>`_::

    engine = create_engine("sqlite:///my_db.db", echo=True, future=True)

If you would want to access your configuration here, you would loose all these benefits: The config file would be
loaded while you import your database module (unwanted side effects) and changing your config afterwards would not
affect the engine at all.

Instead, you could wrap the creation into a function call and only access your configuration within the function::

    def get_engine():
        return create_engine(f"sqlite:///{DBConfig().path}", echo=True, future=True)

However, now you create a new engine every time you access this function, which is not what you want / what
SQLAlchemy intends.

To overcome this issue, ConfZ provides a decorator :func:`~confz.depends_on`::

    from confz import depends_on

    @depends_on(DBConfig)
    def get_engine():
        return create_engine(f"sqlite:///{DBConfig().path}", echo=True, future=True)

It transforms any function into a singleton and only executes it the first time it gets accessed. Additionally, it
allows you to specify one or many config classes on which the function depends on. Whenever one of these configs
changed because we are in a config change context manager and the function gets accesses again, it re-executes,
allowing the new config to take effect. As soon as the context is left again, the original instance of the function
singleton will be active again.


Early Loading
-------------

We have already seen the helper function :func:`~confz.validate_all_configs` to force all config classes to load
their sources at a defined point in time. It provides an optional flag to also force all listeners to do the same::

    from confz import validate_all_configs

    if __name__ == '__main__':
        validate_all_configs(include_listeners=True)
        # your application code

This will also call all your functions decorated with :func:`~confz.depends_on` at any (reachable) location, if they
depend on a class that has `CONFIG_SOURCES` set.


Asynchronous Listeners
----------------------


The decorator also works for asynchronous functions::

    from confz import depends_on

    @depends_on(DBConfig)
    async def get_engine():
        engine = create_async_engine(f"sqlite:///{DBConfig().path}", echo=True)

        async with engine.begin() as conn:
            await conn.run_sync(meta.drop_all)
            await conn.run_sync(meta.create_all)

        return engine

As soon as you have at least one async listener defined, :func:`~confz.validate_all_configs` becomes async whenever
you set `include_listeners` to true. You could then call it with::

    import asyncio

    from confz import validate_all_configs

    async def main():
        await validate_all_configs(include_listeners=True)
        # your application code

    if __name__ == '__main__':
        asyncio.run(main())
